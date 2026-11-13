from __future__ import annotations

from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
from pathlib import Path
import re
import subprocess

import sqlglot
from sqlglot.errors import ParseError

from .comparison import compare_results
from .execution.base import ExecutionAdapter
from .models import (
    CaseDefinition,
    CaseFile,
    CaseRunReport,
    ComparisonSpec,
    SuiteReport,
)
from .source_provider import SourceEvidenceError, SourceResultProvider
from .transpiler import SqlglotTranspiler


class ValidationService:
    def __init__(
        self,
        case_file: CaseFile,
        target: ExecutionAdapter,
        *,
        source_provider: SourceResultProvider | None = None,
        transpiler: SqlglotTranspiler | None = None,
    ) -> None:
        self.case_file = case_file
        self.target = target
        self.source_provider = source_provider
        self.transpiler = transpiler or SqlglotTranspiler()

    def run_suite(self, cases: list[CaseDefinition]) -> SuiteReport:
        started_at = datetime.now(timezone.utc)
        reports = [self.run_case(case) for case in cases]
        return SuiteReport(
            started_at=started_at,
            finished_at=datetime.now(timezone.utc),
            sqlglot_version=sqlglot.__version__,
            sqlglot_commit=_sqlglot_commit(),
            source=self.case_file.source,
            target=self.case_file.target,
            input=self.case_file.input,
            validation_mode=self.case_file.validation_mode,
            import_summary=self.case_file.import_summary,
            import_diagnostics=self.case_file.import_diagnostics,
            recorded_output=self.case_file.recorded_output,
            cases=reports,
        )

    def run_case(self, case: CaseDefinition) -> CaseRunReport:
        mode = self.case_file.validation_mode
        try:
            transpilation = self.transpiler.transpile_case(
                case,
                source_dialect=self.case_file.source.dialect,
                target_dialect=self.case_file.target.dialect,
            )
        except Exception as exc:
            return CaseRunReport(
                id=case.id,
                validation_mode=mode,
                data_assurance="unverified",
                status="TRANSLATION_FAILED",
                source_sql=case.sql.strip(),
                failure_stage="source_parse" if isinstance(exc, ParseError) else "transpilation",
                transpilation_error=re.sub(r"\x1b\[[0-9;]*m", "", f"{type(exc).__name__}: {exc}"),
            )

        data_assurance = (
            "unverified" if transpilation.table_backed else "not_applicable"
        )
        if self.source_provider is None:
            return self._source_failure(
                case,
                data_assurance,
                transpilation.target_sql,
                "SourceResultProvider is required for semantic validation",
            )

        try:
            with ThreadPoolExecutor(max_workers=2, thread_name_prefix="validator") as pool:
                source_future = pool.submit(self.source_provider.get_result, case)
                target_future = pool.submit(
                    self.target.execute_select,
                    transpilation.target_sql,
                    database=self.case_file.target.database,
                )
                source_evidence = source_future.result()
                target_result = target_future.result()
        except SourceEvidenceError as exc:
            return self._source_failure(
                case,
                data_assurance,
                transpilation.target_sql,
                str(exc),
            )

        comparison = compare_results(
            source_evidence,
            target_result,
            ComparisonSpec(
                row_order=(
                    "ordered" if transpilation.ordered_result else "multiset"
                )
            ),
            explicit_output_aliases=transpilation.explicit_output_aliases,
            data_assurance=data_assurance,
        )
        return CaseRunReport(
            id=case.id,
            validation_mode=mode,
            data_assurance=data_assurance,
            status="COMPLETED",
            source_sql=transpilation.source_sql,
            target_sql=transpilation.target_sql,
            source_evidence=source_evidence,
            target_result=target_result,
            comparison=comparison,
        )

    def _source_failure(
        self,
        case: CaseDefinition,
        data_assurance: str,
        target_sql: str,
        message: str,
    ) -> CaseRunReport:
        return CaseRunReport(
            id=case.id,
            validation_mode=self.case_file.validation_mode,
            data_assurance=data_assurance,
            status="SOURCE_EVIDENCE_FAILED",
            source_sql=case.sql.strip(),
            target_sql=target_sql,
            source_evidence_error=message,
        )


def _sqlglot_commit() -> str | None:
    package_dir = Path(sqlglot.__file__).resolve().parent
    try:
        return subprocess.check_output(
            ["git", "-C", str(package_dir), "rev-parse", "HEAD"],
            text=True,
            stderr=subprocess.DEVNULL,
            timeout=2,
        ).strip()
    except (OSError, subprocess.SubprocessError):
        return None
