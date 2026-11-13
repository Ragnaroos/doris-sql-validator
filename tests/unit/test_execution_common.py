from doris_sql_validator.execution.common import classify_error


def test_error_classifier_distinguishes_missing_database_and_table() -> None:
    database = classify_error(RuntimeError("Unknown database 'missing_db'"))
    table = classify_error(
        RuntimeError("Table 'dsv_validation.missing_table' doesn't exist")
    )
    doris_table = classify_error(
        RuntimeError(
            "Table [MISSING_TABLE] does not exist in database [dsv_validation]"
        )
    )

    assert database.category == "DATABASE_NOT_FOUND"
    assert table.category == "TABLE_NOT_FOUND"
    assert doris_table.category == "TABLE_NOT_FOUND"


def test_missing_function_is_not_misclassified_as_missing_table() -> None:
    error = classify_error(RuntimeError("FUNCTION missing_function does not exist"))

    assert error.category == "FUNCTION_NOT_FOUND"
