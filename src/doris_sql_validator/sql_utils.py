from __future__ import annotations

import hashlib

import sqlglot
from sqlglot import expressions as exp
from sqlglot.errors import ErrorLevel


FORBIDDEN_QUERY_NODES = (
    exp.Insert,
    exp.Update,
    exp.Delete,
    exp.Create,
    exp.Drop,
    exp.Alter,
    exp.Command,
    exp.Merge,
)


def parse_read_only_query(sql: str, dialect: str) -> exp.Query:
    statements = sqlglot.parse(sql, read=dialect, error_level=ErrorLevel.RAISE)
    if len(statements) != 1 or not isinstance(statements[0], exp.Query):
        actual = type(statements[0]).__name__ if len(statements) == 1 else len(statements)
        raise ValueError(f"Expected one read-only Query, got {actual}")
    expression = statements[0]
    for node_type in FORBIDDEN_QUERY_NODES:
        if expression.find(node_type):
            raise ValueError(f"Forbidden AST node: {node_type.__name__}")
    return expression


def normalized_sql(sql: str, dialect: str) -> str:
    return parse_read_only_query(sql, dialect).sql(
        dialect=dialect,
        pretty=False,
        comments=False,
    )


def sql_sha256(sql: str, dialect: str) -> str:
    return hashlib.sha256(normalized_sql(sql, dialect).encode("utf-8")).hexdigest()


def file_sha256(content: bytes) -> str:
    return hashlib.sha256(content).hexdigest()
