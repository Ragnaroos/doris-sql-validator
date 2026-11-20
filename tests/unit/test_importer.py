from pathlib import Path

import pytest

from doris_sql_validator.importing import ImportOptions, import_case_file
from doris_sql_validator.importing.importer import split_sql_script
from doris_sql_validator.source_provider import RecordedOutputProvider


def _options(*, recorded_output: Path | None = None) -> ImportOptions:
    return ImportOptions(
        input_format="pg-regress" if recorded_output else "raw-sql",
        dialect="postgres",
        source_engine="postgres",
        source_connection_profile="postgres-local",
        recorded_output=recorded_output,
    )


def test_splitter_keeps_semicolon_inside_string() -> None:
    statements = split_sql_script("SELECT 'a;b' AS value;\nSELECT 2 AS value;")
    assert len(statements) == 2
    assert "'a;b'" in statements[0].text
    assert statements[0].line_start == 1
    assert statements[1].line_start == 2


@pytest.mark.parametrize("recorded", [False, True])
def test_parser_failure_is_retained_for_normal_validation(tmp_path, recorded):
    from doris_sql_validator.case_loader import load_case_file, write_case_file
    from doris_sql_validator.service import ValidationService
    from doris_sql_validator.reporting import write_reports
    import json

    sql = "SELECT DISTINCT ON (a) a FROM t ORDER BY a USING <;"
    source = tmp_path / "unsupported.sql"
    source.write_text(sql + "\n" + sql)
    output = tmp_path / "unsupported.out"
    # Output lookup must not hide the primary SQLGlot parser failure.
    output.write_text("no matching query output")
    path = tmp_path / "cases.yaml"
    definition = import_case_file(source, path, _options(recorded_output=output if recorded else None))
    assert len(definition.cases) == 2
    assert definition.import_summary.errors == 2
    if recorded:
        assert [c.output_occurrence for c in definition.cases] == [1, 2]
    write_case_file(definition, path)
    definition = load_case_file(path).definition

    class NeverExecute:
        def execute_select(self, *args, **kwargs):
            pytest.fail("parser failures must not reach the database")
        def get_result(self, *args, **kwargs):
            pytest.fail("parser failures must not reach output lookup")

    report = ValidationService(definition, NeverExecute(), source_provider=NeverExecute()).run_suite(definition.cases)
    assert all(c.status == "TRANSLATION_FAILED" and c.failure_stage == "source_parse" for c in report.cases)
    assert all(c.target_result is None and c.comparison is None for c in report.cases)
    json_path = write_reports(report, tmp_path / "validation/report.json", case_file_path=path)
    payload = json.loads(json_path.read_text())
    assert payload["summary"]["total"] == 2
    assert payload["summary"]["outcomes"]["SQLGlot 转译失败"] == 2
    assert payload["queries"][0]["failure_stage"] == "source_parse"
    assert "Unexpected token" in json_path.read_text()
    assert sorted(p.name for p in json_path.parent.iterdir()) == ["report.json"]


def test_unsafe_ast_is_not_retained_as_parser_failure(tmp_path):
    source = tmp_path / "unsafe.sql"
    source.write_text("WITH x AS (DELETE FROM t RETURNING *) SELECT * FROM x; SELECT 1;")
    definition = import_case_file(source, tmp_path / "cases.yaml", _options())
    assert [c.sql for c in definition.cases] == ["SELECT 1;"]


@pytest.mark.parametrize("source_error", [False, True])
def test_parser_failure_reads_out_for_source_classification_without_executing_sql(tmp_path, source_error):
    from doris_sql_validator.case_loader import write_case_file
    from doris_sql_validator.reporting import load_validation_report, write_reports
    from doris_sql_validator.service import ValidationService

    sql = "SELECT DISTINCT ON (a) a FROM t ORDER BY a USING <;"
    source, output = tmp_path / "source.sql", tmp_path / "source.out"
    source.write_text(sql)
    output.write_text(sql + ("\nERROR: invalid argument\n" if source_error else "\n a\n---\n 1\n(1 row)\n"))
    path = tmp_path / "cases.yaml"
    definition = import_case_file(source, path, _options(recorded_output=output))
    write_case_file(definition, path)
    provider = RecordedOutputProvider(definition.recorded_output, base_dir=tmp_path, dialect="postgres")

    class NeverExecute:
        def execute_select(self, *args, **kwargs):
            pytest.fail("transpilation failure must never execute SQL")

    report = ValidationService(definition, NeverExecute(), source_provider=provider).run_suite(definition.cases)
    document = load_validation_report(write_reports(report, tmp_path / "validation/report.json", case_file_path=path))
    query = document["queries"][0]
    assert "Unexpected token" in query["transpilation_error"]
    assert report.cases[0].target_result is None
    assert report.cases[0].source_evidence.result.success is not source_error
    if source_error:
        assert query["result"] == "源端负向用例"
        assert query["action"] == "默认不归因"
        assert query["source_error"]["message"]
        assert document["summary"]["negative_source_cases"] == 1
        assert document["summary"]["needs_attribution"] == 0
    else:
        assert query["result"] == "SQLGlot 转译失败"
        assert query["action"] == "归因"
        assert document["summary"]["known_source_success"] == 1
        assert document["summary"]["needs_attribution"] == 1
        assert document["summary"]["successful_match_rate"]["denominator"] == 1


def test_raw_import_accepts_only_read_only_queries(tmp_path: Path) -> None:
    source = tmp_path / "sample.sql"
    source.write_text(
        "CREATE TABLE ignored (id INT);\n"
        "INSERT INTO ignored VALUES (1);\n"
        "SELECT 'a;b' AS value;\n",
        encoding="utf-8",
    )

    case_file = import_case_file(source, tmp_path / "cases.yaml", _options())

    assert case_file.validation_mode == "live_source"
    assert len(case_file.cases) == 1
    assert case_file.cases[0].sql == "SELECT 'a;b' AS value;"
    assert case_file.import_summary.accepted == 1
    assert case_file.import_summary.skipped == 2
    assert len(case_file.import_diagnostics) == 2
    assert case_file.input.sha256 is not None


def test_import_strips_leading_comments_from_case_sql(tmp_path: Path) -> None:
    source = tmp_path / "commented.sql"
    source.write_text(
        "-- suite heading\n/* case note */\nSELECT 1 AS value;\n",
        encoding="utf-8",
    )

    case_file = import_case_file(source, tmp_path / "cases.yaml", _options())

    assert case_file.cases[0].sql == "SELECT 1 AS value;"


def test_raw_import_does_not_persist_runtime_mode_or_comparison(tmp_path: Path) -> None:
    source = tmp_path / "sample.sql"
    source.write_text("SELECT 1 AS value;", encoding="utf-8")
    case_file = import_case_file(source, tmp_path / "cases.yaml", _options())

    payload = case_file.model_dump(mode="json", exclude_none=True)
    assert "mode" not in payload["source"]
    assert "comparison" not in payload["cases"][0]


def test_pg_recorded_import_and_provider(tmp_path: Path) -> None:
    source = tmp_path / "sample.sql"
    output = tmp_path / "sample.out"
    sql = "SELECT 1 AS value;"
    source.write_text(sql + "\n", encoding="utf-8")
    output.write_text(
        sql + "\n value\n-------\n     1\n(1 row)\n",
        encoding="utf-8",
    )
    case_path = tmp_path / "cases.yaml"

    case_file = import_case_file(source, case_path, _options(recorded_output=output))

    assert case_file.import_summary.accepted == 1
    assert case_file.validation_mode == "recorded_output"
    assert case_file.recorded_output is not None
    provider = RecordedOutputProvider(
        case_file.recorded_output,
        base_dir=case_path.parent,
        dialect="postgres",
    )
    evidence = provider.get_result(case_file.cases[0])
    assert evidence.result.success is True
    assert evidence.result.rows == [["1"]]
    assert evidence.capabilities.row_values == "display_text"
    assert "sha256" not in case_file.recorded_output.model_dump()
    assert "artifact_sha256" not in evidence.model_dump()


def test_recorded_output_can_remain_outside_generated_yaml_directory(tmp_path: Path) -> None:
    input_dir = tmp_path / "inputs" / "postgres"
    input_dir.mkdir(parents=True)
    source = input_dir / "queries.sql"
    output = input_dir / "queries.out"
    case_dir = tmp_path / "reports" / "data-preparation"
    source.write_text("SELECT 1;", encoding="utf-8")
    output.write_text("SELECT 1;\n ?column?\n----------\n        1\n(1 row)\n")

    original = output.read_bytes()
    definition = import_case_file(source, case_dir / "queries-001-cases.yaml", _options(recorded_output=output))
    assert (case_dir / definition.recorded_output.file).resolve() == output.resolve()
    assert definition.recorded_output.file.startswith("../")
    provider = RecordedOutputProvider(definition.recorded_output, base_dir=case_dir, dialect="postgres")
    assert provider.get_result(definition.cases[0]).result.rows == [["1"]]
    assert output.read_bytes() == original
    assert set(input_dir.iterdir()) == {source, output}

    output.write_text("SELECT 1;\n ?column?\n----------\n        2\n(1 row)\n", encoding="utf-8")
    current = RecordedOutputProvider(definition.recorded_output, base_dir=case_dir, dialect="postgres")
    assert current.get_result(definition.cases[0]).result.rows == [["2"]]


def test_pg_occurrences_use_echo_identity_not_ast_identity(tmp_path: Path) -> None:
    source, output = tmp_path / "source.sql", tmp_path / "source.out"
    statements = [
        "SELECT * FROM t x;", "SELECT * FROM t AS x;",
        "SELECT 1 AS value;", "SELECT 1 AS value;",
    ]
    source.write_text("\n".join(statements))
    output.write_text("".join(f"{sql}\n value\n-------\n {i}\n(1 row)\n" for i, sql in enumerate(statements)))
    definition = import_case_file(source, tmp_path / "cases.yaml", _options(recorded_output=output))
    assert definition.import_summary.errors == 0
    assert [c.output_occurrence for c in definition.cases] == [1, 1, 1, 2]
    provider = RecordedOutputProvider(definition.recorded_output, base_dir=tmp_path, dialect="postgres")
    assert [provider.get_result(c).result.rows for c in definition.cases] == [[["0"]], [["1"]], [["2"]], [["3"]]]


def test_pg_blank_layout_lines_share_occurrence_counter(tmp_path: Path) -> None:
    source, output = tmp_path / "source.sql", tmp_path / "source.out"
    source.write_text("SELECT\n\n 1 AS value;\nSELECT\n 1 AS value;")
    output.write_text("SELECT\n 1 AS value;\n value\n-------\n 1\n(1 row)\nSELECT\n\n 1 AS value;\n value\n-------\n 2\n(1 row)\n")
    definition = import_case_file(source, tmp_path / "cases.yaml", _options(recorded_output=output))
    assert [c.output_occurrence for c in definition.cases] == [1, 2]
    provider = RecordedOutputProvider(definition.recorded_output, base_dir=tmp_path, dialect="postgres")
    assert provider.get_result(definition.cases[1]).result.rows == [["2"]]


def test_pg_importer_and_provider_read_expanded_and_multiline_results(tmp_path: Path) -> None:
    source, output = tmp_path / "source.sql", tmp_path / "source.out"
    sql = "SELECT v FROM t;"
    source.write_text(f"CREATE TABLE t(v TEXT);\n{sql}\n{sql}\n", encoding="utf-8")
    output.write_text(
        "CREATE TABLE t(v TEXT);\n"
        + sql + "\n-[ RECORD 1 ]\nv | first\n\n"
        + sql + "\n v\n-------\n next +\n line\n(1 row)\n",
        encoding="utf-8",
    )
    definition = import_case_file(source, tmp_path / "cases.yaml", _options(recorded_output=output))
    assert definition.import_summary.accepted == 2
    assert definition.import_summary.skipped == 1
    assert definition.import_summary.errors == 0
    assert [c.output_occurrence for c in definition.cases] == [1, 2]
    provider = RecordedOutputProvider(definition.recorded_output, base_dir=tmp_path, dialect="postgres")
    assert [provider.get_result(case).result.rows for case in definition.cases] == [
        [["first"]], [["next\nline"]],
    ]


def test_pg_importer_repeated_queries_ignore_prepare_explain_and_prefixes(tmp_path: Path) -> None:
    source, output = tmp_path / "source.sql", tmp_path / "source.out"
    source.write_text(
        "PREPARE p AS\nSELECT v FROM t;\nEXECUTE p;\n"
        "EXPLAIN (COSTS OFF)\nSELECT v FROM t;\n"
        "SELECT v FROM t\nWHERE v = 2;\n"
        "SELECT v FROM t;\nSELECT v FROM t;\n", encoding="utf-8",
    )
    output.write_text(
        "PREPARE p AS\nSELECT v FROM t;\nEXECUTE p;\n v\n---\n 8\n(1 row)\n"
        "EXPLAIN (COSTS OFF)\nSELECT v FROM t;\n QUERY PLAN\n------------\n Seq Scan\n(1 row)\n"
        "SELECT v FROM t\nWHERE v = 2;\n v\n---\n 2\n(1 row)\n"
        "SELECT v FROM t;\n v\n---\n 1\n(1 row)\n"
        "SELECT v FROM t;\n v\n---\n 3\n(1 row)\n", encoding="utf-8",
    )
    definition = import_case_file(source, tmp_path / "cases.yaml", _options(recorded_output=output))
    assert definition.import_summary.accepted == 3
    assert not [d for d in definition.import_diagnostics if d.statement_type == "recorded_output"]
    assert [c.output_occurrence for c in definition.cases] == [1, 1, 2]
    provider = RecordedOutputProvider(definition.recorded_output, base_dir=tmp_path, dialect="postgres")
    assert [provider.get_result(c).result.rows for c in definition.cases] == [
        [["2"]], [["1"]], [["3"]],
    ]
