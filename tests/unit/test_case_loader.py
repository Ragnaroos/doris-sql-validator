from pathlib import Path

from doris_sql_validator.case_loader import (
    load_case_file,
    load_cases,
    write_case_file,
)
from doris_sql_validator.models import (
    CaseDefinition, CaseFile, ImportSummary, InputSpec, SourceSpec, TargetSpec,
)


def _write_minimal_cases(path: Path) -> None:
    write_case_file(
        CaseFile(
            source=SourceSpec(dialect="hive", engine="hive", connection_profile="hive-local"),
            target=TargetSpec(),
            input=InputSpec(format="manual"),
            import_summary=ImportSummary(accepted=1, skipped=0, ambiguous=0, errors=0),
            cases=[CaseDefinition(id="constant-one", statement_index=1, sql="SELECT 1 AS value")],
        ),
        path,
    )


def test_case_file_round_trip(tmp_path: Path) -> None:
    path = tmp_path / "cases.yaml"
    _write_minimal_cases(path)
    loaded = load_case_file(path)
    cases = loaded.definition.cases
    assert len(cases) == 1
    assert len({case.id for case in cases}) == 1
    assert loaded.definition.validation_mode == "live_source"
    assert loaded.definition.import_summary.accepted == 1
    assert loaded.definition.model_dump().get("format_version") is None
    assert loaded.definition.model_dump().get("suite") is None


def test_load_cases_returns_query_definitions(tmp_path: Path) -> None:
    path = tmp_path / "cases.yaml"
    _write_minimal_cases(path)
    cases = load_cases(path)

    assert len(cases) == 1
    assert cases[0].id == "constant-one"
    assert all(case.sql.strip().upper().startswith("SELECT") for case in cases)

