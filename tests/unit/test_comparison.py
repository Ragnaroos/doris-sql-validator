from doris_sql_validator.comparison import compare_results
from doris_sql_validator.models import (
    ComparisonSpec,
    NormalizedError,
    QueryColumn,
    QueryResult,
    SourceEvidence,
)


def _result(engine: str, rows: list[list[object]]) -> QueryResult:
    return QueryResult(
        engine=engine,
        success=True,
        columns=[QueryColumn(name="value", database_type="INT", canonical_type="integer")],
        rows=rows,
        elapsed_ms=1,
    )


def _source(rows: list[list[object]]) -> SourceEvidence:
    return SourceEvidence(mode="live_source", result=_result("hive", rows))


def test_multiset_preserves_duplicates_but_ignores_order() -> None:
    spec = ComparisonSpec(
        row_order="multiset",
        column_names="explicit_alias_only",
    )
    comparison = compare_results(
        _source([[1], [2], [1]]),
        _result("doris", [[2], [1], [1]]),
        spec,
        explicit_output_aliases=True,
        data_assurance="unverified",
    )
    assert comparison.equivalent is True


def test_multiset_detects_duplicate_count_difference() -> None:
    spec = ComparisonSpec(
        row_order="multiset",
        column_names="explicit_alias_only",
    )
    comparison = compare_results(
        _source([[1], [1]]),
        _result("doris", [[1], [2]]),
        spec,
        explicit_output_aliases=True,
        data_assurance="unverified",
    )
    assert comparison.observed_outcome == "ROW_VALUE_MISMATCH"
    assert comparison.semantic_assessment == "INCONCLUSIVE"


def test_float_review_applies_tolerance_to_unordered_rows() -> None:
    spec = ComparisonSpec(
        float_tolerance=1e-12,
        row_order="multiset",
        column_names="explicit_alias_only",
    )
    comparison = compare_results(
        _source([[1.0], [2.0]]),
        _result("doris", [[2.0 + 1e-13], [1.0 - 1e-13]]),
        spec,
        explicit_output_aliases=True,
        data_assurance="not_applicable",
    )
    assert comparison.equivalent is True


def test_missing_doris_table_is_environment_error() -> None:
    comparison = compare_results(
        _source([[1]]),
        QueryResult(
            engine="doris",
            success=False,
            error=NormalizedError(
                category="TABLE_NOT_FOUND",
                message="Table dsv.items does not exist",
            ),
        ),
        ComparisonSpec(row_order="multiset"),
        explicit_output_aliases=False,
        data_assurance="unverified",
    )

    assert comparison.observed_outcome == "TARGET_ENVIRONMENT_ERROR"
    assert any("external data-preparation" in cause for cause in comparison.possible_causes)


def test_postgres_recorded_boolean_matches_doris_wire_integer() -> None:
    source = SourceEvidence(
        mode="recorded_output",
        result=QueryResult(
            engine="postgres-recorded",
            success=True,
            columns=[QueryColumn(name="value", canonical_type="unknown")],
            rows=[["t"]],
        ),
        value_encoding="postgres_psql_text",
    )
    target = QueryResult(
        engine="doris",
        success=True,
        columns=[QueryColumn(name="value", canonical_type="boolean")],
        rows=[[1]],
    )

    comparison = compare_results(
        source,
        target,
        ComparisonSpec(row_order="multiset"),
        explicit_output_aliases=False,
        data_assurance="not_applicable",
    )

    assert comparison.observed_outcome == "MATCH"

