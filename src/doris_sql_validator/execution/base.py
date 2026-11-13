from __future__ import annotations

from abc import ABC, abstractmethod

from ..models import QueryResult


class ExecutionAdapter(ABC):
    @abstractmethod
    def execute_select(self, sql: str, *, database: str | None = None) -> QueryResult:
        raise NotImplementedError

    def healthcheck(self) -> QueryResult:
        return self.execute_select("SELECT 1 AS value")

