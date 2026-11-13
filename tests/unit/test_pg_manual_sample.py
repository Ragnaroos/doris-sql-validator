"""Offline safety and evidence tests for the explicit sample preparation helper."""
from datetime import date
import importlib.util
import json
from pathlib import Path

import pytest

from doris_sql_validator.models import (
    CaseDefinition, CaseFile, ImportDiagnostic, ImportSummary, InputSpec,
    RecordedOutputSpec, SourceSpec, TargetSpec,
)


ROOT = Path(__file__).resolve().parents[2]
spec = importlib.util.spec_from_file_location("pg_manual_sample", ROOT / "scripts/pg_manual_sample.py")
sample = importlib.util.module_from_spec(spec)
spec.loader.exec_module(sample)


def test_record_comparison_preserves_duplicates_null_and_full_float_values():
    assert sample.bag_evidence([(1,), (1,), (None,)])[0] != sample.bag_evidence([(1,), (None,)])[0]
    assert sample.record_key((None,)) != sample.record_key(("",))
    assert sample.record_key((1,)) != sample.record_key(("1",))
    assert sample.record_key((100.0,)) != sample.record_key((100.00000000000001,))
    assert sample.bag_evidence([(1,), (2,)]) == sample.bag_evidence([(2,), (1,)])
    assert "2024-02-29" in sample.record_key((date(2024, 2, 29),))


def test_collector_copies_only_inputs_not_historical_observations(tmp_path, monkeypatch):
    corpus = tmp_path / "old"
    (corpus / "assets").mkdir(parents=True)
    (corpus / "setup/data").mkdir(parents=True)
    (corpus / "assets/sample.sql").write_text("SELECT 1;")
    (corpus / "setup/postgres.sql").write_text("CREATE TABLE t(id int);")
    (corpus / "setup/data/a.data").write_text("1\n")
    entry = dict(id="pg-sample-0001", category="smoke", file="sample.sql", line_start=1, line_end=1, source_sql="SELECT 1;", official_occurrence=1, outcome="OLD", source_rows=[[999]], rewrite="SELECT 999")
    (corpus / "provenance.json").write_text(json.dumps({"upstream_commit": "abc", "cases": [entry]}))
    monkeypatch.setattr(sample, "INPUT", tmp_path / "current")
    sample.collect_inputs(corpus)
    scope = sample.load_scope()
    assert scope["cases"][0]["source_sql"] == "SELECT 1;"
    assert not {"outcome", "source_rows", "rewrite"} & scope["cases"][0].keys()
    with pytest.raises(RuntimeError, match="拒绝覆盖"):
        sample.collect_inputs(corpus)
    (sample.INPUT / "assets/sample.sql").write_text("SELECT 2;")
    with pytest.raises(RuntimeError, match="输入已改变"):
        sample.load_scope()


def test_preparation_refuses_existing_evidence_before_connecting(tmp_path, monkeypatch):
    monkeypatch.setattr(sample, "load_scope", lambda: {})
    monkeypatch.setattr(sample, "OUTPUT", tmp_path)
    (tmp_path / "data-preparation").mkdir()
    monkeypatch.setattr(sample, "PostgresAdapter", lambda: pytest.fail("must not connect"))
    with pytest.raises(RuntimeError, match="拒绝覆盖"):
        sample.prepare("dsv_pg_manual_new")
    with pytest.raises(ValueError, match="独立测试库"):
        sample.prepare("production")


def test_all_rejected_group_uses_normal_yaml_and_validation_report(tmp_path, monkeypatch):
    source = tmp_path / "input"
    source.mkdir()
    output = tmp_path / "report"
    (output / "data-preparation").mkdir(parents=True)
    verification = {"database": "dsv_pg_manual_test", "tables": {"t": {"complete_record_multiset_equal": True}}, "source_baselines": []}
    (output / "data-preparation/data-verification.json").write_text(json.dumps(verification))
    item = dict(id="pg-sample-0001", file="sample.sql", source_sql="SELECT DISTINCT ON(a) a FROM t ORDER BY a USING <;", official_occurrence=1)
    monkeypatch.setattr(sample, "INPUT", source)
    monkeypatch.setattr(sample, "OUTPUT", output)
    monkeypatch.setattr(sample, "ROOT", tmp_path)
    monkeypatch.setattr(sample, "load_scope", lambda: {"cases": [item]})
    diagnostic = ImportDiagnostic(statement_index=1, line_start=1, line_end=1, disposition="error", statement_type="parse_error", reason="USING is not parsed")
    # The raw file has a second query, but it is outside this batch's scope.
    definition = CaseFile(source=SourceSpec(dialect="postgres", engine="postgres"), target=TargetSpec(), input=InputSpec(format="pg-regress"), recorded_output=RecordedOutputSpec(format="pg-regress", file="assets/sample.out", sha256="a"*64), import_summary=ImportSummary(accepted=1, skipped=0, ambiguous=0, errors=1), import_diagnostics=[diagnostic], cases=[CaseDefinition(id="pg-sample-0002", statement_index=2, sql="SELECT 2;", output_occurrence=1)])
    definition.source.database = verification["database"]
    definition.target.database = verification["database"]
    monkeypatch.setattr(sample, "import_case_file", lambda *args: definition)
    monkeypatch.setattr("doris_sql_validator.service._sqlglot_commit", lambda: "test")
    def run_normal_report(command, **kwargs):
        from types import SimpleNamespace
        from doris_sql_validator.case_loader import load_case_file
        from doris_sql_validator.service import ValidationService
        from doris_sql_validator.reporting import write_reports
        path = Path(command[command.index("--path") + 1])
        loaded = load_case_file(path)
        # No adapter/provider is used for parser failures.
        report = ValidationService(loaded.definition, object()).run_suite(loaded.definition.cases)
        write_reports(report, Path(command[command.index("--output-dir") + 1]), case_file_path=path)
        return SimpleNamespace(returncode=1, stdout="", stderr="")
    monkeypatch.setattr(sample.subprocess, "run", run_normal_report)
    sample.validate()
    assert (source / "sample.yaml").exists()
    result = json.loads((output / "validation-summary.json").read_text())
    assert result["runs"][0]["accepted"] == 1
    assert result["runs"][0]["in_scope_import_errors"] == 1
    assert sorted(p.name for p in (output / "validation/sample").iterdir()) == ["validation.json", "validation.md"]
    assert result["runs"][0]["summary"]["translation_failed"] == 1
    assert "USING is not parsed" in (output / "validation/sample/validation.md").read_text()
    sample.validate(overwrite=True)
    assert (source / "sample.yaml").exists()


def test_overwrite_and_resume_are_mutually_exclusive():
    with pytest.raises(ValueError, match="不能同时"):
        sample.validate(overwrite=True, resume=True)


def test_reverification_refuses_untraceable_database_before_connecting(tmp_path, monkeypatch):
    output = tmp_path / "report"
    folder = output / "data-preparation"
    folder.mkdir(parents=True)
    (folder / "data-verification.json").write_text(json.dumps({"database": "production"}))
    (folder / "execution-start.json").write_text(json.dumps({"database": "production"}))
    monkeypatch.setattr(sample, "load_scope", lambda: {})
    monkeypatch.setattr(sample, "OUTPUT", output)
    monkeypatch.setattr(sample, "PostgresAdapter", lambda: pytest.fail("must not connect"))
    with pytest.raises(RuntimeError, match="拒绝复用"):
        sample.reverify()
