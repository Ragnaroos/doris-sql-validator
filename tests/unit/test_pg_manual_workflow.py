"""Offline import, single-file validation and direct diagnostic probes."""
import json

import pytest
from typer.testing import CliRunner

from doris_sql_validator.cli import app
from doris_sql_validator.case_loader import load_case_file
from doris_sql_validator.models import QueryColumn, QueryResult
from doris_sql_validator.reporting import load_validation_report, validate_report_inputs
from doris_sql_validator.pg_probe import (
    compare_probe, execute_query, probe_postgres_case, probe_postgres_cases,
    render_probe_batch_markdown, summarize_probe,
)


@pytest.fixture(params=[False, True], ids=["yaml-with-input", "yaml-in-report-directory"])
def first_round(tmp_path, monkeypatch, request):
    sql = tmp_path / "source.sql"
    sql.write_text("CREATE TABLE orders(amount INT);\nINSERT INTO orders VALUES (1),(2);\nSELECT SUM(amount) AS total FROM orders;\nSELECT 5 / 2 AS value;\nSELECT 1 / 0;\n")
    out = tmp_path / "expected.out"
    out.write_text("SELECT SUM(amount) AS total FROM orders;\n total\n-------\n 3\n(1 row)\nSELECT 5 / 2 AS value;\n value\n-------\n 2\n(1 row)\nSELECT 1 / 0;\nERROR: division by zero\n")
    calls = []

    class Adapter:
        def execute_select(self, sql, *, database=None):
            calls.append(sql)
            assert sql.upper().startswith("SELECT")
            if "SUM" in sql:
                return QueryResult(engine="doris", success=True, columns=[QueryColumn(name="total", canonical_type="integer")], rows=[[3]])
            if "5 / 2" in sql:
                return QueryResult(engine="doris", success=True, columns=[QueryColumn(name="value", canonical_type="float")], rows=[[2.5]])
            return QueryResult(engine="doris", success=True, columns=[QueryColumn(name="value")], rows=[[None]])

    engines = []
    def create(engine):
        engines.append(engine)
        assert engine == "doris", "Recorded Output must never create a PG adapter"
        return Adapter()
    monkeypatch.setattr("doris_sql_validator.cli.create_adapter", create)
    runner = CliRunner()
    case_path = (
        tmp_path / "reports/data-preparation/queries-001-cases.yaml"
        if request.param else tmp_path / "cases.yaml"
    )
    imported = runner.invoke(app, ["import-cases", "--format", "pg-regress", "--dialect", "postgres", "--input", str(sql), "--recorded-output", str(out), "--source-database", "pg_test", "--target-database", "doris_test", "--output", str(case_path)])
    assert imported.exit_code == 0, imported.output
    run = runner.invoke(app, ["run", "--path", str(case_path), "--output", str(tmp_path / "reports/validation/queries-001-validation.json")])
    assert run.exit_code == 1, run.output
    report_path = tmp_path / "reports/validation/queries-001-validation.json"
    report = json.loads(report_path.read_text())
    assert engines == ["doris"]
    assert len(calls) == 3
    assert report["summary"]["successful_matches"] == 1
    assert report["summary"]["negative_source_cases"] == 1
    assert report["summary"]["total"] == 3
    assert report["summary"]["successful_match_rate"]["value"] == .5
    assert report["summary"]["import"]["skipped"] == 2
    assert "sha256" not in report["run"]["recorded_output"]
    assert "sha256" not in load_case_file(case_path).definition.recorded_output.model_dump()
    return tmp_path, case_path, report_path, sql, out


def test_dropped_output_lookup_failure_reaches_single_report(tmp_path, monkeypatch):
    sql, out, cases = tmp_path / "source.sql", tmp_path / "expected.out", tmp_path / "cases.yaml"
    sql.write_text("SELECT 1 AS value;\nSELECT 2 AS value;\n")
    out.write_text("SELECT 1 AS value;\n value\n-------\n 1\n(1 row)\n")

    class Adapter:
        def execute_select(self, sql, *, database=None):
            assert "2" not in sql, "output lookup failure must not execute rejected query"
            return QueryResult(engine="doris", success=True,
                columns=[QueryColumn(name="value", canonical_type="integer")], rows=[[1]])

    monkeypatch.setattr("doris_sql_validator.cli.create_adapter", lambda engine: Adapter())
    runner = CliRunner()
    imported = runner.invoke(app, ["import-cases", "--format", "pg-regress", "--dialect", "postgres",
        "--input", str(sql), "--recorded-output", str(out), "--output", str(cases)])
    assert imported.exit_code == 0, imported.output
    assert len(load_case_file(cases).definition.cases) == 1
    directory = tmp_path / "validation"
    run = runner.invoke(app, ["run", "--path", str(cases), "--output", str(directory / "queries-001-validation.json")])
    assert run.exit_code == 1, run.output
    assert sorted(p.name for p in directory.iterdir()) == ["queries-001-validation.json"]
    assert "Markdown:" not in run.output
    path = directory / "queries-001-validation.json"
    report = json.loads(path.read_text())
    assert report["summary"]["total"] == 2
    assert report["summary"]["processed_queries"] == 1
    assert report["summary"]["successful_matches"] == 1
    assert report["queries"][1]["result"] == "导入时参考输出读取失败"

    validate_report_inputs(report, load_case_file(cases))


def test_direct_report_checks_do_not_generate_an_entry_directory(first_round):
    root, cases, report_path, _, _ = first_round
    validate_report_inputs(load_validation_report(report_path), load_case_file(cases))
    assert sorted(p.name for p in report_path.parent.iterdir()) == ["queries-001-validation.json"]
    assert not list(root.rglob("HANDOFF.md"))
    assert not list(root.rglob("evidence-index.json"))


def test_direct_report_checks_reject_changed_yaml(first_round):
    _, cases, report_path, _, _ = first_round
    cases.write_text(cases.read_text() + "\n")
    with pytest.raises(ValueError, match="YAML.*修改"):
        validate_report_inputs(load_validation_report(report_path), load_case_file(cases))


def test_direct_report_checks_reject_changed_source_sql(first_round):
    _, cases, report_path, sql, _ = first_round
    sql.write_text(sql.read_text() + "SELECT 9;\n")
    with pytest.raises(ValueError, match="SQL.*改变"):
        validate_report_inputs(load_validation_report(report_path), load_case_file(cases))


def test_direct_report_checks_do_not_hash_output(first_round):
    _, cases, report_path, _, out = first_round
    out.write_text(out.read_text().replace(" 3\n(1 row)", " 4\n(1 row)"))
    validate_report_inputs(load_validation_report(report_path), load_case_file(cases))


def test_rerun_uses_current_output_without_reimport_or_fingerprint_gate(first_round):
    root, cases, _, _, out = first_round
    out.write_text(out.read_text().replace(" 3\n(1 row)", " 4\n(1 row)"))
    path = root / "reports/validation/queries-001-validation-rerun.json"
    run = CliRunner().invoke(app, ["run", "--path", str(cases), "--output", str(path)])
    assert run.exit_code == 1, run.output
    document = load_validation_report(path)
    assert document["queries"][0]["result"] == "行值或顺序不匹配"
    assert document["queries"][0]["difference"]["source_only"] == [{"row": ["4"], "extra_count": 1}]


def test_run_defaults_to_parallel_validation_directory(first_round, monkeypatch):
    root, cases, _, _, _ = first_round
    monkeypatch.setattr("doris_sql_validator.cli.PROJECT_DIR", root)
    run = CliRunner().invoke(app, ["run", "--path", str(cases)])
    assert run.exit_code == 1, run.output
    stem = cases.stem.removesuffix("-cases")
    path = root / "reports/validation" / f"{stem}-validation.json"
    assert path.is_file()
    assert str(path) in run.output


def test_run_stdout_returns_same_report_without_writing_files(first_round, monkeypatch):
    root, cases, report_path, _, _ = first_round
    existing = {p.relative_to(root): p.read_bytes() for p in root.rglob("*") if p.is_file()}
    monkeypatch.setattr("doris_sql_validator.cli.PROJECT_DIR", root / "unused-project")
    monkeypatch.setattr("doris_sql_validator.cli.write_reports", lambda *a, **kw: pytest.fail("must not write report"))
    run = CliRunner().invoke(app, ["run", "--path", str(cases), "--stdout"])
    assert run.exit_code == 1, run.output
    document, saved = json.loads(run.output), load_validation_report(report_path)
    assert set(document) == {"run", "summary", "queries"}
    assert document["summary"] == saved["summary"]
    assert document["queries"] == saved["queries"]
    for field in ("case_file", "input", "recorded_output", "comparison_rules", "sqlglot_version"):
        assert document["run"][field] == saved["run"][field]
    assert document["summary"]["negative_source_cases"] == 1
    assert {p.relative_to(root): p.read_bytes() for p in root.rglob("*") if p.is_file()} == existing
    assert not (root / "unused-project").exists()


def test_run_stdout_successfully_filters_one_matching_query(first_round, monkeypatch):
    _, cases, report_path, _, _ = first_round
    case_id = load_validation_report(report_path)["queries"][0]["id"]
    monkeypatch.setattr("doris_sql_validator.cli.write_reports", lambda *a, **kw: pytest.fail("must not write report"))
    run = CliRunner().invoke(app, ["run", "--path", str(cases), "--id", case_id, "--stdout"])
    assert run.exit_code == 0, run.output
    document = json.loads(run.output)
    assert document["run"]["filtered"] is True
    assert document["summary"]["total"] == document["summary"]["successful_matches"] == 1
    assert document["queries"] == [load_validation_report(report_path)["queries"][0]]


def test_run_rejects_stdout_and_output_before_execution(first_round, monkeypatch):
    root, cases, _, _, _ = first_round
    output = root / "must-not-exist/report.json"
    monkeypatch.setattr("doris_sql_validator.cli.create_adapter", lambda *a: pytest.fail("must not create adapter"))
    run = CliRunner().invoke(app, ["run", "--path", str(cases), "--stdout", "--output", str(output)])
    assert run.exit_code == 2, run.output
    assert "不能同时使用" in run.output
    assert not output.parent.exists()


@pytest.mark.parametrize("input_index", [1, 3, 4], ids=["yaml", "source-sql", "recorded-output"])
def test_report_output_cannot_overwrite_inputs(first_round, monkeypatch, input_index):
    _, cases, _, _, _ = first_round
    path = first_round[input_index]
    before = path.read_bytes()
    monkeypatch.setattr("doris_sql_validator.cli.create_adapter", lambda *args: pytest.fail("must not create adapter"))
    run = CliRunner().invoke(app, ["run", "--path", str(cases), "--output", str(path)])
    assert run.exit_code == 2, run.output
    assert "不能覆盖" in run.output
    assert path.read_bytes() == before


def test_probe_rejects_report_yaml_mismatch_before_database_execution(first_round, monkeypatch):
    root, cases, report_path, _, _ = first_round
    document = load_validation_report(report_path)
    document["run"]["target"]["database"] = "another_database"
    report_path.write_text(json.dumps(document))
    candidate = "SELECT 5 DIV 2 AS value"
    monkeypatch.setattr("doris_sql_validator.pg_probe.execute_query", lambda *a, **kw: pytest.fail("must not execute"))
    with pytest.raises(ValueError, match="目标数据库配置"):
        probe_postgres_case(cases, report_path, document["queries"][1]["id"], candidate)
    assert not (root / "probe").exists()


def test_removed_review_command_is_not_registered():
    result = CliRunner().invoke(app, ["--help"])
    assert result.exit_code == 0
    assert "prepare-pg-review" not in result.output


def result(native, rows):
    return {"成功": True, "字段": [{"名称": "value", "原生类型": native, "精度": None, "小数位数": None}], "记录": rows, "错误": None}


def test_probe_values_continue_after_type_difference():
    c = compare_probe(result("numeric", [[{"十进制数": "1"}]]), result("double", [[2.0]]), "SELECT 1 AS value")
    assert c["字段类型"][0]["逻辑类型"] == "不同"
    assert c["记录值及重复次数"] == "不同"
    assert c["字段类型"][0]["精度与小数位"] == "信息不足"


def test_probe_unknown_types_are_not_passed():
    c = compare_probe(result("int4", [[1]]), result(None, [[1]]), "SELECT 1")
    assert c["字段类型"][0]["逻辑类型"] == "信息不足"
    assert c["记录值及重复次数"] == "一致"


def test_probe_decimal_tail_zeros_equal_but_type_domain_not_erased():
    c = compare_probe(result("numeric", [[{"十进制数": "0"}]]), result("decimalv3(21,1)", [[{"十进制数": "0.0"}]]), "SELECT 0")
    assert c["记录值及重复次数"] == "一致"
    assert c["字段类型"][0]["类型声明"] == "不同"


def test_probe_high_precision_differences_are_not_rounded_by_python_decimal_context():
    c = compare_probe(result("numeric", [[{"十进制数": "12345678901234567890123456789012345671"}]]),
        result("decimalv3(38,0)", [[{"十进制数": "12345678901234567890123456789012345672"}]]), "SELECT 1")
    assert c["记录值及重复次数"] == "不同"


def test_probe_boolean_wire_integer_uses_native_type_evidence():
    c = compare_probe(result("bool", [[True]]), result("boolean", [[1]]), "SELECT TRUE")
    assert c["记录值及重复次数"] == "一致"


def test_probe_json_text_identical_content_is_not_a_false_value_difference():
    c = compare_probe(result("text", [['{"a":1}']]), result("json", [['{"a":1}']]), "SELECT 'x'")
    assert c["字段类型"][0]["逻辑类型"] == "不同"
    assert c["记录值及重复次数"] == "一致"
    different_text = compare_probe(result("text", [['{"a":1}']]), result("json", [['{ "a": 1 }']]), "SELECT 'x'")
    assert different_text["记录值及重复次数"] == "不同"


def test_probe_json_null_and_sql_null_are_distinct():
    c = compare_probe(result("jsonb", [[None]]), result("json", [["null"]]), "SELECT NULL")
    assert c["记录值及重复次数"] == "不同"


def test_probe_numeric_array_pack_does_not_introduce_a_driver_difference():
    c = compare_probe(result("_numeric", [[[{"十进制数": "1.00"}, None]]]),
        result("array<decimalv3(4,2)>", [['[1.00,null]']]), "SELECT ARRAY[1.00,NULL]")
    assert c["记录值及重复次数"] == "一致"


def test_probe_order_and_duplicate_counts_are_separate():
    c = compare_probe(result("int4", [[1], [1], [2]]), result("int", [[2], [1], [1]]), "SELECT 1 ORDER BY 1")
    assert c["记录值及重复次数"] == "一致"
    assert c["最终行顺序"].startswith("不同")
    c = compare_probe(result("int4", [[1], [1], [2]]), result("int", [[2], [2], [1]]), "SELECT 1")
    assert c["记录值及重复次数"] == "不同"


@pytest.mark.parametrize("sql", ["CREATE TABLE bad(i INT)", "SELECT 1; DROP TABLE bad", "SELECT * INTO bad FROM good", "SELECT * FROM t FOR UPDATE"])
def test_probe_rejects_writes_or_locks_before_connect(sql, monkeypatch):
    monkeypatch.setattr("doris_sql_validator.pg_probe.PostgresAdapter.connect", lambda *a, **kw: pytest.fail("must not connect"))
    with pytest.raises(ValueError): execute_query("postgres", sql, "test")


def test_probe_explicit_candidate_and_boundary_return_facts_without_files(first_round, monkeypatch):
    root, cases, report_path, _, _ = first_round
    report = json.loads(report_path.read_text())
    case = report["queries"][1]
    original_report = report_path.read_text()
    candidate = "SELECT 5 DIV 2 AS value"
    calls = []
    def execute(engine, sql, database, **kwargs):
        calls.append((engine, sql, database))
        if engine == "postgres": return result("int4", [[2]])
        return result("int", [[2]]) if "DIV" in sql else result("double", [[2.5]])
    monkeypatch.setattr("doris_sql_validator.pg_probe.execute_query", execute)
    before = {p.relative_to(root) for p in root.rglob("*")}
    evidence = probe_postgres_case(cases, report_path, case["id"], candidate)
    assert len(calls) == 5
    assert evidence["候选与社区输出相同"] is False
    assert evidence["独立候选比较"]["记录值及重复次数"] == "一致"
    assert evidence["社区输出比较"]["记录值及重复次数"] == "不同"
    assert evidence["社区输出比较"]["行值反例"]["Doris多出"][0]["记录"] == [2.5]
    assert evidence["是否边界变体"] is False
    assert evidence["独立Doris实际结果"]["记录"] == [[2]]
    evidence = probe_postgres_case(
        cases, report_path, case["id"], "SELECT CAST(NULL AS INT) AS value",
        source_variant_sql="SELECT NULL::int AS value",
    )
    assert evidence["是否边界变体"] is True
    assert "历史输出参考" not in evidence
    assert "社区Doris实际结果" not in evidence
    assert {p.relative_to(root) for p in root.rglob("*")} == before
    assert report_path.read_text() == original_report


@pytest.mark.parametrize("sql", [
    "CREATE TABLE bad(i INT)", "SELECT 1; DROP TABLE bad",
    "SELECT * INTO bad FROM good", "SELECT * FROM t FOR UPDATE",
])
def test_probe_rejects_unsafe_candidate_before_any_execution(first_round, monkeypatch, sql):
    _, cases, report_path, _, _ = first_round
    case_id = load_validation_report(report_path)["queries"][1]["id"]
    monkeypatch.setattr("doris_sql_validator.pg_probe.execute_query", lambda *a, **kw: pytest.fail("must not execute"))
    with pytest.raises(ValueError):
        probe_postgres_case(cases, report_path, case_id, sql)


@pytest.mark.parametrize("stdin", [False, True], ids=["inline-sql", "stdin-sql"])
def test_probe_cli_returns_json_without_creating_files(first_round, monkeypatch, stdin):
    root, cases, report_path, _, _ = first_round
    case_id = load_validation_report(report_path)["queries"][1]["id"]
    candidate = "SELECT 5 DIV 2 AS value"
    calls = []
    def execute(engine, sql, database, **kwargs):
        calls.append((engine, sql))
        return result("int4" if engine == "postgres" else "int", [[2]])
    monkeypatch.setattr("doris_sql_validator.pg_probe.execute_query", execute)
    before = {p.relative_to(root) for p in root.rglob("*")}
    command = CliRunner().invoke(app, [
        "probe-pg-case", "--path", str(cases), "--report", str(report_path),
        "--case-id", case_id, "--candidate-sql", "-" if stdin else candidate,
    ], input=candidate if stdin else None)
    assert command.exit_code == 0, command.output
    document = json.loads(command.output)
    assert document["独立DorisSQL"] == candidate
    assert document["独立Doris实际结果"]["行数"] == 1
    assert document["独立Doris实际结果"]["记录样本"] == [[2]]
    assert "记录" not in document["独立Doris实际结果"]
    assert len(calls) == 5
    assert {p.relative_to(root) for p in root.rglob("*")} == before


def test_probe_compact_output_is_derived_after_full_result_comparison():
    source = result("int4", [[i] for i in range(20)])
    target = result("int", [[i] for i in range(19)] + [[99]])
    record = {"PostgreSQL实际结果": source, "独立Doris实际结果": target,
        "独立候选比较": compare_probe(source, target, "SELECT value FROM t ORDER BY value")}
    compact = summarize_probe(record)
    assert compact["独立Doris实际结果"]["行数"] == 20
    assert len(compact["独立Doris实际结果"]["记录样本"]) == 3
    assert compact["独立Doris实际结果"]["未展示行数"] == 17
    comparison = compact["独立候选比较"]
    assert comparison["行值反例"]["PostgreSQL多出"] == [{"记录": [19], "多出次数": 1}]
    assert comparison["行值反例"]["Doris多出"] == [{"记录": [99], "多出次数": 1}]
    assert comparison["顺序反例"] == [{"行号": 20, "PostgreSQL": [19], "Doris": [99]}]
    assert len(source["记录"]) == len(target["记录"]) == 20


def test_probe_compact_output_preserves_errors_and_does_not_claim_zero_rows():
    failure = {"成功": False, "字段": [], "记录": [], "错误": {"原文": "permission denied"}}
    compact = summarize_probe({"独立Doris实际结果": failure})
    assert compact["独立Doris实际结果"]["错误"]["原文"] == "permission denied"
    assert compact["独立Doris实际结果"]["行数"] is None


def test_probe_cli_accepts_source_variant_text_without_using_historical_output(first_round, monkeypatch):
    root, cases, report_path, _, _ = first_round
    case_id = load_validation_report(report_path)["queries"][1]["id"]
    source_sql, candidate_sql = "SELECT NULL::int AS value", "SELECT CAST(NULL AS INT) AS value"
    calls = []
    def execute(engine, sql, database, **kwargs):
        calls.append((engine, sql))
        return result("int4" if engine == "postgres" else "int", [[None]])
    monkeypatch.setattr("doris_sql_validator.pg_probe.execute_query", execute)
    before = {p.relative_to(root) for p in root.rglob("*")}
    command = CliRunner().invoke(app, ["probe-pg-case", "--path", str(cases), "--report", str(report_path),
        "--case-id", case_id, "--candidate-sql", candidate_sql, "--source-variant-sql", source_sql])
    assert command.exit_code == 0, command.output
    document = json.loads(command.output)
    assert document["是否边界变体"] is True
    assert document["源SQL"] == source_sql
    assert "历史输出参考" not in document
    assert "社区Doris实际结果" not in document
    assert calls == [("postgres", source_sql), ("doris", candidate_sql)] * 2
    assert {p.relative_to(root) for p in root.rglob("*")} == before


def test_probe_cli_reports_invalid_sql_before_database_execution(first_round, monkeypatch):
    _, cases, report_path, _, _ = first_round
    case_id = load_validation_report(report_path)["queries"][1]["id"]
    monkeypatch.setattr("doris_sql_validator.pg_probe.execute_query", lambda *a, **kw: pytest.fail("must not execute"))
    command = CliRunner().invoke(app, ["probe-pg-case", "--path", str(cases), "--report", str(report_path),
        "--case-id", case_id, "--candidate-sql", "SELECT ("])
    assert command.exit_code == 2, command.output
    assert command.output


def test_probe_difference_examples_keep_duplicate_counts_and_bound_output():
    source = result("int4", [[1], [1]] + [[i] for i in range(2, 9)])
    target = result("int", [[1], [2]] + [[i] for i in range(12, 19)])
    comparison = compare_probe(source, target, "SELECT value FROM t")
    examples = comparison["行值反例"]
    assert examples["PostgreSQL多出"][0] == {"记录": [1], "多出次数": 1}
    assert len(examples["PostgreSQL多出"]) == len(examples["Doris多出"]) == 3
    assert examples["未展示的不同记录种类"] > 0


def test_batch_reuses_materials_but_not_database_results(first_round, monkeypatch):
    import doris_sql_validator.pg_probe as probe

    root, cases, report_path, _, _ = first_round
    case_id = load_validation_report(report_path)["queries"][1]["id"]
    counts = {"yaml": 0, "report": 0, "validate": 0, "out": 0}
    for name, key in (("load_case_file", "yaml"), ("load_validation_report", "report"),
                      ("validate_report_inputs", "validate"), ("RecordedOutputProvider", "out")):
        original = getattr(probe, name)
        def counted(*args, _original=original, _key=key, **kwargs):
            counts[_key] += 1
            return _original(*args, **kwargs)
        monkeypatch.setattr(probe, name, counted)
    calls = []
    def execute(engine, sql, database, **kwargs):
        calls.append((engine, sql, database))
        assert database == ("pg_test" if engine == "postgres" else "doris_test")
        return result("int4" if engine == "postgres" else "int", [[2]])
    monkeypatch.setattr(probe, "execute_query", execute)
    before = {p.relative_to(root): p.read_bytes() for p in root.rglob("*") if p.is_file()}
    requests = [{"case_id": case_id, "candidate_sql": "SELECT 5 DIV 2 AS value"}] * 2
    requests += [{"case_id": case_id, "candidate_sql": "SELECT CAST(NULL AS INT) AS value", "source_variant_sql": "SELECT NULL::int AS value"}]
    batch = probe_postgres_cases(cases, report_path, requests)
    assert counts == {"yaml": 1, "report": 1, "validate": 1, "out": 1}
    assert len(calls) == 14  # 5 + 5 + 4, including repeat checks each time
    assert batch["批次统计"]["请求总数"] == batch["批次统计"]["完成对照请求数"] == 3
    assert batch["批次统计"]["边界变体请求数"] == 1
    assert [a["请求序号"] for a in batch["逐条请求"]] == [1, 2, 3]
    assert "历史输出参考" not in batch["逐条请求"][2]["事实"]
    assert {p.relative_to(root): p.read_bytes() for p in root.rglob("*") if p.is_file()} == before


@pytest.mark.parametrize("bad_request", [
    {},
    {"case_id": "unknown", "candidate_sql": "SELECT 1"},
    {"candidate_sql": "SELECT 1; DROP TABLE orders"},
    {"candidate_sql": "SELECT 1", "source_variant_sql": "DELETE FROM orders"},
    {"candidate_sql": "SELECT 1", "database": "wrong-stage"},
    {"candidate_sql": 123},
    None,
])
def test_batch_bad_request_never_executes_and_does_not_block_next(first_round, monkeypatch, bad_request):
    _, cases, report_path, _, _ = first_round
    case_id = load_validation_report(report_path)["queries"][1]["id"]
    bad = {"case_id": case_id, **bad_request} if isinstance(bad_request, dict) else bad_request
    if isinstance(bad_request, dict) and "candidate_sql" not in bad_request:
        bad.pop("candidate_sql", None)
    calls = []
    def execute(engine, sql, database, **kwargs):
        calls.append((engine, sql))
        return result("int4" if engine == "postgres" else "int", [[2]])
    monkeypatch.setattr("doris_sql_validator.pg_probe.execute_query", execute)
    batch = probe_postgres_cases(cases, report_path, [bad, {"case_id": case_id, "candidate_sql": "SELECT 5 DIV 2 AS value"}])
    assert [a["处理状态"] for a in batch["逐条请求"]] == ["未执行", "已完成"]
    assert batch["逐条请求"][0]["错误"]["原文"]
    assert len(calls) == 5
    assert batch["批次统计"]["未执行请求数"] == 1


def test_batch_database_error_is_observed_not_a_successful_match(first_round, monkeypatch):
    _, cases, report_path, _, _ = first_round
    case_id = load_validation_report(report_path)["queries"][1]["id"]
    def execute(engine, sql, database, **kwargs):
        if "no_such_function" in sql:
            return {"成功": False, "字段": [], "记录": [], "错误": {"原文": "No matching function: no_such_function"}}
        return result("int4" if engine == "postgres" else "int", [[2]])
    monkeypatch.setattr("doris_sql_validator.pg_probe.execute_query", execute)
    batch = probe_postgres_cases(cases, report_path, [
        {"case_id": case_id, "candidate_sql": "SELECT no_such_function(1)"},
        {"case_id": case_id, "candidate_sql": "SELECT 2 AS value"},
    ])
    assert batch["批次统计"]["完成对照请求数"] == 2
    observations = batch["批次统计"]["完成请求的候选观察（可重叠）"]
    assert observations["候选执行失败"] == observations["行值及重复次数一致"] == 1
    assert observations["行值未比较或无法归一化"] == 1
    facts = dict(batch["逐条请求"][0]["事实"])
    assert facts["独立Doris实际结果"]["行数"] is None
    assert "No matching function" in facts["独立Doris实际结果"]["错误"]["原文"]


def test_batch_tool_failure_keeps_partial_facts_and_continues(first_round, monkeypatch):
    import doris_sql_validator.pg_probe as probe
    _, cases, report_path, _, _ = first_round
    case_id = load_validation_report(report_path)["queries"][1]["id"]
    monkeypatch.setattr(probe, "execute_query", lambda engine, *a, **kw: result("int4" if engine == "postgres" else "int", [[2]]))
    original = probe.compare_probe
    def compare(source, target, source_sql):
        if source_sql == "SELECT 99":
            raise TypeError("comparison failed")
        return original(source, target, source_sql)
    monkeypatch.setattr(probe, "compare_probe", compare)
    batch = probe_postgres_cases(cases, report_path, [
        {"case_id": case_id, "candidate_sql": "SELECT 99", "source_variant_sql": "SELECT 99"},
        {"case_id": case_id, "candidate_sql": "SELECT 2 AS value"},
    ])
    assert batch["批次统计"]["工具处理失败请求数"] == 1
    failed, completed = batch["逐条请求"]
    assert failed["处理状态"] == "工具处理失败"
    assert failed["事实"]["PostgreSQL实际结果"]["记录样本"] == [[2]]
    assert failed["事实"]["独立Doris实际结果"]["记录样本"] == [[2]]
    assert completed["处理状态"] == "已完成"


@pytest.mark.parametrize("payload", ["{}", "[]", "not-json"])
def test_batch_cli_bad_envelope_connects_to_neither_database(first_round, monkeypatch, payload):
    _, cases, report_path, _, _ = first_round
    monkeypatch.setattr("doris_sql_validator.pg_probe.execute_query", lambda *a, **kw: pytest.fail("must not execute"))
    command = CliRunner().invoke(app, ["probe-pg-batch", "--path", str(cases), "--report", str(report_path), "--candidates-json", payload])
    assert command.exit_code == 2


@pytest.mark.parametrize("output_format", ["json", "markdown"])
def test_batch_cli_fact_rendering_without_files(first_round, monkeypatch, output_format):
    root, cases, report_path, _, _ = first_round
    case_id = load_validation_report(report_path)["queries"][1]["id"]
    calls = []
    def execute(engine, sql, database, **kwargs):
        calls.append(sql)
        return result("int4" if engine == "postgres" else "bigint", [[i] for i in range(20)])
    monkeypatch.setattr("doris_sql_validator.pg_probe.execute_query", execute)
    before = {p.relative_to(root): p.read_bytes() for p in root.rglob("*") if p.is_file()}
    command = CliRunner().invoke(app, ["probe-pg-batch", "--path", str(cases), "--report", str(report_path),
        "--candidates-json", "-", "--output-format", output_format], input=json.dumps([
            {"case_id": case_id, "candidate_sql": "SELECT 1; DELETE FROM orders"},
            {"case_id": case_id, "candidate_sql": "SELECT 5 DIV 2 AS value"},
        ]))
    assert command.exit_code == 1, command.output
    assert len(calls) == 5
    if output_format == "json":
        batch = json.loads(command.output)
        assert batch["批次统计"]["完成请求的候选观察（可重叠）"]["类型不同、信息不足或未比较"] == 1
        assert batch["逐条请求"][1]["事实"]["独立Doris实际结果"]["未展示行数"] == 17
    else:
        assert case_id in command.output
        assert "SELECT 5 DIV 2 AS value" in command.output
        assert "int4" in command.output and "bigint" in command.output
        assert "类型声明" in command.output and "不同" in command.output
        assert "源SQL" in command.output and "未执行" in command.output
    assert {p.relative_to(root): p.read_bytes() for p in root.rglob("*") if p.is_file()} == before


def test_batch_checks_material_identity_before_any_execution(first_round, monkeypatch):
    _, cases, report_path, _, _ = first_round
    case_id = load_validation_report(report_path)["queries"][1]["id"]
    cases.write_text(cases.read_text() + "\n")
    monkeypatch.setattr("doris_sql_validator.pg_probe.execute_query", lambda *a, **kw: pytest.fail("must not execute"))
    with pytest.raises(ValueError, match="YAML.*修改"):
        probe_postgres_cases(cases, report_path, [{"case_id": case_id, "candidate_sql": "SELECT 2"}])


def test_batch_and_single_probe_keep_identical_comparison_facts(first_round, monkeypatch):
    _, cases, report_path, _, _ = first_round
    case_id = load_validation_report(report_path)["queries"][1]["id"]
    def execute(engine, sql, database, **kwargs):
        rows = [[1], [1], [2], [3]] if engine == "postgres" else [[1], [2], [2], [4]]
        return result("int4" if engine == "postgres" else None, rows)
    monkeypatch.setattr("doris_sql_validator.pg_probe.execute_query", execute)
    request = {"case_id": case_id, "candidate_sql": "SELECT value FROM t ORDER BY value",
               "source_variant_sql": "SELECT value FROM t ORDER BY value"}
    single = summarize_probe(probe_postgres_case(cases, report_path, **request))
    batch = probe_postgres_cases(cases, report_path, [request])
    facts = dict(batch["逐条请求"][0]["事实"])
    single.pop("执行时间")
    facts.pop("执行时间")
    assert facts == single
    checks = facts["独立候选比较"]
    assert checks["字段类型"][0]["逻辑类型"] == "信息不足"
    assert checks["行值反例"]["PostgreSQL多出"][0] == {"记录": [1], "多出次数": 1}
    assert checks["最终行顺序"].startswith("不同")
    markdown = render_probe_batch_markdown(batch)
    assert "行值反例" in markdown and "顺序反例" in markdown


def test_batch_output_lookup_failure_never_executes_that_request(first_round, monkeypatch):
    _, cases, report_path, _, out = first_round
    case_id = load_validation_report(report_path)["queries"][1]["id"]
    out.write_text("SELECT 99;\n ?column?\n----------\n 99\n(1 row)\n")
    calls = []
    def execute(engine, sql, database, **kwargs):
        calls.append(sql)
        return result("int4" if engine == "postgres" else "int", [[2]])
    monkeypatch.setattr("doris_sql_validator.pg_probe.execute_query", execute)
    batch = probe_postgres_cases(cases, report_path, [
        {"case_id": case_id, "candidate_sql": "SELECT 2 AS value"},
        {"case_id": case_id, "candidate_sql": "SELECT 2 AS value", "source_variant_sql": "SELECT 2 AS value"},
    ])
    assert batch["逐条请求"][0]["处理状态"] == "未执行"
    assert batch["逐条请求"][0]["错误"]["异常类"] == "SourceEvidenceError"
    assert batch["逐条请求"][1]["处理状态"] == "已完成"
    assert len(calls) == 4


def test_batch_unsafe_historical_target_rejected_before_source_connection(first_round, monkeypatch):
    _, cases, report_path, _, _ = first_round
    document = load_validation_report(report_path)
    case_id = document["queries"][1]["id"]
    document["queries"][1]["target_sql"] = "SELECT 1; DROP TABLE orders"
    report_path.write_text(json.dumps(document))
    monkeypatch.setattr("doris_sql_validator.pg_probe.execute_query", lambda *a, **kw: pytest.fail("must not execute"))
    batch = probe_postgres_cases(cases, report_path, [{"case_id": case_id, "candidate_sql": "SELECT 2"}])
    assert batch["逐条请求"][0]["处理状态"] == "未执行"
