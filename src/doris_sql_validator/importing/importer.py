from __future__ import annotations

import os
import re
from collections import Counter
from dataclasses import dataclass
from pathlib import Path
from sqlglot.errors import ParseError

from ..models import (
    CaseDefinition,
    CaseFile,
    ImportDiagnostic,
    ImportSummary,
    InputSpec,
    RecordedOutputSpec,
    SourceSpec,
    TargetSpec,
)
from ..recorded_output import RecordedOutputError, parse_recorded_case
from ..recorded_output.pg_echo import pg_echo_identity
from ..sql_utils import file_sha256, parse_read_only_query, sql_sha256


@dataclass(frozen=True)
class ImportOptions:
    input_format: str
    dialect: str
    source_engine: str
    source_connection_profile: str | None
    target_connection_profile: str = "doris-local"
    source_database: str | None = None
    target_database: str | None = None
    recorded_output: Path | None = None
    qtest_driver: str | None = None


@dataclass(frozen=True)
class ScriptStatement:
    index: int
    text: str
    line_start: int
    line_end: int


def import_case_file(
    source_path: Path,
    output_path: Path,
    options: ImportOptions,
) -> CaseFile:
    source_path = source_path.resolve()
    output_path = output_path.resolve()
    source_text = source_path.read_text(encoding="utf-8")
    if options.input_format not in {"raw-sql", "pg-regress", "hive-qtest"}:
        raise ValueError(f"Unsupported input format: {options.input_format}")
    if options.recorded_output and options.input_format == "raw-sql":
        raise ValueError("raw-sql does not define a Recorded Output format")
    prepared = _sanitize_harness(source_text, options.input_format)
    statements = split_sql_script(prepared)
    diagnostics: list[ImportDiagnostic] = []
    cases: list[CaseDefinition] = []
    hash_occurrences: Counter[str] = Counter()
    parse_failed: set[str] = set()
    prefix = {
        "raw-sql": "sql",
        "pg-regress": "pg",
        "hive-qtest": "hive",
    }[options.input_format]
    source_ref = _relative_path(source_path, output_path.parent)
    output_ref_path = (
        _recorded_output_path(options.recorded_output.resolve(), output_path.parent)
        if options.recorded_output
        else None
    )

    for statement in statements:
        raw = _strip_leading_comments(statement.text.strip())
        if not raw:
            continue
        parser_failed = False
        try:
            parse_read_only_query(raw, options.dialect)
        except Exception as exc:
            statement_type = _statement_type(raw, options.dialect)
            disposition = "skipped" if statement_type != "parse_error" else "error"
            diagnostics.append(
                ImportDiagnostic(
                    statement_index=statement.index,
                    line_start=statement.line_start,
                    line_end=statement.line_end,
                    disposition=disposition,
                    statement_type=statement_type,
                    reason=str(exc),
                )
            )
            # Preserve SELECT-shaped parser failures for the ordinary run/report
            # path. No SQL is executed unless the transpiler later parses and
            # passes its read-only AST guard. DDL/DML and unsafe ASTs stay out.
            parser_failed = isinstance(exc, ParseError) and bool(
                re.match(r"(?is)^\s*\(*\s*(SELECT|WITH|VALUES|TABLE)\b", raw)
            )
            if not parser_failed:
                continue

        digest = file_sha256(raw.encode("utf-8")) if parser_failed else sql_sha256(raw, options.dialect)
        # Hive matches normalized AST hashes; pg_regress matches original SQL
        # echoes with only safe layout differences. Do not mix their counters.
        occurrence_key = pg_echo_identity(raw) if options.input_format == "pg-regress" else digest
        hash_occurrences[occurrence_key] += 1
        case_id = _case_id(prefix, source_path.stem, statement.index, digest)
        case = CaseDefinition(
            id=case_id,
            statement_index=statement.index,
            line_start=statement.line_start,
            line_end=statement.line_end,
            sql=raw,
            output_occurrence=(
                hash_occurrences[occurrence_key] if options.recorded_output else None
            ),
        )
        cases.append(case)
        if parser_failed:
            parse_failed.add(case.id)

    recorded_spec = None
    output_text = None
    if options.recorded_output:
        content = options.recorded_output.resolve().read_bytes()
        output_text = content.decode("utf-8")
        recorded_spec = RecordedOutputSpec(
            format=(
                "pg-regress"
                if options.input_format == "pg-regress"
                else "hive-qtest"
            ),
            file=output_ref_path or options.recorded_output.name,
            driver=options.qtest_driver,
        )
        validated: list[CaseDefinition] = []
        for case in cases:
            if case.id in parse_failed:
                # Parsing is the first failing stage. Do not replace that error
                # with a secondary .out locator error or silently drop the case.
                validated.append(case)
                continue
            try:
                parse_recorded_case(
                    output_format=recorded_spec.format,
                    output_text=output_text,
                    case=case,
                    dialect=options.dialect,
                    artifact=recorded_spec.file,
                )
            except RecordedOutputError as exc:
                diagnostics.append(
                    ImportDiagnostic(
                        statement_index=case.statement_index,
                        line_start=case.line_start or 1,
                        line_end=case.line_end or case.line_start or 1,
                        disposition="error",
                        statement_type="recorded_output",
                        reason=str(exc),
                        case_id=case.id,
                        sql=case.sql,
                        output_occurrence=case.output_occurrence,
                    )
                )
            else:
                validated.append(case)
        cases = validated

    if not cases:
        raise ValueError(
            "No executable read-only Query could be imported with the selected "
            "source dialect and Recorded Output format"
        )
    return CaseFile(
        source=SourceSpec(
            dialect=options.dialect,
            engine=options.source_engine,
            connection_profile=options.source_connection_profile,
            database=options.source_database,
        ),
        target=TargetSpec(
            connection_profile=options.target_connection_profile,
            database=options.target_database,
        ),
        input=InputSpec(
            format=options.input_format,
            file=source_ref,
            sha256=file_sha256(source_path.read_bytes()),
        ),
        recorded_output=recorded_spec,
        import_summary=ImportSummary(
            accepted=len(cases),
            skipped=sum(item.disposition == "skipped" for item in diagnostics),
            ambiguous=sum(item.disposition == "ambiguous" for item in diagnostics),
            errors=sum(item.disposition == "error" for item in diagnostics),
        ),
        import_diagnostics=diagnostics,
        cases=cases,
    )


def split_sql_script(text: str) -> list[ScriptStatement]:
    statements: list[ScriptStatement] = []
    start = 0
    start_line = 1
    line = 1
    index = 0
    i = 0
    quote: str | None = None
    dollar_tag: str | None = None
    line_comment = False
    block_comment = False
    while i < len(text):
        char = text[i]
        pair = text[i : i + 2]
        if char == "\n":
            line += 1
            line_comment = False
            i += 1
            continue
        if line_comment:
            i += 1
            continue
        if block_comment:
            if pair == "*/":
                block_comment = False
                i += 2
            else:
                i += 1
            continue
        if dollar_tag:
            if text.startswith(dollar_tag, i):
                i += len(dollar_tag)
                dollar_tag = None
            else:
                i += 1
            continue
        if quote:
            if char == quote:
                if i + 1 < len(text) and text[i + 1] == quote:
                    i += 2
                    continue
                quote = None
            elif char == "\\" and quote in {"'", '"'}:
                i += 2
                continue
            i += 1
            continue
        if pair == "--":
            line_comment = True
            i += 2
            continue
        if pair == "/*":
            block_comment = True
            i += 2
            continue
        if char in {"'", '"', "`"}:
            quote = char
            i += 1
            continue
        if char == "$":
            match = re.match(r"\$[A-Za-z_][A-Za-z0-9_]*\$|\$\$", text[i:])
            if match:
                dollar_tag = match.group(0)
                i += len(dollar_tag)
                continue
        if char == ";":
            index += 1
            segment = text[start : i + 1]
            statements.append(
                ScriptStatement(
                    index=index,
                    text=segment,
                    line_start=_first_content_line(segment, start_line),
                    line_end=line,
                )
            )
            start = i + 1
            start_line = line
        i += 1
    trailing = text[start:].strip()
    if trailing:
        index += 1
        segment = text[start:]
        statements.append(
            ScriptStatement(
                index=index,
                text=segment,
                line_start=_first_content_line(segment, start_line),
                line_end=line,
            )
        )
    return statements


def _first_content_line(segment: str, base_line: int) -> int:
    leading_length = len(segment) - len(segment.lstrip())
    return base_line + segment[:leading_length].count("\n")


def _sanitize_harness(text: str, input_format: str) -> str:
    if input_format != "pg-regress":
        return text
    lines = text.splitlines(keepends=True)
    sanitized: list[str] = []
    copy_data = False
    for line in lines:
        stripped = line.lstrip()
        if copy_data:
            sanitized.append("-- pg_regress COPY data omitted\n")
            if stripped.startswith("\\."):
                copy_data = False
            continue
        if stripped.startswith("\\"):
            if stripped.startswith(("\\gset", "\\gexec", "\\watch")):
                prefix = "".join(sanitized).rstrip()
                if prefix and not prefix.endswith(";"):
                    sanitized.append("\n__PSQL_STATEFUL_META_COMMAND__;\n")
                    continue
            sanitized.append("-- pg_regress psql command omitted\n")
            continue
        sanitized.append(line)
        if re.search(r"(?i)\bCOPY\b.*\bFROM\s+stdin\s*;\s*$", line):
            copy_data = True
    return "".join(sanitized)


def _statement_type(sql: str, dialect: str) -> str:
    stripped = _strip_leading_comments(sql)
    if stripped.startswith("!"):
        return "shell"
    keyword = stripped.split(None, 1)[0].rstrip(";").lower() if stripped else "empty"
    known_non_query = {
        "create",
        "alter",
        "drop",
        "insert",
        "update",
        "delete",
        "merge",
        "set",
        "reset",
        "load",
        "copy",
        "dfs",
        "use",
        "explain",
        "source",
        "shell",
    }
    return keyword if keyword in known_non_query else "parse_error"


def _strip_leading_comments(sql: str) -> str:
    stripped = sql.lstrip()
    while stripped:
        if stripped.startswith("--"):
            newline = stripped.find("\n")
            if newline < 0:
                return ""
            stripped = stripped[newline + 1 :].lstrip()
            continue
        if stripped.startswith("/*"):
            end = stripped.find("*/", 2)
            if end < 0:
                return stripped
            stripped = stripped[end + 2 :].lstrip()
            continue
        break
    return stripped


def _case_id(prefix: str, stem: str, index: int, digest: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", stem.lower()).strip("-") or "script"
    return f"{prefix}-{slug}-{index:04d}-{digest[:8]}"


def _relative_path(path: Path, base: Path) -> str:
    return Path(os.path.relpath(path, base)).as_posix()


def _recorded_output_path(path: Path, base: Path) -> str:
    # The caller explicitly supplies the reference output. Keep the original
    # file in place even when generated YAML lives in a reports directory.
    return _relative_path(path.resolve(), base.resolve())
