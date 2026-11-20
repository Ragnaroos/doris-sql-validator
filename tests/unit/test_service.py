from doris_sql_validator.models import (
    CaseDefinition,
    CaseFile,
    ImportSummary,
    InputSpec,
    QueryColumn,
    QueryResult,
    RecordedOutputSpec,
    SourceEvidence,
    SourceSpec,
    TargetSpec,
)
from doris_sql_validator.service import ValidationService


class _Adapter:
    def __init__(self, engine: str, rows: list[list[object]]) -> None:
        self.engine = engine
        self.rows = rows
        self.databases: list[str | None] = []

    def execute_select(self, sql: str, *, database: str | None = None) -> QueryResult:
        self.databases.append(database)
        return QueryResult(
            engine=self.engine,
            success=True,
            columns=[QueryColumn(name="value", canonical_type="integer")],
            rows=self.rows,
        )


class _Provider:
    def __init__(self, adapter: _Adapter, database: str | None) -> None:
        self.adapter = adapter
        self.database = database

    def get_result(self, case: CaseDefinition) -> SourceEvidence:
        return SourceEvidence(
            mode="live_source",
            result=self.adapter.execute_select(case.sql, database=self.database),
        )


def _case() -> CaseDefinition:
    return CaseDefinition(id="constant-one", statement_index=1, sql="SELECT 1 AS value")


def _case_file(*, recorded: bool = False, table_case: bool = False) -> CaseFile:
    case = (
        CaseDefinition(
            id="table-query", statement_index=1, sql="SELECT value FROM items"
        )
        if table_case
        else _case()
    )
    return CaseFile(
        source=SourceSpec(
            dialect="hive",
            engine="hive",
            connection_profile="hive-local",
            database="source_db",
        ),
        target=TargetSpec(
            connection_profile="doris-local",
            database="target_db",
        ),
        input=InputSpec(format="manual"),
        recorded_output=(
            RecordedOutputSpec(
                format="hive-qtest", file="expected.out"
            )
            if recorded
            else None
        ),
        import_summary=ImportSummary(
            accepted=1, skipped=0, ambiguous=0, errors=0
        ),
        cases=[
            case.model_copy(update={"output_occurrence": 1}) if recorded else case
        ],
    )


def test_live_source_executes_both_sides_without_fixture_gate() -> None:
    case_file = _case_file()
    case = case_file.cases[0]
    source = _Adapter("hive", [[1]])
    target = _Adapter("doris", [[1]])

    report = ValidationService(
        case_file,
        target,  # type: ignore[arg-type]
        source_provider=_Provider(source, "source_db"),
    ).run_case(case)

    assert report.status == "COMPLETED"
    assert report.data_assurance == "not_applicable"
    assert report.comparison and report.comparison.observed_outcome == "MATCH"
    assert source.databases == ["source_db"]
    assert target.databases == ["target_db"]


def test_table_mismatch_is_reported_as_inconclusive_without_data_assurance() -> None:
    case_file = _case_file(table_case=True)
    case = case_file.cases[0]
    source = _Adapter("hive", [[1]])
    target = _Adapter("doris", [[2]])

    report = ValidationService(
        case_file,
        target,  # type: ignore[arg-type]
        source_provider=_Provider(source, "source_db"),
    ).run_case(case)

    assert report.status == "COMPLETED"
    assert report.data_assurance == "unverified"
    assert report.comparison
    assert report.comparison.observed_outcome == "ROW_VALUE_MISMATCH"
    assert report.comparison.semantic_assessment == "INCONCLUSIVE"


def test_final_order_by_selects_ordered_comparison() -> None:
    case_file = _case_file(table_case=True)
    ordered_case = case_file.cases[0].model_copy(
        update={"sql": "SELECT value FROM items ORDER BY value"}
    )
    case_file = case_file.model_copy(update={"cases": [ordered_case]})
    source = _Adapter("hive", [[1], [2]])
    target = _Adapter("doris", [[2], [1]])

    report = ValidationService(
        case_file,
        target,  # type: ignore[arg-type]
        source_provider=_Provider(source, "source_db"),
    ).run_case(ordered_case)

    assert report.comparison
    assert report.comparison.observed_outcome == "ROW_VALUE_MISMATCH"


def test_recorded_output_mode_is_inferred_and_needs_no_live_adapter() -> None:
    case_file = _case_file(recorded=True)
    case = case_file.cases[0]
    target = _Adapter("doris", [[1]])

    class _RecordedProvider:
        def get_result(self, case: CaseDefinition) -> SourceEvidence:
            return SourceEvidence(
                mode="recorded_output",
                result=QueryResult(
                    engine="hive-recorded",
                    success=True,
                    columns=[QueryColumn(name="value", canonical_type="unknown")],
                    rows=[[1]],
                ),
                artifact="expected.out",
            )

    report = ValidationService(
        case_file,
        target,  # type: ignore[arg-type]
        source_provider=_RecordedProvider(),
    ).run_case(case)

    assert report.validation_mode == "recorded_output"
    assert report.comparison
    assert report.comparison.semantic_assessment == "MATCHES_RECORDED_SOURCE_OUTPUT"
    assert target.databases == ["target_db"]
