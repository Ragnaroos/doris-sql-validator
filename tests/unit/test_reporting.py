from datetime import datetime, timezone

from doris_sql_validator.models import (
    CaseRunReport,
    ComparisonResult,
    ImportDiagnostic,
    ImportSummary,
    InputSpec,
    NormalizedError,
    QueryColumn,
    QueryResult,
    SourceEvidence,
    SourceSpec,
    SuiteReport,
    TargetSpec,
)
from doris_sql_validator.reporting import render_markdown, write_reports


def test_reports_use_stable_final_paths_and_overwrite(tmp_path) -> None:
    first = SuiteReport(
        started_at=datetime(2026, 1, 1, tzinfo=timezone.utc),
        finished_at=datetime(2026, 1, 1, tzinfo=timezone.utc),
        sqlglot_version="test",
        source=SourceSpec(
            dialect="hive", engine="hive", connection_profile="hive-local"
        ),
        target=TargetSpec(connection_profile="doris-local"),
        input=InputSpec(format="manual"),
        validation_mode="live_source",
        import_summary=ImportSummary(accepted=0, skipped=1, ambiguous=0, errors=0),
        import_diagnostics=[
            ImportDiagnostic(
                statement_index=1,
                line_start=1,
                line_end=1,
                disposition="skipped",
                statement_type="create",
                reason="not a read-only Query",
            )
        ],
        cases=[],
    )
    second = first.model_copy(
        update={"started_at": datetime(2026, 1, 2, tzinfo=timezone.utc)}
    )

    first_paths = write_reports(first, tmp_path)
    second_paths = write_reports(second, tmp_path)

    assert first_paths == second_paths
    assert first_paths == (tmp_path / "validation.json", tmp_path / "validation.md")
    json_text = (tmp_path / "validation.json").read_text()
    assert "2026-01-02" in json_text
    assert '"summary"' in json_text
    assert "输入处理与证据限制" in (tmp_path / "validation.md").read_text()
    assert sorted(path.name for path in tmp_path.iterdir()) == [
        "validation.json",
        "validation.md",
    ]
def test_markdown_summarizes_matches_and_expands_failures() -> None:
    source_result = QueryResult(
        engine="hive",
        success=True,
        columns=[QueryColumn(name="value", canonical_type="integer")],
        rows=[[1]],
    )
    match = CaseRunReport(
        id="match-one",
        validation_mode="live_source",
        data_assurance="not_applicable",
        status="COMPLETED",
        source_sql="SELECT 1 AS value",
        target_sql="SELECT 1 AS `value`",
        source_evidence=SourceEvidence(mode="live_source", result=source_result),
        target_result=source_result.model_copy(update={"engine": "doris"}),
        comparison=ComparisonResult(
            observed_outcome="MATCH",
            semantic_assessment="MATCH_ON_CURRENT_ENVIRONMENTS",
            equivalent=True,
            summary="rows match",
            details=["source_digest=hidden-on-match", "doris_digest=hidden-on-match"],
        ),
    )
    mismatch = CaseRunReport(
        id="target-error",
        validation_mode="live_source",
        data_assurance="not_applicable",
        status="COMPLETED",
        source_sql="SELECT missing_function(1)",
        target_sql="SELECT MISSING_FUNCTION(1)",
        source_evidence=SourceEvidence(mode="live_source", result=source_result),
        target_result=QueryResult(
            engine="doris",
            success=False,
            error=NormalizedError(
                category="FUNCTION_NOT_FOUND",
                message="function missing_function not found",
                code="1105",
            ),
        ),
        comparison=ComparisonResult(
            observed_outcome="EXECUTION_STATUS_MISMATCH",
            semantic_assessment="DIFFERENT_FOR_CONSTANT_QUERY",
            equivalent=False,
            summary="Source succeeded and Doris failed",
            details=["source_success=True", "doris_success=False"],
            possible_causes=["doris-function-is-unavailable"],
        ),
    )
    report = SuiteReport(
        started_at=datetime(2026, 1, 1, tzinfo=timezone.utc),
        finished_at=datetime(2026, 1, 1, tzinfo=timezone.utc),
        sqlglot_version="test",
        source=SourceSpec(
            dialect="hive", engine="hive", connection_profile="hive-local"
        ),
        target=TargetSpec(connection_profile="doris-local"),
        input=InputSpec(format="manual"),
        validation_mode="live_source",
        import_summary=ImportSummary(
            accepted=2, skipped=0, ambiguous=0, errors=0
        ),
        import_diagnostics=[],
        cases=[match, mismatch],
    )

    markdown = render_markdown(report)

    assert "查询总数：**2**" in markdown
    assert "两端成功且已有证据匹配：**1**" in markdown
    assert "Doris 执行失败：**1**" in markdown
    assert "### match-one" not in markdown
    assert "hidden-on-match" not in markdown
    assert "Baseline capabilities" not in markdown
    assert "能比较什么" in markdown
    assert "字段类型" in markdown
    assert "### target-error — 两端执行状态不同" in markdown
    assert "function missing_function not found" in markdown
    assert "后续应如何判断" in markdown


def test_binary_results_do_not_require_utf8_decoding(tmp_path) -> None:
    result = QueryResult(
        engine="postgres", success=True,
        columns=[QueryColumn(name="value", canonical_type="binary")],
        rows=[[b"\x00\xbe\xff"]],
    )
    report = SuiteReport(
        started_at=datetime(2026, 1, 1, tzinfo=timezone.utc),
        finished_at=datetime(2026, 1, 1, tzinfo=timezone.utc),
        sqlglot_version="test", source=SourceSpec(dialect="postgres", engine="postgres"),
        target=TargetSpec(), input=InputSpec(format="manual"),
        validation_mode="live_source",
        import_summary=ImportSummary(accepted=1, skipped=0, ambiguous=0, errors=0),
        import_diagnostics=[],
        cases=[CaseRunReport(
            id="binary", validation_mode="live_source", data_assurance="not_applicable",
            status="COMPLETED", source_sql="SELECT decode('00beff', 'hex')",
            source_evidence=SourceEvidence(mode="live_source", result=result),
            target_result=result.model_copy(update={"engine": "doris"}),
        )],
    )
    json_path, _ = write_reports(report, tmp_path)
    import json
    payload = json.loads(json_path.read_text())
    assert payload["cases"][0]["source_evidence"]["result"]["row_sample"] == [[{"$binary": "AL7/"}]]


def test_compatible_error_match_is_not_counted_as_success(tmp_path) -> None:
    failed = QueryResult(engine="postgres", success=False, error=NormalizedError(category="EXECUTION_ERROR", message="division by zero"))
    case = CaseRunReport(id="negative", validation_mode="live_source", data_assurance="not_applicable", status="COMPLETED", source_sql="SELECT 1/0",
        source_evidence=SourceEvidence(mode="live_source", result=failed), target_result=failed.model_copy(update={"engine": "doris"}),
        comparison=ComparisonResult(observed_outcome="MATCH", semantic_assessment="MATCH_ON_CURRENT_ENVIRONMENTS", equivalent=True, summary="compatible errors"))
    report = SuiteReport(started_at=datetime(2026, 1, 1, tzinfo=timezone.utc), finished_at=datetime(2026, 1, 1, tzinfo=timezone.utc), sqlglot_version="test",
        source=SourceSpec(dialect="postgres", engine="postgres"), target=TargetSpec(), input=InputSpec(format="manual"), validation_mode="live_source",
        import_summary=ImportSummary(accepted=1, skipped=0, ambiguous=0, errors=0), import_diagnostics=[], cases=[case])
    path, markdown = write_reports(report, tmp_path)
    import json
    summary = json.loads(path.read_text())["summary"]
    assert summary["matched"] == 1  # preserve old machine code without declaring pass
    assert summary["successful_matches"] == 0
    assert summary["needs_review"] == 1
    assert summary["negative_source_cases"] == 1
    assert "### negative" in markdown.read_text()
    assert "具体原因尚未确认" in markdown.read_text()
