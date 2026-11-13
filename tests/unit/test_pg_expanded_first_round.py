"""Offline checks for the explicitly invoked local corpus expansion helper."""
import importlib.util
import json
from pathlib import Path

import pytest


@pytest.fixture
def helper(monkeypatch):
    root = Path(__file__).resolve().parents[2]
    monkeypatch.syspath_prepend(str(root / "scripts"))
    spec = importlib.util.spec_from_file_location("pg_expanded_first_round", root / "scripts/pg_expanded_first_round.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


@pytest.mark.parametrize("sql", [
    "SELECT * FROM not_prepared;",
    "SELECT 'red'::rainbow;",
    "SELECT custom_function(1);",
    "SELECT pg_get_viewdef('v');",
    "SELECT RANDOM();",
    "SELECT CURRENT_TIMESTAMP;",
    "SELECT pg_input_is_valid('bad', 'rainbow');",
    "SELECT pg_read_file('/tmp/x');",
    "SELECT XMLPARSE(DOCUMENT '<!DOCTYPE x SYSTEM \"file:///tmp/x\"><x/>');",
])
def test_expansion_excludes_missing_dependencies_or_unstable_inputs(helper, sql):
    assert helper.exclusion_reason(sql, {"pg_input_is_valid", "pg_get_viewdef", "pg_read_file"}, {"rainbow"})


def test_expansion_keeps_original_constant_sql_and_builtin_gap_tests(helper):
    sql = "SELECT pg_input_is_valid('bad', 'integer');"
    assert helper.exclusion_reason(sql, {"pg_input_is_valid"}, set()) is None
    assert helper.exclusion_reason("SELECT 1 + 2 AS value;", set(), set()) is None


def test_parser_failure_seed_uses_normal_yaml_and_reports(helper, tmp_path, monkeypatch):
    from doris_sql_validator.case_loader import load_case_file
    from doris_sql_validator.service import ValidationService
    from doris_sql_validator.reporting import write_reports

    seed = tmp_path / "cases"
    (seed / "assets").mkdir(parents=True)
    sql = "SELECT a FROM t ORDER BY a USING <;"
    (seed / "assets/select_distinct_on.sql").write_text(sql)
    (seed / "assets/select_distinct_on.out").write_text("official output")
    helper.dump(seed / "scope.json", {"cases": [{"file": "select_distinct_on.sql", "id": "unsupported-query", "source_sql": sql, "line_start": 1, "line_end": 1, "official_occurrence": 1}]})
    monkeypatch.setattr(helper, "SEED", seed)
    helper.prepare_seed_parser_cases("test_db")
    loaded = load_case_file(seed / "select_distinct_on.yaml")
    report = ValidationService(loaded.definition, object()).run_suite(loaded.definition.cases)
    write_reports(report, tmp_path / "validation/select_distinct_on", case_file_path=loaded.path)
    payload = json.loads((tmp_path / "validation/select_distinct_on/validation.json").read_text())
    assert payload["summary"]["translation_failed"] == 1
    assert payload["cases"][0]["failure_stage"] == "source_parse"


def test_archive_only_moves_exact_first_round_outputs(helper, tmp_path, monkeypatch):
    output = tmp_path / "reports/pg-manual/current"
    (output / "validation/group").mkdir(parents=True)
    (output / "data-preparation").mkdir()
    (output / "handoff").mkdir()
    (output / "validation/group/validation.md").write_text("old first round")
    (output / "SUMMARY.md").write_text("old summary")
    (output / "data-preparation/data-verification.json").write_text("keep")
    (output / "handoff/HANDOFF.md").write_text("keep")
    monkeypatch.setattr(helper, "ROOT", tmp_path)
    monkeypatch.setattr(helper, "OUTPUT", output)
    archive = helper.archive_previous()
    assert not (output / "validation").exists()
    assert (archive / "validation/group/validation.md").read_text() == "old first round"
    assert (archive / "SUMMARY.md").read_text() == "old summary"
    assert (output / "data-preparation/data-verification.json").read_text() == "keep"
    assert (output / "handoff/HANDOFF.md").read_text() == "keep"


@pytest.mark.parametrize("legacy_kind", [None, "new", "existing"])
def test_summary_uses_only_current_results_without_history_labels(helper, tmp_path, monkeypatch, legacy_kind):
    output = tmp_path / "reports/current"
    (output / "validation/sample").mkdir(parents=True)
    case_file = tmp_path / "input.yaml"
    case_file.write_text("sample input")
    group = {"name": "sample", "yaml": "input.yaml", "queries": 2}
    if legacy_kind:
        group["kind"] = legacy_kind
    stats = {"successful_matches": 1, "negative_source_cases": 0,
             "translation_failed": 1, "source_evidence_failed": 0,
             "outcomes": {"MATCH": 1, "TRANSLATION_FAILED": 1}}
    helper.dump(output / "validation/sample/validation.json", {
        "case_file": {"sha256": helper.fingerprint(case_file)},
        "summary": stats, "cases": [{"source_sql": "SELECT 1;"}, {"source_sql": "SELECT 2;"}],
    })
    monkeypatch.setattr(helper, "ROOT", tmp_path)
    monkeypatch.setattr(helper, "OUTPUT", output)
    monkeypatch.setattr(helper, "DorisAdapter", lambda: pytest.fail("no database connection"))
    monkeypatch.setattr(helper, "PostgresAdapter", lambda: pytest.fail("no database connection"))
    monkeypatch.setattr(helper.subprocess, "run", lambda *a, **k: pytest.fail("no SQL execution"))
    # The archive does not exist: report rendering must not inspect it to
    # decide whether any SQL has already been executed.
    helper.summarize({"database": "sample", "runtime_groups": [group],
                      "groups": [], "deferred_cases": []}, tmp_path / "absent-archive")
    markdown = (output / "SUMMARY.md").read_text()
    assert "| 输入文件 | 查询数 | 成功结果匹配 | SQLGlot 转译失败 | 详细报告 |" in markdown
    assert "| sample.sql | 2 | 1 | 1 |" in markdown
    assert "| 来源 |" not in markdown
    assert "原有范围重跑" not in markdown
    payload = json.loads((output / "validation-summary.json").read_text())
    assert payload["total"] == 2
    assert payload["successful_matches"] == 1
    assert "added_queries" not in payload
    assert all("kind" not in run for run in payload["runs"])
