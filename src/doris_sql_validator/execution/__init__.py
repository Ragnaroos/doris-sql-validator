from __future__ import annotations

from .base import ExecutionAdapter
from .doris import DorisAdapter
from .hive import HiveAdapter
from .postgres import PostgresAdapter


def create_adapter(engine: str) -> ExecutionAdapter:
    normalized = engine.lower()
    if normalized == "doris":
        return DorisAdapter()
    if normalized == "hive":
        return HiveAdapter()
    if normalized in {"postgres", "postgresql", "pg"}:
        return PostgresAdapter()
    raise ValueError(f"No execution adapter registered for engine {engine!r}")


__all__ = [
    "DorisAdapter",
    "ExecutionAdapter",
    "HiveAdapter",
    "PostgresAdapter",
    "create_adapter",
]
