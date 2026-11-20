from __future__ import annotations

from pathlib import Path
from typing import Protocol

from .execution.base import ExecutionAdapter
from .models import (
    CaseDefinition,
    EvidenceCapabilities,
    RecordedOutputSpec,
    SourceEvidence,
)
from .recorded_output import RecordedOutputError, parse_recorded_case


class SourceEvidenceError(RuntimeError):
    pass


class SourceResultProvider(Protocol):
    def get_result(self, case: CaseDefinition) -> SourceEvidence: ...


class LiveSourceResultProvider:
    def __init__(self, adapter: ExecutionAdapter, *, database: str | None = None) -> None:
        self.adapter = adapter
        self.database = database

    def get_result(self, case: CaseDefinition) -> SourceEvidence:
        return SourceEvidence(
            mode="live_source",
            result=self.adapter.execute_select(case.sql, database=self.database),
            capabilities=EvidenceCapabilities(),
            value_encoding="canonical_typed",
        )


class RecordedOutputProvider:
    def __init__(
        self,
        spec: RecordedOutputSpec,
        *,
        base_dir: Path,
        dialect: str,
    ) -> None:
        candidate = (base_dir / spec.file).resolve()
        # References may point outside the YAML directory. Read the current
        # file directly; pairing still uses SQL text and occurrence number.
        try:
            content = candidate.read_bytes()
        except OSError as exc:
            raise SourceEvidenceError(f"Cannot read recorded output {candidate}: {exc}") from exc
        self.spec = spec
        self.path = candidate
        self.text = content.decode("utf-8")
        self.dialect = dialect
        self._cache: dict[str, SourceEvidence] = {}

    def get_result(self, case: CaseDefinition) -> SourceEvidence:
        if case.id in self._cache:
            return self._cache[case.id]
        try:
            evidence = parse_recorded_case(
                output_format=self.spec.format,
                output_text=self.text,
                case=case,
                dialect=self.dialect,
                artifact=str(self.path),
            )
        except RecordedOutputError as exc:
            raise SourceEvidenceError(str(exc)) from exc
        self._cache[case.id] = evidence
        return evidence
