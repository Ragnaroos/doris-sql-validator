from __future__ import annotations

import sqlglot
from sqlglot import expressions as exp
from sqlglot.errors import ErrorLevel

from .models import CaseDefinition, TranspilationResult


class UnsafeQueryError(ValueError):
    pass


class SqlglotTranspiler:
    def transpile_case(
        self,
        case: CaseDefinition,
        *,
        source_dialect: str,
        target_dialect: str = "doris",
    ) -> TranspilationResult:
        statements = sqlglot.parse(
            case.sql,
            read=source_dialect,
            error_level=ErrorLevel.RAISE,
        )
        if len(statements) != 1:
            raise UnsafeQueryError(
                f"Expected exactly one statement, received {len(statements)}"
            )
        expression = statements[0]
        self._guard_read_only_query(expression)
        target_sql = expression.sql(
            dialect=target_dialect,
            unsupported_level=ErrorLevel.RAISE,
        )
        return TranspilationResult(
            source_sql=case.sql.strip(),
            target_sql=target_sql,
            source_ast=expression.to_s(),
            explicit_output_aliases=self._has_explicit_output_aliases(expression),
            ordered_result=bool(expression.args.get("order")),
            sqlglot_version=sqlglot.__version__,
            source_dialect=source_dialect,
            target_dialect=target_dialect,
            table_backed=self._is_table_backed(expression),
        )

    @staticmethod
    def _guard_read_only_query(expression: exp.Expression) -> None:
        if not isinstance(expression, exp.Query):
            raise UnsafeQueryError(
                f"Only read-only query expressions are allowed, got {type(expression).__name__}"
            )
        forbidden = (
            exp.Insert,
            exp.Update,
            exp.Delete,
            exp.Create,
            exp.Drop,
            exp.Alter,
            exp.Command,
            exp.Merge,
        )
        for node_type in forbidden:
            if expression.find(node_type):
                raise UnsafeQueryError(f"Forbidden AST node: {node_type.__name__}")

    @staticmethod
    def _has_explicit_output_aliases(expression: exp.Expression) -> bool:
        outer_select = expression if isinstance(expression, exp.Select) else expression.find(exp.Select)
        if not outer_select or not outer_select.expressions:
            return False
        return all(isinstance(item, exp.Alias) for item in outer_select.expressions)

    @staticmethod
    def _is_table_backed(expression: exp.Expression) -> bool:
        cte_names = {
            cte.alias_or_name.lower()
            for cte in expression.find_all(exp.CTE)
            if cte.alias_or_name
        }
        return any(
            table.name.lower() not in cte_names
            for table in expression.find_all(exp.Table)
            if table.name
        )

