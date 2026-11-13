from __future__ import annotations

import os
from dataclasses import dataclass
from typing import Any

from ..models import QueryResult
from .base import ExecutionAdapter
from .common import execute_dbapi


_POSTGRES_OID_NAMES = {
    16: "BOOLEAN",
    17: "BYTEA",
    20: "BIGINT",
    21: "SMALLINT",
    23: "INTEGER",
    25: "TEXT",
    700: "REAL",
    701: "DOUBLE PRECISION",
    1042: "CHAR",
    1043: "VARCHAR",
    1082: "DATE",
    1083: "TIME",
    1114: "TIMESTAMP",
    1184: "TIMESTAMPTZ",
    1700: "NUMERIC",
    114: "JSON",
    3802: "JSONB",
}


@dataclass(frozen=True)
class PostgresSettings:
    host: str = "127.0.0.1"
    port: int = 5432
    username: str = "postgres"
    password: str = ""
    database: str = "postgres"

    @classmethod
    def from_env(cls) -> "PostgresSettings":
        return cls(
            host=os.getenv("POSTGRES_HOST", "127.0.0.1"),
            port=int(os.getenv("POSTGRES_PORT", "5432")),
            username=os.getenv("POSTGRES_USERNAME", "postgres"),
            password=os.getenv("POSTGRES_PASSWORD", ""),
            database=os.getenv("POSTGRES_DATABASE", "postgres"),
        )


class PostgresAdapter(ExecutionAdapter):
    def __init__(self, settings: PostgresSettings | None = None) -> None:
        self.settings = settings or PostgresSettings.from_env()

    def connect(self, *, database: str | None = None) -> Any:
        try:
            import psycopg
        except ImportError as exc:
            raise RuntimeError(
                "PostgreSQL live mode requires the psycopg package"
            ) from exc
        return psycopg.connect(
            host=self.settings.host,
            port=self.settings.port,
            user=self.settings.username,
            password=self.settings.password,
            dbname=database or self.settings.database,
            connect_timeout=10,
            autocommit=True,
        )

    def execute_select(self, sql: str, *, database: str | None = None) -> QueryResult:
        return execute_dbapi(
            engine="postgres",
            connect=lambda: self.connect(database=database),
            sql=sql,
            type_name=lambda value, _field: _POSTGRES_OID_NAMES.get(
                int(value), str(value)
            )
            if value is not None
            else None,
        )
