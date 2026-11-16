"""Offline consistency checks for the documented, database-independent examples."""
from collections import Counter
from pathlib import Path
import sqlite3

import pytest
import sqlglot
from sqlglot import exp

from doris_sql_validator.importing import ImportOptions, import_case_file
from doris_sql_validator.source_provider import RecordedOutputProvider


BASIC = Path(__file__).resolve().parents[2] / "examples/postgres/basic"


@pytest.mark.parametrize(
    ("source", "output", "count"),
    [("constant.sql", "constant.out", 1), ("queries.sql", "expected.out", 4)],
)
def test_public_recorded_examples_import_and_match_fixed_data(source, output, count):
    suite = import_case_file(
        BASIC / source,
        BASIC / "generated-test.yaml",
        ImportOptions(
            input_format="pg-regress",
            dialect="postgres",
            source_engine="postgres",
            source_connection_profile="postgres-local",
            recorded_output=BASIC / output,
        ),
    )
    assert len(suite.cases) == count
    assert suite.import_summary.errors == 0
    provider = RecordedOutputProvider(
        suite.recorded_output, base_dir=BASIC, dialect="postgres"
    )
    # SQLite checks only the portable sample data/expected rows offline.
    # It is not evidence for PostgreSQL/Doris runtime compatibility.
    with sqlite3.connect(":memory:") as connection:
        connection.execute(
            "CREATE TABLE validation_demo_items(id INTEGER, category TEXT, amount INTEGER)"
        )
        connection.executemany(
            "INSERT INTO validation_demo_items VALUES (?, ?, ?)",
            [(1, "a", 10), (2, "a", 20), (2, "a", 20), (3, "b", 0), (4, "b", None)],
        )
        for case in suite.cases:
            reference = provider.get_result(case).result
            assert reference.success
            rows = [tuple(str(value) for value in row) for row in connection.execute(case.sql)]
            recorded = [tuple(row) for row in reference.rows]
            assert Counter(rows) == Counter(recorded)
            if sqlglot.parse_one(case.sql, read="postgres").args.get("order"):
                assert rows == recorded
            # The default SQLGlot generator must accept the quick-start queries.
            assert sqlglot.transpile(
                case.sql, read="postgres", write="doris", unsupported_level=sqlglot.ErrorLevel.RAISE
            )


def test_public_setup_scripts_preserve_same_rows_and_duplicates():
    source_sql = "\n".join(
        line for line in (BASIC / "postgres-setup.sql").read_text().splitlines()
        if not line.startswith("\\")
    )
    target_sql = (BASIC / "doris-setup.sql").read_text()
    datasets = []
    for text, dialect in [(source_sql, "postgres"), (target_sql, "doris")]:
        inserts = [node for node in sqlglot.parse(text, read=dialect) if isinstance(node, exp.Insert)]
        assert len(inserts) == 1
        values = inserts[0].expression
        assert isinstance(values, exp.Values)
        datasets.append([tuple(value.sql() for value in row.expressions) for row in values.expressions])
    assert datasets[0] == datasets[1]
    assert len(datasets[0]) == 5
    assert Counter(datasets[0])[("2", "'a'", "20")] == 2


def test_public_live_example_has_no_recorded_source():
    suite = import_case_file(
        BASIC / "queries.sql",
        BASIC / "generated-test-live.yaml",
        ImportOptions(
            input_format="pg-regress",
            dialect="postgres",
            source_engine="postgres",
            source_connection_profile="postgres-local",
            source_database="dsv_demo",
            target_database="dsv_demo",
        ),
    )
    assert suite.recorded_output is None
    assert len(suite.cases) == 4
    assert suite.source.database == suite.target.database == "dsv_demo"
