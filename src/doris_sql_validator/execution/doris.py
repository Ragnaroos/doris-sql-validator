from __future__ import annotations

import os
from dataclasses import dataclass
from typing import Any

import pymysql
from pymysql.constants import FIELD_TYPE

from ..models import QueryResult
from .base import ExecutionAdapter
from .common import execute_dbapi


# PyMySQL exposes aliases with the same numeric value (for example TINY/CHAR
# and ENUM/INTERVAL). A reversed vars() mapping therefore produces false type
# names. Keep the wire-protocol names explicit and deterministic.
_MYSQL_TYPE_NAMES = {
    FIELD_TYPE.DECIMAL: "DECIMAL",
    FIELD_TYPE.TINY: "TINYINT",
    FIELD_TYPE.SHORT: "SMALLINT",
    FIELD_TYPE.LONG: "INT",
    FIELD_TYPE.FLOAT: "FLOAT",
    FIELD_TYPE.DOUBLE: "DOUBLE",
    FIELD_TYPE.NULL: "NULL",
    FIELD_TYPE.TIMESTAMP: "TIMESTAMP",
    FIELD_TYPE.LONGLONG: "BIGINT",
    FIELD_TYPE.INT24: "MEDIUMINT",
    FIELD_TYPE.DATE: "DATE",
    FIELD_TYPE.TIME: "TIME",
    FIELD_TYPE.DATETIME: "DATETIME",
    FIELD_TYPE.YEAR: "YEAR",
    FIELD_TYPE.NEWDATE: "NEWDATE",
    FIELD_TYPE.VARCHAR: "VARCHAR",
    FIELD_TYPE.BIT: "BIT",
    FIELD_TYPE.JSON: "JSON",
    FIELD_TYPE.NEWDECIMAL: "DECIMAL",
    FIELD_TYPE.ENUM: "ENUM",
    FIELD_TYPE.SET: "SET",
    FIELD_TYPE.TINY_BLOB: "TINY_BLOB",
    FIELD_TYPE.MEDIUM_BLOB: "MEDIUM_BLOB",
    FIELD_TYPE.LONG_BLOB: "LONG_BLOB",
    FIELD_TYPE.BLOB: "BLOB",
    FIELD_TYPE.VAR_STRING: "VAR_STRING",
    FIELD_TYPE.STRING: "STRING",
    FIELD_TYPE.GEOMETRY: "GEOMETRY",
}


def _doris_type_name(value: Any, field: Any | None) -> str | None:
    if value is None:
        return None
    name = _MYSQL_TYPE_NAMES.get(value, str(value))
    charset_number = getattr(field, "charsetnr", None)
    if name in {"TINY_BLOB", "MEDIUM_BLOB", "LONG_BLOB", "BLOB"}:
        # MySQL protocol uses BLOB type codes for Doris STRING. Charset 63 is
        # binary; a text charset identifies a logical string value.
        return "BINARY" if charset_number == 63 else "STRING"
    if name == "TINYINT" and getattr(field, "length", None) == 1:
        # Doris BOOLEAN is a TINYINT alias on the MySQL wire and is reported
        # with display length 1. Real TINYINT columns use a wider length.
        return "BOOLEAN"
    return name


@dataclass(frozen=True)
class DorisSettings:
    host: str = "127.0.0.1"
    port: int = 9030
    username: str = "root"
    password: str = ""
    database: str | None = None

    @classmethod
    def from_env(cls) -> "DorisSettings":
        return cls(
            host=os.getenv("DORIS_HOST", "127.0.0.1"),
            port=int(os.getenv("DORIS_PORT", "9030")),
            username=os.getenv("DORIS_USERNAME", "root"),
            password=os.getenv("DORIS_PASSWORD", ""),
            database=os.getenv("DORIS_DATABASE") or None,
        )


class DorisAdapter(ExecutionAdapter):
    def __init__(self, settings: DorisSettings | None = None) -> None:
        self.settings = settings or DorisSettings.from_env()

    def connect(self, *, database: str | None = None) -> Any:
        return pymysql.connect(
            host=self.settings.host,
            port=self.settings.port,
            user=self.settings.username,
            password=self.settings.password,
            database=database or self.settings.database,
            charset="utf8mb4",
            connect_timeout=10,
            read_timeout=60,
            write_timeout=60,
            autocommit=True,
        )

    def execute_select(self, sql: str, *, database: str | None = None) -> QueryResult:
        return execute_dbapi(
            engine="doris",
            connect=lambda: self.connect(database=database),
            sql=sql,
            type_name=_doris_type_name,
        )

