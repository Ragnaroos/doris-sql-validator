from __future__ import annotations

import hashlib
import json
import math
from collections import Counter
from datetime import date, datetime, time
from decimal import Decimal
from typing import Any

from .models import ComparisonResult, ComparisonSpec, QueryResult, SourceEvidence
from .normalization import normalize_value, stable_key


def compare_results(
    source: SourceEvidence,
    target: QueryResult,
    spec: ComparisonSpec,
    *,
    explicit_output_aliases: bool,
    data_assurance: str,
) -> ComparisonResult:
    source_result = source.result
    capabilities = source.capabilities
    if source_result.success != target.success:
        details = [
            f"source_success={source_result.success}",
            f"doris_success={target.success}",
        ]
        details.extend(_error_details("source", source_result))
        details.extend(_error_details("doris", target))
        outcome, summary = _execution_mismatch_outcome(source_result, target)
        return _failure(
            outcome,
            summary,
            details,
            data_assurance,
        )

    if not source_result.success:
        source_category = source_result.error.category if source_result.error else "UNKNOWN"
        target_category = target.error.category if target.error else "UNKNOWN"
        if _is_environment_error(source_category) or _is_environment_error(
            target_category
        ):
            return _failure(
                "ENVIRONMENT_ERROR",
                "Both sides failed and at least one failure is an environment or missing-object error",
                _error_details("source", source_result)
                + _error_details("doris", target),
                data_assurance,
            )
        if capabilities.error_category and source_category != target_category:
            return _failure(
                "ERROR_BEHAVIOR_MISMATCH",
                "Both sides failed, but normalized error categories differ",
                _error_details("source", source_result)
                + _error_details("doris", target),
                data_assurance,
            )
        return _match(
            source,
            "Both sides failed with compatible recorded/live error behavior",
        )

    if capabilities.column_count and len(source_result.columns) != len(target.columns):
        return _failure(
            "RESULT_SCHEMA_MISMATCH",
            "Result column counts differ",
            [f"source={len(source_result.columns)}", f"doris={len(target.columns)}"],
            data_assurance,
        )

    compare_names = capabilities.column_names and (
        spec.column_names == "strict"
        or (spec.column_names == "explicit_alias_only" and explicit_output_aliases)
    )
    schema_differences: list[str] = []
    for index, (source_column, target_column) in enumerate(
        zip(source_result.columns, target.columns, strict=False)
    ):
        if compare_names and source_column.name.lower() != target_column.name.lower():
            schema_differences.append(
                f"column[{index}] name: source={source_column.name!r}, "
                f"doris={target_column.name!r}"
            )
        if capabilities.column_types and not _compatible_type(
            source_column.canonical_type, target_column.canonical_type
        ):
            schema_differences.append(
                f"column[{index}] type: source={source_column.canonical_type}, "
                f"doris={target_column.canonical_type}"
            )
    if schema_differences:
        return _failure(
            "RESULT_SCHEMA_MISMATCH",
            "Canonical result schemas differ",
            schema_differences,
            data_assurance,
        )

    if capabilities.row_count and len(source_result.rows) != len(target.rows):
        return _failure(
            "ROW_COUNT_MISMATCH",
            "Result row counts differ",
            [f"source={len(source_result.rows)}", f"doris={len(target.rows)}"],
            data_assurance,
        )

    if capabilities.row_values == "unavailable":
        return ComparisonResult(
            observed_outcome="MATCH",
            semantic_assessment="INCONCLUSIVE",
            equivalent=None,
            summary="Available status/schema evidence matches, but row values are unavailable",
            details=["row_values=NOT_AVAILABLE"],
        )

    source_rows = _prepare_source_rows(source)
    target_rows = _prepare_target_rows(target, source.value_encoding)
    row_order = "multiset" if spec.row_order == "auto" else spec.row_order
    if row_order == "multiset":
        if spec.float_tolerance is not None and source.value_encoding == "canonical_typed":
            equal = _approximate_multiset_equal(
                source_rows,
                target_rows,
                tolerance=spec.float_tolerance,
            )
        else:
            equal = Counter(stable_key(row) for row in source_rows) == Counter(
                stable_key(row) for row in target_rows
            )
    else:
        equal = _rows_equal(
            source_rows,
            target_rows,
            tolerance=(
                spec.float_tolerance
                if source.value_encoding == "canonical_typed"
                else None
            ),
        )

    if not equal:
        return _failure(
            "ROW_VALUE_MISMATCH",
            "Normalized result row values differ",
            [
                f"source_digest={result_digest(source_rows)}",
                f"doris_digest={result_digest(target_rows)}",
                f"source_sample={source_rows[:5]!r}",
                f"doris_sample={target_rows[:5]!r}",
            ],
            data_assurance,
        )
    return _match(
        source,
        "Execution status, available schema evidence, and rows match",
        details=[
            f"source_digest={result_digest(source_rows)}",
            f"doris_digest={result_digest(target_rows)}",
        ],
    )


def result_digest(rows: list[Any]) -> str:
    digest = hashlib.sha256()
    for encoded in sorted(stable_key(row) for row in rows):
        payload = encoded.encode("utf-8")
        digest.update(len(payload).to_bytes(8, "big"))
        digest.update(payload)
    return digest.hexdigest()


def _prepare_source_rows(source: SourceEvidence) -> list[Any]:
    if source.value_encoding == "canonical_typed":
        return [[normalize_value(value) for value in row] for row in source.result.rows]
    return [[str(value) for value in row] for row in source.result.rows]


def _prepare_target_rows(result: QueryResult, encoding: str) -> list[Any]:
    if encoding == "canonical_typed":
        return [[normalize_value(value) for value in row] for row in result.rows]
    return [
        [
            _display_value(
                value,
                encoding,
                canonical_type=(
                    result.columns[index].canonical_type
                    if index < len(result.columns)
                    else "unknown"
                ),
            )
            for index, value in enumerate(row)
        ]
        for row in result.rows
    ]


def _display_value(value: Any, encoding: str, *, canonical_type: str) -> str:
    if value is None:
        return "NULL" if encoding == "hive_qtest_text" else ""
    if canonical_type == "boolean" and value in {0, 1, False, True}:
        boolean = bool(value)
        if encoding == "postgres_psql_text":
            return "t" if boolean else "f"
        return "true" if boolean else "false"
    if isinstance(value, bool):
        if encoding == "postgres_psql_text":
            return "t" if value else "f"
        return "true" if value else "false"
    if isinstance(value, bytes):
        if encoding == "postgres_psql_text":
            return "\\x" + value.hex()
        try:
            return value.decode("utf-8")
        except UnicodeDecodeError:
            return value.hex()
    if isinstance(value, Decimal):
        return format(value, "f")
    if isinstance(value, datetime):
        return value.isoformat(sep=" ")
    if isinstance(value, (date, time)):
        return value.isoformat()
    if isinstance(value, float):
        if math.isnan(value):
            return "NaN"
        if math.isinf(value):
            return "Infinity" if value > 0 else "-Infinity"
        return str(value)
    if isinstance(value, (list, dict, tuple)):
        return json.dumps(value, ensure_ascii=False, sort_keys=True, default=str)
    return str(value)


def _rows_equal(
    source: list[Any],
    target: list[Any],
    *,
    tolerance: float | None,
) -> bool:
    if len(source) != len(target):
        return False
    return all(
        _value_equal(left, right, tolerance=tolerance)
        for left, right in zip(source, target, strict=True)
    )


def _approximate_multiset_equal(
    source: list[Any],
    target: list[Any],
    *,
    tolerance: float,
) -> bool:
    if len(source) != len(target):
        return False
    unmatched = list(target)
    for source_row in source:
        for index, target_row in enumerate(unmatched):
            if _value_equal(source_row, target_row, tolerance=tolerance):
                unmatched.pop(index)
                break
        else:
            return False
    return not unmatched


def _value_equal(left: Any, right: Any, *, tolerance: float | None) -> bool:
    if tolerance is not None and isinstance(left, float) and isinstance(right, float):
        return math.isclose(left, right, rel_tol=tolerance, abs_tol=tolerance)
    if isinstance(left, list) and isinstance(right, list):
        return _rows_equal(left, right, tolerance=tolerance)
    if isinstance(left, dict) and isinstance(right, dict):
        if left.keys() != right.keys():
            return False
        return all(
            _value_equal(left[key], right[key], tolerance=tolerance) for key in left
        )
    return left == right


def _compatible_type(source: str, target: str) -> bool:
    if source == "unknown" or target == "unknown":
        return True
    if source == target:
        return True
    return source.startswith("decimal") and target.startswith("decimal")


def _failure(
    outcome: str,
    summary: str,
    details: list[str],
    data_assurance: str,
) -> ComparisonResult:
    assessment = (
        "DIFFERENT_FOR_CONSTANT_QUERY"
        if data_assurance == "not_applicable"
        else "INCONCLUSIVE"
    )
    return ComparisonResult(
        observed_outcome=outcome,
        semantic_assessment=assessment,
        equivalent=False,
        summary=summary,
        details=details,
        possible_causes=_possible_causes(outcome, data_assurance),
    )


def _error_details(prefix: str, result: QueryResult) -> list[str]:
    if result.success or result.error is None:
        return []
    details = [
        f"{prefix}_error_category={result.error.category}",
        f"{prefix}_error_message={result.error.message}",
    ]
    if result.error.code:
        details.append(f"{prefix}_error_code={result.error.code}")
    return details


def _possible_causes(outcome: str, data_assurance: str) -> list[str]:
    causes: dict[str, list[str]] = {
        "EXECUTION_STATUS_MISMATCH": [
            "One engine may not support the function, syntax, or data type used by its SQL.",
            "Source and Doris session, UDF, permission, or version settings may differ.",
            "The SQLGlot-generated SQL may be incompatible with the target Doris version.",
        ],
        "TARGET_ENVIRONMENT_ERROR": [
            "The Doris database or table may not have been created by the external data-preparation process.",
            "Doris connection, permission, catalog, or database selection may be incorrect.",
            "The generated SQL may still reference a source-only database, catalog, or table name.",
        ],
        "SOURCE_ENVIRONMENT_ERROR": [
            "The source database, table, connection, permission, or session may not be prepared.",
            "The source SQL may depend on setup statements that the validator intentionally does not execute.",
        ],
        "ENVIRONMENT_ERROR": [
            "One or both execution environments are not prepared for this query.",
            "Required databases, tables, permissions, catalogs, or connections may be missing.",
        ],
        "ERROR_BEHAVIOR_MISMATCH": [
            "Source and Doris may classify the same invalid input differently.",
            "Error normalization may not yet map equivalent engine-specific errors.",
            "Source and Doris session, UDF, or version settings may differ.",
        ],
        "RESULT_SCHEMA_MISMATCH": [
            "Source and Doris may infer different return types for the expression.",
            "The SQLGlot rewrite may have changed the expression result type.",
            "Database-driver type normalization may be incomplete.",
        ],
        "ROW_COUNT_MISMATCH": [
            "Filter, join, grouping, or NULL semantics may differ.",
            "Source and Doris table data or schemas may differ.",
        ],
        "ROW_VALUE_MISMATCH": [
            "Function, cast, NULL, rounding, timezone, or complex-type semantics may differ.",
            "The SQLGlot rewrite may have changed expression semantics.",
            "Result normalization or Recorded Output text may have lost type information.",
        ],
    }
    result = list(
        causes.get(outcome, ["Source and Doris observable behavior differs."])
    )
    if data_assurance == "unverified" and outcome in {
        "ROW_COUNT_MISMATCH",
        "ROW_VALUE_MISMATCH",
        "RESULT_SCHEMA_MISMATCH",
    }:
        result.insert(
            0,
            "The validator did not prove that source and Doris table data and schemas match.",
        )
    return result


_ENVIRONMENT_ERROR_CATEGORIES = {
    "CONNECTION_ERROR",
    "DATABASE_NOT_FOUND",
    "TABLE_NOT_FOUND",
    "PERMISSION_DENIED",
    "TIMEOUT",
}


def _is_environment_error(category: str) -> bool:
    return category in _ENVIRONMENT_ERROR_CATEGORIES


def _execution_mismatch_outcome(
    source: QueryResult, target: QueryResult
) -> tuple[str, str]:
    source_category = source.error.category if source.error else "UNKNOWN"
    target_category = target.error.category if target.error else "UNKNOWN"
    if not target.success and _is_environment_error(target_category):
        return (
            "TARGET_ENVIRONMENT_ERROR",
            "Doris failed because its connection, permissions, database, or table environment is unavailable",
        )
    if not source.success and _is_environment_error(source_category):
        return (
            "SOURCE_ENVIRONMENT_ERROR",
            "The live source failed because its connection, permissions, database, or table environment is unavailable",
        )
    return (
        "EXECUTION_STATUS_MISMATCH",
        "Source evidence and Doris execution status differ",
    )


def _match(
    source: SourceEvidence,
    summary: str,
    *,
    details: list[str] | None = None,
) -> ComparisonResult:
    assessment = (
        "MATCHES_RECORDED_SOURCE_OUTPUT"
        if source.mode == "recorded_output"
        else "MATCH_ON_CURRENT_ENVIRONMENTS"
    )
    return ComparisonResult(
        observed_outcome="MATCH",
        semantic_assessment=assessment,
        equivalent=True,
        summary=summary,
        details=details or [],
    )
