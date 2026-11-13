from pathlib import Path

import pytest

from doris_sql_validator.case_loader import load_cases
from doris_sql_validator.transpiler import SqlglotTranspiler, UnsafeQueryError


PROJECT_DIR = Path(__file__).resolve().parents[2]


def test_transpiles_smoke_case() -> None:
    case = load_cases(
        PROJECT_DIR / "cases/hive/candidates/hive-doris-mvp.yaml"
    )[0]
    result = SqlglotTranspiler().transpile_case(case, source_dialect="hive")
    assert result.target_sql == "SELECT 1 AS `value`"
    assert result.explicit_output_aliases is True


def test_rejects_non_query() -> None:
    case = load_cases(
        PROJECT_DIR / "cases/hive/candidates/hive-doris-mvp.yaml"
    )[0].model_copy(deep=True)
    case.sql = "CREATE TABLE dangerous (id INT)"
    with pytest.raises(UnsafeQueryError):
        SqlglotTranspiler().transpile_case(case, source_dialect="hive")

