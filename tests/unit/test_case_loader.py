from pathlib import Path

from doris_sql_validator.case_loader import (
    load_case_file,
    load_cases,
)


PROJECT_DIR = Path(__file__).resolve().parents[2]


def test_candidate_file_is_valid_and_unique() -> None:
    path = PROJECT_DIR / "cases/hive/candidates/hive-doris-mvp.yaml"
    loaded = load_case_file(path)
    cases = loaded.definition.cases
    assert len(cases) == 32
    assert len({case.id for case in cases}) == 32
    assert loaded.definition.validation_mode == "live_source"
    assert loaded.definition.import_summary.accepted == 32
    assert loaded.definition.model_dump().get("format_version") is None
    assert loaded.definition.model_dump().get("suite") is None


def test_feishu_batch_2_contains_only_executable_cases() -> None:
    cases = load_cases(
        PROJECT_DIR / "cases/hive/candidates/hive-doris-feishu-batch-2.yaml"
    )

    assert len(cases) == 9
    assert len({case.id for case in cases}) == 9
    assert all(case.sql.strip().upper().startswith("SELECT") for case in cases)

