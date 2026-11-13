from __future__ import annotations

import os
from dataclasses import dataclass
from typing import Any

from pyhive import hive

from ..models import QueryResult
from .base import ExecutionAdapter
from .common import execute_dbapi


@dataclass(frozen=True)
class HiveSettings:
    host: str = "127.0.0.1"
    port: int = 10000
    username: str = "hive"
    database: str = "default"

    @classmethod
    def from_env(cls) -> "HiveSettings":
        return cls(
            host=os.getenv("HIVE_HOST", "127.0.0.1"),
            port=int(os.getenv("HIVE_PORT", "10000")),
            username=os.getenv("HIVE_USERNAME", "hive"),
            database=os.getenv("HIVE_DATABASE", "default"),
        )


class HiveAdapter(ExecutionAdapter):
    def __init__(self, settings: HiveSettings | None = None) -> None:
        self.settings = settings or HiveSettings.from_env()

    def connect(self, *, database: str | None = None) -> Any:
        return hive.connect(
            host=self.settings.host,
            port=self.settings.port,
            username=self.settings.username,
            database=database or self.settings.database,
            auth="NONE",
        )

    def execute_select(self, sql: str, *, database: str | None = None) -> QueryResult:
        return execute_dbapi(
            engine="hive",
            connect=lambda: self.connect(database=database),
            # HiveServer2's DBAPI endpoint expects the statement terminator to
            # be removed, unlike the interactive Beeline client.
            sql=sql.rstrip().removesuffix(";").rstrip(),
            type_name=lambda value, _field: str(value) if value is not None else None,
        )

