from __future__ import annotations

import re
import unicodedata
from collections import Counter

from ..execution.common import classify_error
from ..models import (
    CaseDefinition,
    EvidenceCapabilities,
    NormalizedError,
    QueryColumn,
    QueryResult,
    SourceEvidence,
)
from ..sql_utils import sql_sha256
from .pg_echo import pg_echo_matches, pg_skip_notices


class RecordedOutputError(ValueError):
    pass


def parse_recorded_case(
    *,
    output_format: str,
    output_text: str,
    case: CaseDefinition,
    dialect: str,
    artifact: str,
) -> SourceEvidence:
    if case.output_occurrence is None:
        raise RecordedOutputError(f"Case {case.id} has no output_occurrence")
    if output_format == "pg-regress":
        return _parse_pg_regress(output_text, case, artifact)
    if output_format == "hive-qtest":
        return _parse_hive_qtest(
            output_text, case, dialect, artifact
        )
    raise RecordedOutputError(f"Unsupported recorded output format: {output_format}")


def _parse_pg_regress(
    output_text: str,
    case: CaseDefinition,
    artifact: str,
) -> SourceEvidence:
    occurrence = case.output_occurrence
    assert occurrence is not None
    positions = pg_echo_matches(case.sql, output_text)
    if len(positions) < occurrence:
        raise RecordedOutputError(
            f"RECORDED_OUTPUT_UNPARSABLE: SQL echo for {case.id} not found"
        )
    tail = output_text[positions[occurrence - 1].end() :]
    lines = tail.splitlines()
    start = pg_skip_notices(lines, 0)
    error_match = re.match(r"^ERROR:\s*(.+)$", lines[start]) if start < len(lines) else None
    if error_match:
        message = error_match.group(1).strip()
        normalized = classify_error(RuntimeError(message))
        result = QueryResult(
            engine="postgres-recorded",
            success=False,
            error=NormalizedError(
                category=normalized.category,
                message=message,
                code=normalized.code,
            ),
        )
        return SourceEvidence(
            mode="recorded_output",
            result=result,
            capabilities=EvidenceCapabilities(
                column_count=False,
                column_names=False,
                column_types=False,
                row_count=False,
                row_values="unavailable",
                complex_types=False,
            ),
            value_encoding="postgres_psql_text",
            artifact=artifact,
            statement_index=case.statement_index,
        )
    # A result must immediately follow this echo. Never search a later query
    # for a table that happens to be readable.
    if start < len(lines) and _PG_RECORD.fullmatch(lines[start]):
        header, rows = _parse_pg_expanded(lines[start:], case.id)
    elif start < len(lines) and lines[start] == "(0 rows)":
        # Expanded output omits column names entirely for an empty result.
        header, rows = [], []
    else:
        header, rows = _parse_pg_aligned(lines[start:], case.id)
    result = QueryResult(
        engine="postgres-recorded",
        success=True,
        columns=[QueryColumn(name=name, canonical_type="unknown") for name in header],
        rows=rows,
    )
    return SourceEvidence(
        mode="recorded_output",
        result=result,
        capabilities=EvidenceCapabilities(
            column_count=bool(header),
            column_names=bool(header),
            column_types=False,
            row_values="display_text",
            complex_types=False,
        ),
        value_encoding="postgres_psql_text",
        artifact=artifact,
        statement_index=case.statement_index,
    )


_PG_RECORD = re.compile(r"^-\[ RECORD ([1-9]\d*) \]-*(?:\+-*)?$")
_PG_ROW_COUNT = re.compile(r"\((\d+) rows?\)\s*")
_PG_NEXT_COMMAND = re.compile(
    r"(?i)^(?:SELECT\b|WITH\b|VALUES\b|TABLE\b|CREATE\b|INSERT\b|UPDATE\b|"
    r"DELETE\b|COPY\b|ALTER\b|DROP\b|SET\b|RESET\b|ERROR:|--|\\)"
)


def _pg_failure(message: str, case_id: str) -> RecordedOutputError:
    return RecordedOutputError(f"RECORDED_OUTPUT_UNPARSABLE: {message} for {case_id}")


def _pg_char_width(char: str) -> int:
    # psql column boundaries use display positions, not Unicode code points.
    if unicodedata.category(char) in {"Mn", "Me", "Cf"}:
        return 0
    return 2 if unicodedata.east_asian_width(char) in {"W", "F"} else 1


def _pg_display_width(text: str) -> int:
    return sum(_pg_char_width(char) for char in text)


def _pg_aligned_cells(line: str, widths: list[int], case_id: str) -> list[str]:
    # Split only at the separator positions established by the horizontal
    # rule. A literal pipe inside a field is data, not a column separator.
    boundaries = []
    offset = 0
    for width in widths[:-1]:
        offset += width
        boundaries.append(offset)
        offset += 1
    cuts = []
    position = 0
    for index, char in enumerate(line):
        if len(cuts) < len(boundaries) and position == boundaries[len(cuts)] and char == "|":
            cuts.append(index)
        position += _pg_char_width(char)
    if len(cuts) != len(boundaries) or position > sum(widths) + len(boundaries):
        raise _pg_failure("column width mismatch", case_id)
    cells = []
    start = 0
    for cut in cuts:
        cells.append(line[start:cut])
        start = cut + 1
    cells.append(line[start:])
    return cells


def _parse_pg_aligned(lines: list[str], case_id: str) -> tuple[list[str], list[list[str]]]:
    if len(lines) < 2 or not re.fullmatch(r"\s*-+(?:\+-+)*\s*", lines[1]):
        raise _pg_failure("no aligned table immediately after SQL echo", case_id)
    widths = [len(part) for part in lines[1].split("+")]
    header = [cell.strip() for cell in _pg_aligned_cells(lines[0], widths, case_id)]
    raw_rows = []
    row_match = None
    for line in lines[2:]:
        row_match = _PG_ROW_COUNT.fullmatch(line)
        if row_match:
            break
        if _PG_NEXT_COMMAND.match(line):
            raise _pg_failure("next command or error before row marker", case_id)
        raw_rows.append(line)
    if row_match is None:
        raise _pg_failure("no row marker", case_id)
    expected_rows = int(row_match.group(1))
    rows = []
    fragments: list[list[str]] = [[] for _ in header]
    continuing = [False] * len(header)
    pending = False
    for line in raw_rows:
        cells = _pg_aligned_cells(line, widths, case_id)
        next_continuing = []
        for index, (cell, width) in enumerate(zip(cells, widths)):
            # In ASCII aligned mode '+' is a newline marker only in the
            # right margin. A value such as 'C++' stops before that margin.
            follows = cell.endswith("+") and _pg_display_width(cell) == width
            text = cell[:-1] if follows else cell
            text = text.removeprefix(" ").rstrip(" ")
            if not pending or continuing[index]:
                fragments[index].append(text)
            elif text.strip() or follows:
                raise _pg_failure("nonempty continuation of a finished column", case_id)
            next_continuing.append(follows)
        continuing = next_continuing
        pending = any(continuing)
        if not pending:
            rows.append([
                "\n".join(parts) if len(parts) > 1 else parts[0].strip()
                for parts in fragments
            ])
            fragments = [[] for _ in header]
    if pending:
        raise _pg_failure("unterminated cell continuation before row marker", case_id)
    # Only discard *extra* blank logical rows, after joining physical lines.
    # Otherwise a real empty-string row after a multiline row could disappear.
    while len(rows) > expected_rows and all(not cell for cell in rows[-1]):
        rows.pop()
    if len(rows) != expected_rows:
        raise _pg_failure(
            f"row marker={expected_rows}, parsed={len(rows)}", case_id
        )
    return header, rows


def _parse_pg_expanded(lines: list[str], case_id: str) -> tuple[list[str], list[list[str]]]:
    header: list[str] = []
    rows: list[list[str]] = []
    names: list[str] = []
    fragments: list[list[str]] = []
    separator_position: int | None = None

    def finish_record() -> None:
        nonlocal header
        if not names:
            raise _pg_failure("empty record in expanded output", case_id)
        if not header:
            header = names.copy()
        elif header != names:
            raise _pg_failure("inconsistent columns in expanded output", case_id)
        rows.append([
            "\n".join(parts) if len(parts) > 1 else parts[0].strip()
            for parts in fragments
        ])

    for index, line in enumerate(lines):
        record = _PG_RECORD.fullmatch(line)
        if record:
            if index:
                finish_record()
            if int(record.group(1)) != len(rows) + 1:
                raise _pg_failure("unexpected expanded record number", case_id)
            names, fragments = [], []
            continue
        # Expanded mode normally has no '(n rows)' footer: a blank line or
        # EOF closes the block. Never scan past that boundary for more fields.
        if not line.strip():
            finish_record()
            return header, rows
        row_count = _PG_ROW_COUNT.fullmatch(line)
        if row_count:
            finish_record()
            if int(row_count.group(1)) != len(rows):
                raise _pg_failure("expanded row marker mismatch", case_id)
            return header, rows
        if _PG_NEXT_COMMAND.match(line):
            raise _pg_failure("next command or error before expanded result boundary", case_id)
        name, separator, text = line.partition("|")
        position = _pg_display_width(name)
        if not separator or (separator_position is not None and position != separator_position):
            raise _pg_failure("invalid expanded field separator", case_id)
        separator_position = position
        text = text.removeprefix(" ").rstrip(" ")
        if name.strip():
            names.append(name.strip())
            fragments.append([text])
        else:
            # Blank field labels repeat the preceding field, not a new column.
            if not fragments or not fragments[-1][-1].endswith("+"):
                raise _pg_failure("expanded continuation without newline marker", case_id)
            fragments[-1][-1] = fragments[-1][-1][:-1].rstrip(" ")
            fragments[-1].append(text)
    finish_record()
    return header, rows


_HIVE_PREHOOK = re.compile(
    r"(?ms)^PREHOOK: query:\s*(.*?)\nPREHOOK: type:\s*([A-Z_]+)\s*$"
)


def _parse_hive_qtest(
    output_text: str,
    case: CaseDefinition,
    dialect: str,
    artifact: str,
) -> SourceEvidence:
    occurrence = case.output_occurrence
    assert occurrence is not None
    target_hash = sql_sha256(case.sql, dialect)
    matches = list(_HIVE_PREHOOK.finditer(output_text))
    occurrences: Counter[str] = Counter()
    selected: tuple[re.Match[str], int] | None = None
    for index, match in enumerate(matches):
        if match.group(2) != "QUERY":
            continue
        query = match.group(1).strip()
        try:
            current_hash = sql_sha256(query, dialect)
        except Exception:
            continue
        occurrences[current_hash] += 1
        if current_hash == target_hash and occurrences[current_hash] == occurrence:
            selected = (match, index)
            break
    if selected is None:
        raise RecordedOutputError(
            f"RECORDED_OUTPUT_UNPARSABLE: PREHOOK query for {case.id} not found"
        )
    match, index = selected
    end = matches[index + 1].start() if index + 1 < len(matches) else len(output_text)
    block = output_text[match.start() : end]
    failed = re.search(r"(?mi)^(?:FAILED|ERROR):\s*(.+)$", block)
    if failed:
        message = failed.group(1).strip()
        normalized = classify_error(RuntimeError(message))
        return SourceEvidence(
            mode="recorded_output",
            result=QueryResult(
                engine="hive-recorded",
                success=False,
                error=NormalizedError(
                    category=normalized.category,
                    message=message,
                    code=normalized.code,
                ),
            ),
            capabilities=EvidenceCapabilities(
                column_count=False,
                column_names=False,
                column_types=False,
                row_count=False,
                row_values="unavailable",
                complex_types=False,
            ),
            value_encoding="hive_qtest_text",
            artifact=artifact,
            statement_index=case.statement_index,
        )

    marker = "#### A masked pattern was here ####"
    posthook_lines = list(re.finditer(r"(?m)^POSTHOOK:.*$", block))
    if not posthook_lines:
        raise RecordedOutputError(
            f"RECORDED_OUTPUT_UNPARSABLE: no POSTHOOK for {case.id}"
        )
    result_text = block[posthook_lines[-1].end() :]
    lines = result_text.strip("\r\n").splitlines() if result_text.strip("\r\n") else []
    # Apache Hive QTest masks non-deterministic hook metadata with this line.
    # It appears between the last POSTHOOK field and the actual tab-separated
    # result and is not itself a result row.
    lines = [line for line in lines if line.strip() != marker]
    rows = [line.split("\t") for line in lines]
    width = max((len(row) for row in rows), default=0)
    if any(len(row) != width for row in rows):
        raise RecordedOutputError(
            f"RECORDED_OUTPUT_UNPARSABLE: inconsistent tab columns for {case.id}"
        )
    result = QueryResult(
        engine="hive-recorded",
        success=True,
        columns=[QueryColumn(name=f"column_{i + 1}") for i in range(width)],
        rows=rows,
    )
    return SourceEvidence(
        mode="recorded_output",
        result=result,
        capabilities=EvidenceCapabilities(
            column_names=False,
            column_types=False,
            row_values="display_text",
            complex_types=False,
        ),
        value_encoding="hive_qtest_text",
        artifact=artifact,
        statement_index=case.statement_index,
    )
