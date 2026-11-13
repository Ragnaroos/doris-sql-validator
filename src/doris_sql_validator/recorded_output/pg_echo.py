"""Conservative pg_regress echo identity and complete-command lookup.

Only blank layout lines and the final terminator are optional. SQL is not
regenerated from an AST: aliases, case, comments and literal contents survive.
"""
from __future__ import annotations

from bisect import bisect_right
from functools import lru_cache
import re


_LAYOUT_LINES = re.compile(r"\r?\n(?:[ \t]*\r?\n)*")
_DOLLAR_TAG = re.compile(r"\$(?:[A-Za-z_][A-Za-z_0-9]*)?\$")
_COMMAND_START = re.compile(
    r"(?i)^[ \t]*(?:\([ \t]*)*(?:SELECT|WITH|VALUES|TABLE|PREPARE|EXECUTE|DEALLOCATE|"
    r"EXPLAIN|CREATE|ALTER|DROP|DO|INSERT|UPDATE|DELETE|MERGE|COPY|SET|RESET|"
    r"SHOW|BEGIN|START|COMMIT|END|ABORT|ROLLBACK|SAVEPOINT|RELEASE|TRUNCATE|"
    r"GRANT|REVOKE|COMMENT|SECURITY|VACUUM|ANALYZE|CLUSTER|REINDEX|REFRESH|"
    r"DECLARE|FETCH|MOVE|CLOSE|LOCK|DISCARD|LISTEN|NOTIFY|UNLISTEN|CHECKPOINT|"
    r"CALL|IMPORT|LOAD|REASSIGN)\b"
)
_ALIGNED_RULE = re.compile(r"\s*-+(?:\+-+)*\s*")
_EXPANDED_RECORD = re.compile(r"^-\[ RECORD [1-9]\d* \]-*(?:\+-*)?$")
_ROW_COUNT = re.compile(r"\(\d+ rows?\)\s*")
_DIAGNOSTIC = re.compile(r"^(?:NOTICE|WARNING|DETAIL|HINT|CONTEXT):")


def _protected_end(sql: str, i: int) -> int | None:
    if sql.startswith("--", i):
        end = sql.find("\n", i)
        return end if end >= 0 else len(sql)
    if sql.startswith("/*", i):
        depth, end = 1, i + 2
        while end < len(sql) and depth:
            if sql.startswith("/*", end):
                depth += 1
                end += 2
            elif sql.startswith("*/", end):
                depth -= 1
                end += 2
            else:
                end += 1
        return end
    if sql[i] in {"'", '"'}:
        quote = sql[i]
        escaped = quote == "'" and i > 0 and sql[i - 1] in "eE" and (
            i < 2 or not (sql[i - 2].isalnum() or sql[i - 2] == "_")
        )
        end = i + 1
        while end < len(sql):
            if escaped and sql[end] == "\\":
                end += 2
            elif sql[end] == quote:
                end += 1
                if end < len(sql) and sql[end] == quote:
                    end += 1
                else:
                    break
            else:
                end += 1
        return min(end, len(sql))
    if sql[i] == "$" and (tag := _DOLLAR_TAG.match(sql, i)):
        close = sql.find(tag[0], tag.end())
        return close + len(tag[0]) if close >= 0 else len(sql)
    return None


def _parts(sql: str):
    """Yield layout/code or protected strings, identifiers and comments."""
    start = i = 0
    while i < len(sql):
        end = _protected_end(sql, i)
        if end is None:
            i += 1
            continue
        if start < i:
            yield False, sql[start:i]
        yield True, sql[i:end]
        start = i = end
    if start < len(sql):
        yield False, sql[start:]


def _body(sql: str) -> str:
    return sql.strip().removesuffix(";").rstrip()


@lru_cache(maxsize=512)
def pg_echo_identity(sql: str) -> str:
    return "".join(
        text if protected else _LAYOUT_LINES.sub("\n", text)
        for protected, text in _parts(_body(sql))
    )


@lru_cache(maxsize=512)
def pg_echo_pattern(sql: str) -> re.Pattern[str]:
    fragments = []
    for protected, text in _parts(_body(sql)):
        if protected:
            fragments.append(re.escape(text))
        else:
            pieces = _LAYOUT_LINES.split(text)
            fragments.append(r"\r?\n(?:[ \t]*\r?\n)*".join(map(re.escape, pieces)))
    # This regex describes spelling/layout only. pg_echo_matches also checks
    # the complete outer command, not just a matching line inside its body.
    return re.compile(
        r"^[ \t]*" + "".join(fragments) + r"[ \t]*;?[ \t]*(?:--[^\r\n]*)?(?=\r?$)",
        re.MULTILINE,
    )


def _aligned_header(lines: list[str], index: int) -> bool:
    # Default psql rules start in column zero and are at least three cells
    # wide. An indented '--' inside a CTE is a SQL comment, not a table rule.
    return (index + 1 < len(lines) and lines[index + 1].startswith("-")
            and len(lines[index + 1]) >= 3
            and bool(_ALIGNED_RULE.fullmatch(lines[index + 1])))


def pg_skip_notices(lines: list[str], start: int) -> int:
    """Skip explicit diagnostics, never search arbitrarily for a later result."""
    diagnostic = False
    while start < len(lines):
        line = lines[start]
        if not line.strip():
            start += 1
        elif _DIAGNOSTIC.match(line):
            diagnostic = True
            start += 1
        elif _aligned_header(lines, start) or _EXPANDED_RECORD.fullmatch(line):
            break
        elif diagnostic and re.match(r"^drop cascades to\b", line):
            start += 1
        elif diagnostic and not _COMMAND_START.match(line) and not line.startswith("ERROR:"):
            # libxml warnings print the input excerpt on a separate line,
            # followed by a caret. Neither line has a WARNING/DETAIL prefix.
            if start + 1 < len(lines) and re.fullmatch(r"[ \t]*\^[ \t]*", lines[start + 1]):
                start += 2
            elif line.startswith((" ", "\t")):
                start += 1
            else:
                break
        else:
            break
    return start


def _echo_end(text: str, lines: list[str], offsets: list[int], first: int) -> tuple[int, int]:
    """Locate a command terminator outside strings/comments/dollar quotes."""
    start = offsets[first]
    i = start
    while i < len(text):
        line_index = bisect_right(offsets, i) - 1
        if i > start and i == offsets[line_index]:
            line = lines[line_index]
            if (_aligned_header(lines, line_index) or _EXPANDED_RECORD.fullmatch(line)
                    or _ROW_COUNT.fullmatch(line) or _DIAGNOSTIC.match(line)
                    or line.startswith(("ERROR:", "\\"))):
                # Support the existing optional final-semicolon convention.
                # A result/diagnostic is a boundary, not part of the SQL.
                return i, line_index
        end = _protected_end(text, i)
        if end is not None:
            i = end
        elif text[i] == ";":
            # Keep the whole line: 'SELECT 1; SELECT 2;' must not match either
            # command individually when its output cannot be disambiguated.
            last = bisect_right(offsets, i) - 1
            return offsets[last] + len(lines[last]), last + 1
        else:
            i += 1
    return len(text), len(lines)


@lru_cache(maxsize=4)
def _command_spans(text: str) -> tuple[tuple[int, int], ...]:
    """Index outer echoes while excluding displayed result cells and COPY data.

    This is a pg_regress/psql transcript scanner, not a SQL semantic parser.
    Unsupported or incomplete blocks are not guessed into a successful match.
    """
    physical_lines = text.splitlines(keepends=True)
    lines = [line.rstrip("\r\n") for line in physical_lines]
    offsets = []
    offset = 0
    for line in physical_lines:
        offsets.append(offset)
        offset += len(line)
    spans = []
    index = 0
    while index < len(lines):
        line = lines[index]
        if _aligned_header(lines, index):
            index += 2
            while index < len(lines) and not _ROW_COUNT.fullmatch(lines[index]):
                if lines[index] and not lines[index][0].isspace() and _COMMAND_START.match(lines[index]):
                    break
                index += 1
            if index < len(lines) and _ROW_COUNT.fullmatch(lines[index]):
                index += 1
        elif _EXPANDED_RECORD.fullmatch(line):
            index += 1
            while index < len(lines) and lines[index].strip():
                if "|" not in lines[index] and _COMMAND_START.match(lines[index]):
                    break
                index += 1
        elif _DIAGNOSTIC.match(line):
            index = pg_skip_notices(lines, index)
        elif re.match(r"^\s*\\sv\b", line):
            # \sv prints an unterminated CREATE VIEW definition, not a new
            # echoed command. Its deparsed body is indented; the next outer
            # command starts in column zero in pg_regress transcripts.
            index += 1
            if index < len(lines) and re.match(r"(?i)^CREATE\b", lines[index]):
                index += 1
                while index < len(lines) and lines[index].strip():
                    if not lines[index][0].isspace() and _COMMAND_START.match(lines[index]):
                        break
                    index += 1
        elif line.lstrip().startswith("/*"):
            comment_start = offsets[index] + len(line) - len(line.lstrip())
            end = _protected_end(text, comment_start)
            assert end is not None
            index = bisect_right(offsets, end - 1)
        elif _COMMAND_START.match(line) or re.fullmatch(r"[ \t]*\(+[ \t]*", line):
            end, following = _echo_end(text, lines, offsets, index)
            spans.append((offsets[index], end))
            is_copy = re.match(r"(?is)^\s*COPY\b.*\bFROM\s+stdin\s*;", text[offsets[index]:end])
            index = following
            if is_copy:
                # pg_regress normally suppresses COPY's stdin payload in the
                # expected .out (including '\.'). Only skip an explicit data
                # block when its terminator is actually present before output.
                data_end = index
                while data_end < len(lines):
                    if lines[data_end].strip() == "\\.":
                        index = data_end + 1
                        break
                    if (_aligned_header(lines, data_end) or _EXPANDED_RECORD.fullmatch(lines[data_end])
                            or _DIAGNOSTIC.match(lines[data_end]) or lines[data_end].startswith("ERROR:")):
                        break
                    data_end += 1
        else:
            index += 1
    return tuple(spans)


def pg_echo_matches(sql: str, output: str) -> list[re.Match[str]]:
    pattern = pg_echo_pattern(sql)
    matches = []
    for start, end in _command_spans(output):
        while end > start and output[end - 1] in "\r\n":
            end -= 1
        if match := pattern.fullmatch(output, start, end):
            matches.append(match)
    return matches
