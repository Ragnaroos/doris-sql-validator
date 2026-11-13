"""Offline end-to-end handoff and diagnostics; no model or live DB is needed."""
from datetime import datetime, timezone
import json
from pathlib import Path

import pytest
from typer.testing import CliRunner

from doris_sql_validator.cli import app
from doris_sql_validator.case_loader import load_case_file
from doris_sql_validator.handoff import prepare_pg_review
from doris_sql_validator.models import QueryColumn, QueryResult
from doris_sql_validator.pg_probe import compare_probe, execute_query, probe_postgres_case


@pytest.fixture
def first_round(tmp_path, monkeypatch):
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
    case_path = tmp_path / "cases.yaml"
    imported = runner.invoke(app, ["import-cases", "--format", "pg-regress", "--dialect", "postgres", "--input", str(sql), "--recorded-output", str(out), "--source-database", "pg_test", "--target-database", "doris_test", "--output", str(case_path)])
    assert imported.exit_code == 0, imported.output
    run = runner.invoke(app, ["run", "--path", str(case_path), "--output-dir", str(tmp_path / "validation")])
    assert run.exit_code == 1, run.output
    report_path = tmp_path / "validation/validation.json"
    report = json.loads(report_path.read_text())
    assert engines == ["doris"]
    assert len(calls) == 3
    assert report["summary"]["successful_matches"] == 1
    assert report["summary"]["negative_source_cases"] == 1
    assert report["summary"]["total"] == 3
    assert report["summary"]["successful_match_rate_all"] == pytest.approx(1/3)
    assert report["import_summary"]["skipped"] == 2
    return tmp_path, case_path, report_path, sql, out


def test_full_offline_handoff_references_originals_without_copies(first_round):
    root, cases, report, sql, out = first_round
    hashes = [p.read_bytes() for p in [cases, report, sql, out]]
    target = root / "handoff"
    path = prepare_pg_review(cases, report, target, setup_files=[sql])
    assert path.is_file()
    assert path.name == "HANDOFF.md"
    index = json.loads((target / "evidence-index.json").read_text())
    assert sorted(p.name for p in target.iterdir()) == ["HANDOFF.md", "evidence-index.json"]
    assert (target / index["入口"]["case_file"]).resolve() == cases.resolve()
    assert (target / index["入口"]["report_file"]).resolve() == report.resolve()
    assert (target / index["入口"]["source_file"]).resolve() == sql.resolve()
    assert (target / index["入口"]["recorded_output_file"]).resolve() == out.resolve()
    loaded = load_case_file(target / index["入口"]["case_file"])
    assert loaded.path == cases.resolve()
    for entry in index["文件"]:
        assert (target / entry["文件"]).is_file()
    assert len(index["待分析查询"]) == 2
    assert index["数据准备报告已提供"] is False
    assert len(index["导入阶段诊断"]) == 2
    assert [p.read_bytes() for p in [cases, report, sql, out]] == hashes
    with pytest.raises(ValueError, match="非空"):
        prepare_pg_review(cases, report, target, setup_files=[sql])


def test_handoff_rejects_changed_case_file(first_round):
    root, cases, report, sql, _ = first_round
    cases.write_text(cases.read_text() + "\n")
    with pytest.raises(ValueError, match="修改"):
        prepare_pg_review(cases, report, root / "handoff", setup_files=[sql])
    assert not (root / "handoff").exists()


def test_handoff_references_preparation_report_without_copying(first_round):
    root, cases, report, sql, _ = first_round
    preparation = root / "数据准备报告.md"
    preparation.write_text("# 数据准备报告\n历史报告原件，不由交接工具重新核验。\n")
    original = preparation.read_bytes()
    target = root / "handoff-new"
    prepare_pg_review(cases, report, target, setup_files=[sql], preparation_report=preparation)
    assert preparation.read_bytes() == original
    index = json.loads((target / "evidence-index.json").read_text())
    assert index["数据准备报告已提供"] is True
    assert (target / index["入口"]["preparation_report"]).resolve() == preparation.resolve()
    assert not (target / "data-preparation").exists()
    assert not (target / "交接说明.md").exists()
    assert not (target / "证据索引.json").exists()


def test_handoff_does_not_inherit_chinese_setup_names(first_round):
    root, cases, report, _, _ = first_round
    setup = root / "用户建表.sql"
    setup.write_text("CREATE TABLE orders(amount INT);\n")
    original = setup.read_bytes()
    target = root / "handoff-ascii"
    prepare_pg_review(cases, report, target, setup_files=[setup])
    assert setup.read_bytes() == original
    assert not (target / "data-preparation").exists()
    assert all(str(p.relative_to(target)).isascii() for p in target.rglob("*"))
    index = json.loads((target / "evidence-index.json").read_text())
    assert (target / index["入口"]["setup_files"][0]).resolve() == setup.resolve()
    entry = next(e for e in index["文件"] if (target / e["文件"]).resolve() == setup.resolve())
    assert setup.name in entry["文件"]


def test_cli_handoff_only_creates_two_reference_files(first_round):
    root, cases, report, sql, _ = first_round
    target = root / "cli-handoff"
    result = CliRunner().invoke(app, ["prepare-pg-review", "--path", str(cases),
        "--report", str(report), "--setup", str(sql), "--output-dir", str(target)])
    assert result.exit_code == 0, result.output
    assert sorted(p.name for p in target.iterdir()) == ["HANDOFF.md", "evidence-index.json"]
    assert "不复制" in (target / "HANDOFF.md").read_text()


def test_handoff_rejects_changed_out(first_round):
    root, cases, report, sql, out = first_round
    out.write_text(out.read_text() + "changed")
    with pytest.raises(ValueError, match="改变"):
        prepare_pg_review(cases, report, root / "handoff", setup_files=[sql])


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


def test_probe_explicit_candidate_and_boundary_save_distinct_evidence(first_round, monkeypatch):
    root, cases, report_path, _, _ = first_round
    report = json.loads(report_path.read_text())
    case = report["cases"][1]
    candidate = root / "candidate.sql"
    candidate.write_text("SELECT 5 DIV 2 AS value")
    calls = []
    def execute(engine, sql, database, **kwargs):
        calls.append((engine, sql, database))
        if engine == "postgres": return result("int4", [[2]])
        return result("int", [[2]]) if "DIV" in sql else result("double", [[2.5]])
    monkeypatch.setattr("doris_sql_validator.pg_probe.execute_query", execute)
    path = probe_postgres_case(cases, report_path, case["id"], candidate, root / "probe")
    assert path.name == "probe-report.md"
    evidence = json.loads(path.with_name("probe-evidence.json").read_text())
    assert len(calls) == 5
    assert evidence["候选与社区输出相同"] is False
    assert evidence["独立候选比较"]["记录值及重复次数"] == "一致"
    assert evidence["社区输出比较"]["记录值及重复次数"] == "不同"
    assert evidence["是否边界变体"] is False
    source_variant = root / "source-variant.sql"
    source_variant.write_text("SELECT NULL::int AS value")
    candidate.write_text("SELECT CAST(NULL AS INT) AS value")
    path = probe_postgres_case(cases, report_path, case["id"], candidate, root / "boundary", source_variant=source_variant)
    evidence = json.loads(path.with_name("probe-evidence.json").read_text())
    assert evidence["是否边界变体"] is True
    assert "社区Doris实际结果" not in evidence
    assert report_path.read_text() == json.dumps(report, ensure_ascii=False, indent=2) + "\n"
