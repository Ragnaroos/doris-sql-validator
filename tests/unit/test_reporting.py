import json
from datetime import datetime, timezone

import pytest

from doris_sql_validator.comparison import compare_results, describe_difference
from doris_sql_validator.models import (
    CaseRunReport, ComparisonResult, ComparisonSpec, ImportDiagnostic, ImportSummary,
    InputSpec, NormalizedError, QueryColumn, QueryResult, SourceEvidence, SourceSpec,
    SuiteReport, TargetSpec,
)
from doris_sql_validator.reporting import build_validation_report, load_validation_report, write_reports


def _result(rows=None, *, error=None):
    return QueryResult(engine="postgres", success=error is None,
        columns=[QueryColumn(name="value", canonical_type="integer")] if error is None else [],
        rows=rows if rows is not None else [[1]], error=error)


def _case(id="one", *, source=None, target=None, sql="SELECT 1 AS value", spec=None):
    source = source or SourceEvidence(mode="live_source", result=_result())
    target = target or _result().model_copy(update={"engine": "doris"})
    spec = spec or ComparisonSpec()
    comparison = compare_results(source, target, spec, explicit_output_aliases=True, data_assurance="not_applicable")
    return CaseRunReport(id=id, validation_mode="live_source", data_assurance="not_applicable",
        status="COMPLETED", source_sql=sql, target_sql=sql,
        source_evidence=source, target_result=target, comparison=comparison,
        difference=describe_difference(source, target, spec, comparison, explicit_output_aliases=True))


def _report(cases, diagnostics=None):
    diagnostics = diagnostics or []
    return SuiteReport(started_at=datetime(2026, 1, 1, tzinfo=timezone.utc),
        finished_at=datetime(2026, 1, 1, tzinfo=timezone.utc), sqlglot_version="test",
        source=SourceSpec(dialect="postgres", engine="postgres"), target=TargetSpec(),
        input=InputSpec(format="manual"), validation_mode="live_source",
        import_summary=ImportSummary(accepted=len(cases), skipped=0, ambiguous=0, errors=len(diagnostics)),
        import_diagnostics=diagnostics, cases=cases)


def test_only_one_json_is_written_and_overwritten(tmp_path):
    report = _report([_case()])
    path = write_reports(report, tmp_path / "validation.json")
    changed = report.model_copy(update={"sqlglot_version": "next"})
    assert write_reports(changed, tmp_path / "validation.json") == path
    assert sorted(p.name for p in tmp_path.iterdir()) == ["validation.json"]
    document = load_validation_report(path)
    assert set(document) == {"run", "summary", "queries"}
    assert document["run"]["sqlglot_version"] == "next"
    assert document["queries"] == [{"id": "one", "source_sql": "SELECT 1 AS value", "result": "匹配"}]
    assert document["summary"]["successful_match_rate"]["value"] == 1


def test_in_memory_report_matches_file_payload_without_creating_files(tmp_path):
    report = _report([_case()])
    payload = build_validation_report(report)
    assert list(tmp_path.iterdir()) == []
    saved = load_validation_report(write_reports(report, tmp_path / "validation.json"))
    assert payload == saved


def test_match_does_not_dump_rows_types_digests_or_target_sql(tmp_path):
    binary = _result([[b"\x00\xbe\xff"]])
    source = SourceEvidence(mode="live_source", result=binary)
    case = _case(source=source, target=binary.model_copy(update={"engine": "doris"}))
    document = load_validation_report(write_reports(_report([case]), tmp_path / "validation.json"))
    assert set(document["queries"][0]) == {"id", "source_sql", "result"}
    assert "result_digest" not in json.dumps(document)
    assert "row_sample" not in json.dumps(document)


def test_negative_and_environment_are_not_success_or_main_attribution(tmp_path):
    negative = SourceEvidence(mode="live_source", result=_result(error=NormalizedError(category="EXECUTION_ERROR", message="division by zero")))
    environment = SourceEvidence(mode="live_source", result=_result(error=NormalizedError(category="TABLE_NOT_FOUND", message="relation t does not exist")))
    cases = [_case("negative", source=negative, target=negative.result), _case("environment", source=environment)]
    document = load_validation_report(write_reports(_report(cases), tmp_path / "validation.json"))
    assert document["summary"]["successful_matches"] == 0
    assert document["summary"]["negative_source_cases"] == 1
    assert document["summary"]["needs_attribution"] == 0
    assert document["summary"]["prerequisite_issues"] == 1
    assert document["summary"]["successful_match_rate"]["value"] is None
    assert document["queries"][0]["source_error"]["message"] == "division by zero"


def test_doris_errors_retain_actual_code_and_message_once(tmp_path):
    target = _result(error=NormalizedError(category="FUNCTION_NOT_FOUND", message="function f not found", code="1105"))
    case = _case("target-error", target=target, sql="SELECT f(1)")
    path = write_reports(_report([case]), tmp_path / "validation.json")
    record = load_validation_report(path)["queries"][0]
    assert record["action"] == "归因"
    assert record["result"] == "Doris 执行失败"
    assert record["doris_error"]["code"] == "1105"
    assert path.read_text().count("function f not found") == 1


@pytest.mark.parametrize("ordered", [False, True])
def test_differences_are_real_counterexamples_not_first_five_samples(tmp_path, ordered):
    rows = [[i] for i in range(20)]
    target_rows = rows[:-1] + [[99]]
    case = _case(source=SourceEvidence(mode="live_source", result=_result(rows)),
        target=_result(target_rows), spec=ComparisonSpec(row_order="ordered" if ordered else "multiset"))
    difference = load_validation_report(write_reports(_report([case]), tmp_path / "validation.json"))["queries"][0]["difference"]
    if ordered:
        assert difference["rows"] == [{"row": 20, "source": [19], "doris": [99]}]
    else:
        assert difference["source_only"] == [{"row": [19], "extra_count": 1}]
        assert difference["doris_only"] == [{"row": [99], "extra_count": 1}]


def test_duplicate_counts_and_float_tolerance_use_existing_comparison_rules():
    source = SourceEvidence(mode="live_source", result=_result([[1], [1], [2]]))
    case = _case(source=source, target=_result([[1], [2], [2]]))
    assert case.difference["source_only"] == [{"row": [1], "extra_count": 1}]
    assert case.difference["doris_only"] == [{"row": [2], "extra_count": 1}]
    source = SourceEvidence(mode="live_source", result=_result([[1.0], [2.0]]))
    case = _case(source=source, target=_result([[1.0 + 1e-13], [9.0]]))
    assert case.difference["source_only"] == [{"row": [2.0], "extra_count": 1}]


def test_row_count_and_schema_differences_are_bounded(tmp_path):
    case = _case(target=_result([[1], [2]]))
    assert case.difference == {"source_row_count": 1, "doris_row_count": 2}
    columns = [QueryColumn(name=f"c{i}", canonical_type="integer") for i in range(8)]
    source = SourceEvidence(mode="live_source", result=_result().model_copy(update={"columns": columns}))
    target = _result().model_copy(update={"columns": [c.model_copy(update={"name": "x" + c.name}) for c in columns]})
    case = _case(source=source, target=target)
    assert len(case.difference["columns"]) == 3
    assert case.difference["omitted_columns"] == 5


def test_unavailable_row_evidence_is_not_reported_as_success(tmp_path):
    from doris_sql_validator.models import EvidenceCapabilities
    source = SourceEvidence(mode="live_source", result=_result(), capabilities=EvidenceCapabilities(row_values="unavailable"))
    document = load_validation_report(write_reports(_report([_case(source=source)]), tmp_path / "validation.json"))
    assert document["queries"][0]["result"] == "证据不足"
    assert document["summary"]["successful_matches"] == 0


def test_import_lookup_failures_remain_visible_without_duplicate_parser_records(tmp_path):
    diagnostic = ImportDiagnostic(statement_index=2, line_start=3, line_end=3,
        disposition="error", statement_type="recorded_output", reason="SQL echo not found",
        case_id="missing-output", sql="SELECT 2", output_occurrence=1)
    document = load_validation_report(write_reports(_report([_case()], [diagnostic]), tmp_path / "validation.json"))
    assert document["summary"]["total"] == 2
    assert document["queries"][1]["source_sql"] == "SELECT 2"
    assert document["queries"][1]["result"] == "导入时参考输出读取失败"


def test_fifty_five_queries_have_fifty_five_single_line_records(tmp_path):
    negative = SourceEvidence(mode="live_source", result=_result(error=NormalizedError(category="EXECUTION_ERROR", message="division by zero")))
    failure = _result(error=NormalizedError(category="FUNCTION_NOT_FOUND", message="unknown function", code="1105"))
    cases = [_case(f"match-{i}", sql=f"SELECT {i}") for i in range(35)]
    cases += [_case(f"negative-{i}", source=negative, target=negative.result, sql=f"SELECT {i}/0") for i in range(5)]
    cases += [_case(f"error-{i}", target=failure, sql=f"SELECT f({i})") for i in range(15)]
    path = write_reports(_report(cases), tmp_path / "validation.json")
    document = load_validation_report(path)
    assert document["summary"]["total"] == 55
    assert document["summary"]["needs_attribution"] == 15
    assert document["summary"]["successful_match_rate"]["value"] == .7
    assert len([line for line in path.read_text().splitlines() if line.startswith('    {"id":')]) == 55
    assert path.read_text().count('"source_sql"') == 55
    assert len(path.read_bytes()) < 30000


def test_reader_rejects_wrong_structure_and_duplicate_case_ids(tmp_path):
    path = tmp_path / "report.json"
    path.write_text('{"cases": []}')
    with pytest.raises(ValueError, match="三部分"):
        load_validation_report(path)
    path.write_text(json.dumps({"run": {}, "summary": {}, "queries": [
        {"id": "a", "source_sql": "SELECT 1", "result": "匹配"},
        {"id": "a", "source_sql": "SELECT 1", "result": "匹配"}]}))
    with pytest.raises(ValueError, match="重复"):
        load_validation_report(path)


def test_multiline_source_sql_is_not_rewritten_and_occupies_one_record_line(tmp_path):
    sql = "SELECT -- preserve this comment\n 1 AS value"
    path = write_reports(_report([_case(sql=sql)]), tmp_path / "validation.json")
    assert load_validation_report(path)["queries"][0]["source_sql"] == sql
    assert len([line for line in path.read_text().splitlines() if line.startswith('    {"id":')]) == 1


def test_filtered_run_does_not_report_unselected_import_failures(tmp_path):
    diagnostic = ImportDiagnostic(statement_index=2, line_start=2, line_end=2,
        disposition="error", statement_type="recorded_output", reason="SQL echo not found",
        case_id="not-selected", sql="SELECT 2", output_occurrence=1)
    report = _report([_case()], [diagnostic]).model_copy(update={"filtered": True})
    document = load_validation_report(write_reports(report, tmp_path / "validation.json"))
    assert document["run"]["filtered"] is True
    assert document["summary"]["total"] == 1
    assert document["summary"]["import"]["errors"] == 1
    assert "not-selected" not in [query["id"] for query in document["queries"]]
