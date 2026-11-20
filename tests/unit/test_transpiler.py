import pytest

from doris_sql_validator.models import CaseDefinition
from doris_sql_validator.transpiler import SqlglotTranspiler, UnsafeQueryError


def test_transpiles_smoke_case() -> None:
    case = CaseDefinition(id="constant-one", statement_index=1, sql="SELECT 1 AS value")
    result = SqlglotTranspiler().transpile_case(case, source_dialect="hive")
    assert result.target_sql == "SELECT 1 AS `value`"
    assert result.explicit_output_aliases is True


def test_rejects_non_query() -> None:
    case = CaseDefinition(id="unsafe-ddl", statement_index=1, sql="CREATE TABLE dangerous (id INT)")
    with pytest.raises(UnsafeQueryError):
        SqlglotTranspiler().transpile_case(case, source_dialect="hive")

