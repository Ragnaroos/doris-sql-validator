from __future__ import annotations

from collections.abc import Sequence
from time import perf_counter
from typing import Any, Callable

from ..models import NormalizedError, QueryColumn, QueryResult
from ..normalization import canonical_type


def classify_error(exc: Exception) -> NormalizedError:
    message = str(exc)
    lowered = message.lower()
    if "timeout" in lowered or "timed out" in lowered:
        category = "TIMEOUT"
    elif (
        "table" in lowered
        and any(
            marker in lowered
            for marker in ("doesn't exist", "does not exist", "not found")
        )
        or any(
            marker in lowered
            for marker in (
                "unknown table",
                "table or view not found",
            )
        )
    ):
        category = "TABLE_NOT_FOUND"
    elif (
        "database" in lowered
        and any(marker in lowered for marker in ("does not exist", "not found"))
        or any(
            marker in lowered
            for marker in ("unknown database", "no database selected")
        )
    ):
        category = "DATABASE_NOT_FOUND"
    elif any(
        marker in lowered
        for marker in (
            "permission denied",
            "access denied",
            "not authorized",
            "authorization",
        )
    ):
        category = "PERMISSION_DENIED"
    elif "parse" in lowered or "syntax" in lowered:
        category = "PARSE_ERROR"
    elif "function" in lowered and ("not" in lowered or "unknown" in lowered):
        category = "FUNCTION_NOT_FOUND"
    elif "cast" in lowered or "convert" in lowered:
        category = "CAST_ERROR"
    elif "connect" in lowered or "connection" in lowered:
        category = "CONNECTION_ERROR"
    else:
        category = "EXECUTION_ERROR"
    code = None
    if getattr(exc, "args", None) and exc.args and isinstance(exc.args[0], (int, str)):
        code = str(exc.args[0])
    return NormalizedError(category=category, message=message, code=code)


def execute_dbapi(
    *,
    engine: str,
    connect: Callable[[], Any],
    sql: str,
    type_name: Callable[[Any, Any | None], str | None],
) -> QueryResult:
    started = perf_counter()
    connection = None
    cursor = None
    try:
        connection = connect()
        cursor = connection.cursor()
        cursor.execute(sql)
        raw_description: Sequence[Sequence[Any]] = cursor.description or []
        raw_fields = getattr(getattr(cursor, "_result", None), "fields", ())
        columns = []
        for index, description in enumerate(raw_description):
            field = raw_fields[index] if index < len(raw_fields) else None
            database_type = type_name(
                description[1] if len(description) > 1 else None,
                field,
            )
            columns.append(
                QueryColumn(
                    name=str(description[0]),
                    database_type=database_type,
                    canonical_type=canonical_type(database_type),
                )
            )
        rows = [list(row) for row in cursor.fetchall()]
        return QueryResult(
            engine=engine,
            success=True,
            columns=columns,
            rows=rows,
            elapsed_ms=(perf_counter() - started) * 1000,
        )
    except Exception as exc:  # Adapter boundary intentionally normalizes driver errors.
        return QueryResult(
            engine=engine,
            success=False,
            error=classify_error(exc),
            elapsed_ms=(perf_counter() - started) * 1000,
        )
    finally:
        if cursor is not None:
            cursor.close()
        if connection is not None:
            connection.close()

