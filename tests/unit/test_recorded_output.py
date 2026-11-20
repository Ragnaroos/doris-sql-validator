from pathlib import Path

import pytest

from doris_sql_validator.models import (
    CaseDefinition,
    RecordedOutputSpec,
)
from doris_sql_validator.recorded_output import RecordedOutputError, parse_recorded_case
from doris_sql_validator.recorded_output.pg_echo import pg_echo_identity, pg_echo_pattern
from doris_sql_validator.source_provider import (
    RecordedOutputProvider,
    SourceEvidenceError,
)


def test_hive_qtest_output_is_paired_by_normalized_sql_hash() -> None:
    sql = "SELECT 1 AS value;"
    case = CaseDefinition(
        id="hive-one",
        statement_index=1,
        sql=sql,
        output_occurrence=1,
    )
    output = (
        "PREHOOK: query: SELECT 1 AS value\n"
        "PREHOOK: type: QUERY\n"
        "POSTHOOK: query: SELECT 1 AS value\n"
        "POSTHOOK: type: QUERY\n"
        "1\n"
    )

    evidence = parse_recorded_case(
        output_format="hive-qtest",
        output_text=output,
        case=case,
        dialect="hive",
        artifact="sample.q.out",
    )

    assert evidence.result.success is True
    assert evidence.result.rows == [["1"]]
    assert evidence.capabilities.column_names is False


def test_hive_qtest_skips_non_query_prehooks_and_masked_hook_lines() -> None:
    case = CaseDefinition(
        id="hive-official-shape",
        statement_index=3,
        sql="select count(*) from t_n34 group by ();",
        output_occurrence=1,
    )
    output = (
        "PREHOOK: query: create table t_n34 (a int)\n"
        "PREHOOK: type: CREATETABLE\n"
        "POSTHOOK: query: create table t_n34 (a int)\n"
        "POSTHOOK: type: CREATETABLE\n"
        "PREHOOK: query: insert into t_n34 values (1),(1),(2)\n"
        "PREHOOK: type: QUERY\n"
        "POSTHOOK: query: insert into t_n34 values (1),(1),(2)\n"
        "POSTHOOK: type: QUERY\n"
        "PREHOOK: query: select count(*) from t_n34 group by ()\n"
        "PREHOOK: type: QUERY\n"
        "PREHOOK: Input: default@t_n34\n"
        "#### A masked pattern was here ####\n"
        "POSTHOOK: query: select count(*) from t_n34 group by ()\n"
        "POSTHOOK: type: QUERY\n"
        "POSTHOOK: Input: default@t_n34\n"
        "#### A masked pattern was here ####\n"
        "3\n"
    )

    evidence = parse_recorded_case(
        output_format="hive-qtest",
        output_text=output,
        case=case,
        dialect="hive",
        artifact="groupby_empty.q.out",
    )

    assert evidence.result.success is True
    assert evidence.result.rows == [["3"]]


def test_recorded_provider_reads_current_output_without_fingerprint(tmp_path: Path) -> None:
    output = tmp_path / "sample.out"
    sql = "SELECT 1 AS value;"
    output.write_text(sql + "\n value\n-------\n 1\n(1 row)\n")
    spec = RecordedOutputSpec(format="pg-regress", file="sample.out")
    output.write_text(sql + "\n value\n-------\n 2\n(1 row)\n")
    provider = RecordedOutputProvider(spec, base_dir=tmp_path, dialect="postgres")
    case = CaseDefinition(id="pg-one", statement_index=1, sql=sql, output_occurrence=1)
    assert provider.get_result(case).result.rows == [["2"]]
    assert "sha256" not in spec.model_dump()


def test_recorded_provider_still_reports_missing_output(tmp_path: Path) -> None:
    spec = RecordedOutputSpec(format="pg-regress", file="missing.out")
    with pytest.raises(SourceEvidenceError, match="Cannot read recorded output"):
        RecordedOutputProvider(spec, base_dir=tmp_path, dialect="postgres")


def test_pg_output_preserves_trailing_empty_string_row() -> None:
    sql = "SELECT value FROM sample;"
    case = CaseDefinition(
        id="pg-empty-string",
        statement_index=1,
        sql=sql,
        output_occurrence=1,
    )
    output = (
        f"{sql}\n"
        " value\n"
        "-------\n"
        " a\n"
        "  \n"
        "(2 rows)\n"
    )

    evidence = parse_recorded_case(
        output_format="pg-regress",
        output_text=output,
        case=case,
        dialect="postgres",
        artifact="sample.out",
    )

    assert evidence.result.rows == [["a"], [""]]


def _pg(sql: str, output: str, occurrence: int = 1):
    return parse_recorded_case(
        output_format="pg-regress", output_text=output,
        case=CaseDefinition(id="pg-echo-test", statement_index=1, sql=sql, output_occurrence=occurrence),
        dialect="postgres", artifact="sample.out",
    )


def test_pg_echo_allows_blank_layout_lines_and_preserves_original_result():
    sql = "WITH t AS (\n\n -- comment\n SELECT 1 AS v\n\n)\nSELECT v FROM t;"
    echo = "WITH t AS (\n -- comment\n SELECT 1 AS v\n)\nSELECT v FROM t;"
    output = echo + "\n v\n---\n 1\n  \n(2 rows)\n"
    assert _pg(sql, output).result.rows == [["1"], [""]]
    assert pg_echo_identity(sql) == pg_echo_identity(echo)


@pytest.mark.parametrize("protected", [
    "'a\n\nb'", '"a\n\nb"', "$tag$a\n\nb$tag$", "$$a\n\nb$$",
    "E'a\\\'\n\nb'", "/* outer\n\n /* inner */ end */ 1",
])
def test_pg_echo_does_not_erase_protected_blank_lines(protected):
    sql = "SELECT " + protected + ";"
    changed = sql.replace("\n\n", "\n")
    assert pg_echo_identity(sql) != pg_echo_identity(changed)
    assert pg_echo_pattern(sql).search(sql)
    assert not pg_echo_pattern(sql).search(changed)


def test_pg_echo_does_not_merge_spaces_inside_literal_or_identifier():
    assert pg_echo_identity("SELECT 'a b';") != pg_echo_identity("SELECT 'ab';")
    assert pg_echo_identity('SELECT "a b";') != pg_echo_identity('SELECT "ab";')


@pytest.mark.parametrize("footer", ["SELECT 2;\n v\n---\n 2\n(1 row)\n", "SELECT 2;\nERROR: division by zero\n"])
def test_pg_missing_output_cannot_borrow_next_query_result_or_error(footer):
    with pytest.raises(RecordedOutputError, match="immediately after"):
        _pg("SELECT 1;", "SELECT 1;\n" + footer)


def test_pg_missing_row_marker_stops_before_next_query():
    output = "SELECT 1;\n v\n---\n 1\nSELECT 2;\n v\n---\n 2\n(5 rows)\n"
    with pytest.raises(RecordedOutputError, match="next command"):
        _pg("SELECT 1;", output)


def test_pg_repeated_query_preserves_negative_result_and_stage_order():
    output = "SELECT v FROM t;\nERROR: permission denied\nSELECT v FROM t;\n v\n---\n 2\n(1 row)\n"
    assert not _pg("SELECT v FROM t;", output).result.success
    assert _pg("SELECT v FROM t;", output, 2).result.rows == [["2"]]
    with pytest.raises(RecordedOutputError, match="not found"):
        _pg("SELECT v FROM t;", output, 3)


def test_pg_matching_requires_whole_echo_not_a_subquery_or_prefix():
    for output in [
        "EXPLAIN SELECT 1;\n v\n---\n 1\n(1 row)\n",
        "SELECT 10;\n v\n---\n 10\n(1 row)\n",
        "SELECT 1; SELECT 2;\n v\n---\n 1\n(1 row)\n",
    ]:
        with pytest.raises(RecordedOutputError, match="not found"):
            _pg("SELECT 1;", output)


def test_pg_echo_optional_terminator_and_crlf_do_not_double_count():
    output = "SELECT 1;\r\n v\r\n---\r\n 1\r\n(1 row)\r\nSELECT 1\r\n v\r\n---\r\n 2\r\n(1 row)\r\n"
    assert _pg("SELECT 1;", output, 2).result.rows == [["2"]]
    assert _pg("SELECT 1", output).result.rows == [["1"]]


def test_pg_zero_rows_remain_a_success_not_a_missing_result():
    evidence = _pg("SELECT 1 WHERE FALSE;", "SELECT 1 WHERE FALSE;\n v\n---\n(0 rows)\n")
    assert evidence.result.success
    assert evidence.result.rows == []


def test_pg_echo_trailing_comment_is_not_a_second_command_or_result():
    output = "SELECT 1; -- documented expected value\n v\n---\n 1\n(1 row)\n"
    assert _pg("SELECT 1;", output).result.rows == [["1"]]


@pytest.mark.parametrize("wrapper", [
    "PREPARE p AS\nSELECT v FROM t;\nEXECUTE p;\n",
    "EXPLAIN (VERBOSE, COSTS OFF)\nSELECT v FROM t;\n",
    "CREATE VIEW v AS\nSELECT v FROM t;\n",
    "SELECT * FROM (\nSELECT v FROM t\n) AS q;\n",
    "CREATE FUNCTION f() RETURNS text LANGUAGE sql AS $$\nSELECT v FROM t;\n$$;\n",
])
def test_pg_echo_matches_only_independent_complete_statements(wrapper):
    output = (
        wrapper + " v\n-------\n other\n(1 row)\n\n"
        "SELECT v FROM t;\n v\n-------\n first\n(1 row)\n"
        "SELECT v FROM t;\n v\n--------\n second\n(1 row)\n"
    )
    assert _pg("SELECT v FROM t;", output).result.rows == [["first"]]
    assert _pg("SELECT v FROM t;", output, 2).result.rows == [["second"]]


def test_pg_echo_does_not_match_prefix_before_where_on_next_line():
    output = (
        "SELECT v FROM t\nWHERE v = 2;\n v\n---\n 2\n(1 row)\n"
        "SELECT v FROM t;\n v\n---\n 1\n(1 row)\n"
    )
    assert _pg("SELECT v FROM t;", output).result.rows == [["1"]]
    with pytest.raises(RecordedOutputError, match="not found"):
        _pg("SELECT v FROM t;", output, 2)


def test_pg_echo_cannot_match_sql_text_printed_inside_multiline_result():
    output = (
        "SELECT definition FROM views;\n definition\n----------------------\n"
        " SELECT v FROM t;    +\n"
        " SELECT v FROM t;\n(1 row)\n"
        "SELECT v FROM t;\n v\n---\n 3\n(1 row)\n"
    )
    assert _pg("SELECT v FROM t;", output).result.rows == [["3"]]


def test_pg_echo_cannot_match_sql_inside_nested_comments_or_copy_data():
    output = (
        "/* outer\n /* nested */\nSELECT v FROM t;\n*/\n"
        "COPY log FROM stdin;\nSELECT v FROM t;\n\\.\n"
        "SELECT v FROM t;\n v\n---\n 4\n(1 row)\n"
    )
    assert _pg("SELECT v FROM t;", output).result.rows == [["4"]]


def test_pg_echo_copy_with_suppressed_payload_does_not_hide_following_queries():
    output = (
        "COPY t FROM stdin;\nSELECT v FROM t;\n v\n---\n 1\n(1 row)\n"
        "COPY t FROM stdin;\nERROR: bad value\nSELECT v FROM t;\n v\n---\n 2\n(1 row)\n"
    )
    assert _pg("SELECT v FROM t;", output).result.rows == [["1"]]
    assert _pg("SELECT v FROM t;", output, 2).result.rows == [["2"]]


def test_pg_echo_does_not_confuse_cte_comments_with_result_separators():
    sql = "WITH t AS (VALUES\n (1),\n  --\n (2)\n)\nSELECT * FROM t;"
    output = sql + "\n v\n---\n 1\n 2\n(2 rows)\n"
    assert _pg(sql, output).result.rows == [["1"], ["2"]]


@pytest.mark.parametrize("sql", [
    "(SELECT 2) UNION SELECT 2;",
    "((SELECT 2)) UNION SELECT 2;",
    "(\nSELECT 2\n) UNION SELECT 2;",
])
def test_pg_echo_preserves_parenthesized_query_start(sql):
    output = sql + "\n v\n---\n 2\n(1 row)\n"
    assert _pg(sql, output).result.rows == [["2"]]


def test_pg_echo_sv_deparsed_definition_is_not_an_echo_or_prefix_of_next_sql():
    output = (
        "\\sv v\nCREATE OR REPLACE VIEW public.v AS\n SELECT v FROM t\n"
        "SELECT v FROM t;\n v\n---\n 7\n(1 row)\n"
    )
    assert _pg("SELECT v FROM t;", output).result.rows == [["7"]]


def test_pg_notice_cascade_lines_do_not_hide_following_drop_or_select():
    output = (
        "DROP TYPE mytype CASCADE;\nNOTICE: drop cascades to 2 other objects\n"
        "drop cascades to function f()\ndrop cascades to cast from mytype to real\n"
        "DROP TABLE t;\nSELECT 1;\n v\n---\n 1\n(1 row)\n"
    )
    assert _pg("SELECT 1;", output).result.rows == [["1"]]


def test_pg_multiline_warning_skips_xml_source_and_caret_not_the_result():
    sql = "SELECT xpath('/*', '<relativens xmlns=''relative''/>');"
    output = (
        sql + "\nWARNING:  line 1: xmlns: URI relative is not absolute\n"
        "<relativens xmlns='relative'/>\n"
        "                            ^\n"
        " xpath\n--------\n value\n(1 row)\n"
    )
    assert _pg(sql, output).result.rows == [["value"]]


def test_pg_multiline_notice_can_precede_expanded_result_or_current_error():
    prefix = "SELECT 1;\nNOTICE: diagnostic\n  continued\nDETAIL: more\nHINT: hint\n"
    assert _pg("SELECT 1;", prefix + "-[ RECORD 1 ]\nv | 1\n\n").result.rows == [["1"]]
    evidence = _pg("SELECT 1;", prefix + "ERROR: division by zero\n")
    assert not evidence.result.success
    assert evidence.result.error.message == "division by zero"


@pytest.mark.parametrize("diagnostic", [
    "WARNING: xml warning\n<bad/>\n     ^\n",
    "NOTICE: notice\n  indented continuation\n",
])
def test_pg_warning_without_result_cannot_borrow_next_query(diagnostic):
    output = "SELECT 1;\n" + diagnostic + "  SELECT 2;\n v\n---\n 2\n(1 row)\n"
    with pytest.raises(RecordedOutputError, match="immediately after"):
        _pg("SELECT 1;", output)


def test_pg_expanded_output_preserves_columns_empty_fields_and_error_info():
    sql = "SELECT * FROM pg_input_error_info('bad', 'integer');"
    output = (
        sql + "\n-[ RECORD 1 ]--+------------------------\n"
        'message        | invalid input: "bad"\n'
        "detail         | \n"
        "hint           | \n"
        "sql_error_code | 22P02\n\n"
        "SELECT 2;\n v\n---\n 2\n(1 row)\n"
    )
    evidence = _pg(sql, output)
    assert evidence.result.success
    assert [c.name for c in evidence.result.columns] == [
        "message", "detail", "hint", "sql_error_code",
    ]
    assert evidence.result.rows == [['invalid input: "bad"', "", "", "22P02"]]
    assert not evidence.capabilities.column_types
    assert evidence.capabilities.row_values == "display_text"


def test_pg_expanded_multiple_records_keep_duplicate_column_names_and_literal_symbols():
    sql = "SELECT * FROM sample;"
    output = (
        sql + "\n-[ RECORD 1 ]\n"
        "v | left | right\n"
        "v | C++\n"
        "-[ RECORD 2 ]\n"
        "v | \n"
        "v | +\n\n"
    )
    evidence = _pg(sql, output)
    assert [c.name for c in evidence.result.columns] == ["v", "v"]
    assert evidence.result.rows == [["left | right", "C++"], ["", "+"]]


def test_pg_expanded_multiline_field_preserves_indentation_and_blank_lines():
    sql = "SELECT text FROM sample;"
    output = (
        sql + "\n-[ RECORD 1 ]-------\n"
        "text | first          +\n"
        "     |                +\n"
        "     |   SELECT a | b\n\n"
    )
    assert _pg(sql, output).result.rows == [["first\n\n  SELECT a | b"]]


@pytest.mark.parametrize("body, message", [
    ("-[ RECORD 1 ]\na | 1\n-[ RECORD 3 ]\na | 2\n\n", "record number"),
    ("-[ RECORD 1 ]\na | 1\nb | 2\n-[ RECORD 2 ]\na | 3\n\n", "columns"),
    ("-[ RECORD 1 ]\na | 1\n-[ RECORD 2 ]\nb | 2\n\n", "columns"),
    ("-[ RECORD 1 ]\na | first\n  | second\n\n", "continuation"),
    ("-[ RECORD 1 ]\na | 1\nSELECT 2;\n v\n---\n 2\n(1 row)\n", "next command"),
    ("-[ RECORD 1 ]\n\n", "empty record"),
])
def test_pg_expanded_rejects_incomplete_or_inconsistent_records(body, message):
    with pytest.raises(RecordedOutputError, match=message):
        _pg("SELECT 1;", "SELECT 1;\n" + body)


def test_pg_expanded_no_result_cannot_borrow_next_record():
    output = "SELECT 1;\nSELECT 2;\n-[ RECORD 1 ]\nv | 2\n\n"
    with pytest.raises(RecordedOutputError, match="immediately after"):
        _pg("SELECT 1;", output)


def test_pg_expanded_repeated_echo_stays_with_its_own_result():
    sql = "SELECT v FROM t;"
    output = (
        sql + "\n-[ RECORD 1 ]\nv | first\n\n"
        + sql + "\n v\n--------\n second\n(1 row)\n"
    )
    assert _pg(sql, output).result.rows == [["first"]]
    assert _pg(sql, output, 2).result.rows == [["second"]]


def test_pg_expanded_complete_record_at_end_of_file_needs_no_row_footer():
    assert _pg("SELECT 1;", "SELECT 1;\n-[ RECORD 1 ]\nv | 1").result.rows == [["1"]]


def test_pg_expanded_rejects_incorrect_optional_row_footer():
    with pytest.raises(RecordedOutputError, match="row marker"):
        _pg("SELECT 1;", "SELECT 1;\n-[ RECORD 1 ]\nv | 1\n(2 rows)\n")


def test_pg_expanded_zero_rows_has_no_invented_column_evidence():
    evidence = _pg("SELECT 1 WHERE FALSE;", "SELECT 1 WHERE FALSE;\n(0 rows)\n\n")
    assert evidence.result.success
    assert evidence.result.rows == []
    assert not evidence.capabilities.column_count
    assert not evidence.capabilities.column_names
    assert evidence.capabilities.row_count


def test_pg_aligned_multiline_value_is_one_row_and_keeps_sql_indentation():
    sql = "SELECT pg_get_viewdef('v', true);"
    output = (
        sql + "\n pg_get_viewdef\n----------------\n"
        "  SELECT a     +\n"
        "    FROM t;\n"
        "(1 row)\n"
    )
    assert _pg(sql, output).result.rows == [[" SELECT a\n   FROM t;"]]


def test_pg_aligned_multiline_columns_finish_independently_and_keep_empty_last_row():
    sql = "SELECT a, b FROM sample;"
    output = (
        sql + "\n a   | b\n-----+-----\n"
        " a  +| C++\n"
        "    +| \n"
        " c   | \n"
        "     | \n"
        "(2 rows)\n"
    )
    assert _pg(sql, output).result.rows == [["a\n\nc", "C++"], ["", ""]]


def test_pg_aligned_multiline_in_different_columns_preserves_literal_plus_and_pipe():
    sql = "SELECT a, b FROM sample;"
    output = (
        sql + "\n a   | b\n-----+-----\n"
        " C++ | x  +\n"
        "     | y|z\n"
        "(1 row)\n"
    )
    assert _pg(sql, output).result.rows == [["C++", "x\ny|z"]]


def test_pg_aligned_literal_plus_before_newline_marker_remains_data():
    output = "SELECT v FROM t;\n v\n------\n C++ +\n end\n(1 row)\n"
    assert _pg("SELECT v FROM t;", output).result.rows == [["C++\nend"]]


def test_pg_aligned_last_newline_is_preserved():
    output = "SELECT v FROM t;\n v\n-----\n a  +\n \n(1 row)\n"
    assert _pg("SELECT v FROM t;", output).result.rows == [["a\n"]]


def test_pg_aligned_wide_unicode_does_not_shift_column_boundaries():
    sql = "SELECT a, b FROM sample;"
    output = sql + "\n a   | b\n-----+----\n 中文| yes\n(1 row)\n"
    assert _pg(sql, output).result.rows == [["中文", "yes"]]


def test_pg_aligned_combining_character_does_not_shift_column_boundaries():
    sql = "SELECT a, b FROM sample;"
    output = sql + "\n a | b\n---+---\n e\u0301 | x\n(1 row)\n"
    assert _pg(sql, output).result.rows == [["e\u0301", "x"]]


@pytest.mark.parametrize("body, message", [
    (" v\n-----\n a  +\n(1 row)\n", "continuation"),
    (" a   | b\n-----+-----\n a  +| x\n b   | y\n(1 row)\n", "finished column"),
    (" v\n-----\n a  +\nSELECT 2;\n v\n---\n 2\n(1 row)\n", "next command"),
    (" a | b\n---+---\n x | y | z\n(1 row)\n", "column width"),
])
def test_pg_aligned_rejects_truncated_or_misaligned_multiline_rows(body, message):
    with pytest.raises(RecordedOutputError, match=message):
        _pg("SELECT 1;", "SELECT 1;\n" + body)
