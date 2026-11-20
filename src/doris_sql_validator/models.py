from __future__ import annotations

from datetime import datetime
from pathlib import Path
from typing import Any, Literal

from pydantic import BaseModel, ConfigDict, Field, model_validator


class StrictModel(BaseModel):
    model_config = ConfigDict(extra="forbid")


ValidationMode = Literal["live_source", "recorded_output"]


class ComparisonSpec(StrictModel):
    """Runtime comparison policy; it is deliberately not stored per Case."""

    row_order: Literal["ordered", "multiset"] = "multiset"
    float_tolerance: float | None = Field(default=1e-12, gt=0)
    column_names: Literal["explicit_alias_only", "ignore", "strict"] = (
        "explicit_alias_only"
    )


class SourceSpec(StrictModel):
    dialect: str
    engine: str
    connection_profile: str | None = None
    database: str | None = None


class TargetSpec(StrictModel):
    connection_profile: str = "doris-local"
    database: str | None = None

    @property
    def dialect(self) -> str:
        return "doris"

    @property
    def engine(self) -> str:
        return "doris"


class InputSpec(StrictModel):
    format: Literal["raw-sql", "pg-regress", "hive-qtest", "manual"]
    file: str | None = None
    sha256: str | None = Field(default=None, pattern=r"^[0-9a-f]{64}$")


class RecordedOutputSpec(StrictModel):
    format: Literal["pg-regress", "hive-qtest"]
    file: str
    driver: str | None = None


class ImportDiagnostic(StrictModel):
    statement_index: int = Field(ge=1)
    line_start: int = Field(ge=1)
    line_end: int = Field(ge=1)
    disposition: Literal["skipped", "ambiguous", "error"]
    statement_type: str
    reason: str
    case_id: str | None = None
    sql: str | None = None
    output_occurrence: int | None = None


class ImportSummary(StrictModel):
    accepted: int = Field(ge=0)
    skipped: int = Field(ge=0)
    ambiguous: int = Field(ge=0)
    errors: int = Field(ge=0)


class CaseDefinition(StrictModel):
    id: str = Field(pattern=r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
    statement_index: int = Field(ge=1)
    line_start: int | None = Field(default=None, ge=1)
    line_end: int | None = Field(default=None, ge=1)
    output_occurrence: int | None = Field(default=None, ge=1)
    sql: str = Field(min_length=1)

    @model_validator(mode="after")
    def validate_lines(self) -> "CaseDefinition":
        if (
            self.line_start is not None
            and self.line_end is not None
            and self.line_end < self.line_start
        ):
            raise ValueError("line_end must be greater than or equal to line_start")
        return self


class CaseFile(StrictModel):
    source: SourceSpec
    target: TargetSpec
    input: InputSpec
    recorded_output: RecordedOutputSpec | None = None
    import_summary: ImportSummary
    import_diagnostics: list[ImportDiagnostic] = Field(default_factory=list)
    cases: list[CaseDefinition]

    @property
    def validation_mode(self) -> ValidationMode:
        return "recorded_output" if self.recorded_output else "live_source"

    @model_validator(mode="after")
    def validate_cases(self) -> "CaseFile":
        if not self.cases:
            raise ValueError("No cases found")
        seen: set[str] = set()
        for case in self.cases:
            if case.id in seen:
                raise ValueError(f"Duplicate id {case.id!r}")
            seen.add(case.id)
            if self.recorded_output and case.output_occurrence is None:
                raise ValueError(
                    f"Case {case.id!r} requires output_occurrence when "
                    "recorded_output is configured"
                )
            if not self.recorded_output and case.output_occurrence is not None:
                raise ValueError(
                    f"Case {case.id!r} cannot define output_occurrence without "
                    "recorded_output"
                )
        if self.import_summary.accepted != len(self.cases):
            raise ValueError(
                "import_summary.accepted must equal the number of cases"
            )
        counts = {
            "skipped": sum(d.disposition == "skipped" for d in self.import_diagnostics),
            "ambiguous": sum(
                d.disposition == "ambiguous" for d in self.import_diagnostics
            ),
            "errors": sum(d.disposition == "error" for d in self.import_diagnostics),
        }
        for field, actual in counts.items():
            if getattr(self.import_summary, field) != actual:
                raise ValueError(
                    f"import_summary.{field}={getattr(self.import_summary, field)} "
                    f"does not match import_diagnostics count {actual}"
                )
        return self


class LoadedCaseFile(StrictModel):
    definition: CaseFile
    path: Path

    model_config = ConfigDict(extra="forbid", arbitrary_types_allowed=True)

    @property
    def base_dir(self) -> Path:
        return self.path.parent


class QueryColumn(StrictModel):
    name: str
    database_type: str | None = None
    canonical_type: str = "unknown"


class NormalizedError(StrictModel):
    category: str
    message: str
    code: str | None = None


class QueryResult(StrictModel):
    engine: str
    success: bool
    columns: list[QueryColumn] = Field(default_factory=list)
    rows: list[list[Any]] = Field(default_factory=list)
    error: NormalizedError | None = None
    elapsed_ms: float = 0
    query_id: str | None = None
    result_digest: str | None = None


class EvidenceCapabilities(StrictModel):
    execution_status: bool = True
    error_category: bool = True
    column_count: bool = True
    column_names: bool = True
    column_types: bool = True
    row_count: bool = True
    row_values: Literal["typed", "display_text", "unavailable"] = "typed"
    complex_types: bool = True


class SourceEvidence(StrictModel):
    mode: ValidationMode
    result: QueryResult
    capabilities: EvidenceCapabilities = Field(default_factory=EvidenceCapabilities)
    value_encoding: Literal[
        "canonical_typed", "postgres_psql_text", "hive_qtest_text"
    ] = "canonical_typed"
    artifact: str | None = None
    statement_index: int | None = None


class TranspilationResult(StrictModel):
    source_sql: str
    target_sql: str
    source_ast: str
    explicit_output_aliases: bool
    ordered_result: bool
    sqlglot_version: str
    source_dialect: str
    target_dialect: str
    table_backed: bool


class ComparisonResult(StrictModel):
    observed_outcome: str
    semantic_assessment: str
    equivalent: bool | None
    summary: str
    details: list[str] = Field(default_factory=list)
    possible_causes: list[str] = Field(default_factory=list)


class CaseRunReport(StrictModel):
    id: str
    validation_mode: ValidationMode
    data_assurance: Literal["not_applicable", "unverified"]
    status: Literal[
        "COMPLETED",
        "TRANSLATION_FAILED",
        "SOURCE_EVIDENCE_FAILED",
        "TARGET_EXECUTION_FAILED",
    ]
    source_sql: str
    failure_stage: Literal["source_parse", "transpilation"] | None = None
    target_sql: str | None = None
    transpilation_error: str | None = None
    source_evidence_error: str | None = None
    source_evidence: SourceEvidence | None = None
    target_result: QueryResult | None = None
    comparison: ComparisonResult | None = None
    difference: dict[str, Any] | None = None
    statement_index: int | None = None
    line_start: int | None = None
    line_end: int | None = None


class SuiteReport(StrictModel):
    started_at: datetime
    finished_at: datetime
    sqlglot_version: str
    sqlglot_commit: str | None = None
    source: SourceSpec
    target: TargetSpec
    input: InputSpec
    validation_mode: ValidationMode
    import_summary: ImportSummary
    import_diagnostics: list[ImportDiagnostic]
    recorded_output: RecordedOutputSpec | None = None
    cases: list[CaseRunReport]
    filtered: bool = False
