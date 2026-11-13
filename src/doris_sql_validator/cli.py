from __future__ import annotations

import hashlib
from pathlib import Path

import sqlglot
import typer
from dotenv import load_dotenv

from .case_loader import (
    CaseFileError,
    load_case_file,
    write_case_file,
)
from .execution import create_adapter
from .importing import ImportOptions, import_case_file
from .models import CaseDefinition
from .reporting import write_reports
from .handoff import prepare_pg_review
from .pg_probe import probe_postgres_case
from .service import ValidationService
from .source_provider import (
    LiveSourceResultProvider,
    RecordedOutputProvider,
    SourceEvidenceError,
)
from .transpiler import SqlglotTranspiler


PROJECT_DIR = Path(__file__).resolve().parents[2]
DEFAULT_CASE_FILE = PROJECT_DIR / "cases/hive/candidates/hive-doris-mvp.yaml"
app = typer.Typer(no_args_is_help=True, help="Multi-source SQL → Doris validator")


@app.callback()
def main() -> None:
    load_dotenv(PROJECT_DIR / ".env")


@app.command("cases-lint")
def cases_lint(
    path: Path = typer.Option(DEFAULT_CASE_FILE, exists=True, readable=True),
) -> None:
    try:
        loaded = load_case_file(path)
    except CaseFileError as exc:
        typer.echo(str(exc), err=True)
        raise typer.Exit(1) from exc
    definition = loaded.definition
    typer.echo(f"OK: {len(definition.cases)} unique cases")
    typer.echo(f"  evidence: {definition.validation_mode}")
    typer.echo(f"  source: {definition.source.dialect}/{definition.source.engine}")
    typer.echo(f"  target: {definition.target.dialect}/{definition.target.engine}")
    typer.echo(
        "  import: "
        f"accepted={definition.import_summary.accepted}, "
        f"skipped={definition.import_summary.skipped}, "
        f"ambiguous={definition.import_summary.ambiguous}, "
        f"errors={definition.import_summary.errors}"
    )


@app.command()
def transpile(
    sql: str,
    source_dialect: str = typer.Option("hive", "--source-dialect", "--read"),
) -> None:
    generated_id = f"adhoc-{hashlib.sha256(sql.encode('utf-8')).hexdigest()[:12]}"
    case = CaseDefinition(
        id=generated_id,
        statement_index=1,
        sql=sql,
    )
    result = SqlglotTranspiler().transpile_case(
        case,
        source_dialect=source_dialect,
        target_dialect="doris",
    )
    typer.echo(result.target_sql)


@app.command()
def doctor(source_engine: str = typer.Option("hive", "--source-engine")) -> None:
    typer.echo(f"SQLGlot {sqlglot.__version__} ({Path(sqlglot.__file__).resolve()})")
    failed = False
    for name, adapter in (
        (source_engine, create_adapter(source_engine)),
        ("doris", create_adapter("doris")),
    ):
        result = adapter.healthcheck()
        if result.success:
            typer.echo(f"{name}: OK ({result.elapsed_ms:.1f} ms)")
        else:
            failed = True
            typer.echo(f"{name}: FAILED - {result.error}", err=True)
    if failed:
        raise typer.Exit(1)


@app.command("import-cases")
def import_cases_command(
    input_path: Path = typer.Option(..., "--input", exists=True, readable=True),
    output_path: Path = typer.Option(..., "--output"),
    input_format: str = typer.Option(..., "--format"),
    dialect: str = typer.Option(..., "--dialect"),
    source_engine: str | None = typer.Option(None, "--source-engine"),
    source_connection_profile: str | None = typer.Option(
        None, "--source-connection-profile"
    ),
    target_connection_profile: str = typer.Option(
        "doris-local", "--target-connection-profile"
    ),
    source_database: str | None = typer.Option(None, "--source-database"),
    target_database: str | None = typer.Option(None, "--target-database"),
    recorded_output: Path | None = typer.Option(
        None, "--recorded-output", exists=True, readable=True
    ),
    qtest_driver: str | None = typer.Option(None, "--qtest-driver"),
) -> None:
    if recorded_output and input_format not in {"pg-regress", "hive-qtest"}:
        raise typer.BadParameter(
            "--recorded-output requires --format pg-regress or hive-qtest"
        )
    engine = source_engine or {
        "pg-regress": "postgres",
        "hive-qtest": "hive",
    }.get(input_format, dialect)
    try:
        case_file = import_case_file(
            input_path,
            output_path,
            ImportOptions(
                input_format=input_format,
                dialect=dialect,
                source_engine=engine,
                source_connection_profile=source_connection_profile,
                target_connection_profile=target_connection_profile,
                source_database=source_database,
                target_database=target_database,
                recorded_output=recorded_output,
                qtest_driver=qtest_driver,
            ),
        )
    except ValueError as exc:
        raise typer.BadParameter(str(exc)) from exc
    write_case_file(case_file, output_path)
    typer.echo(f"Cases: {output_path} ({len(case_file.cases)} accepted)")


@app.command("run")
def run_suite(
    path: Path = typer.Option(DEFAULT_CASE_FILE, exists=True, readable=True),
    ids: list[str] = typer.Option([], "--id", "--case-id"),
    output_dir: Path | None = typer.Option(None),
) -> None:
    loaded = load_case_file(path)
    definition = loaded.definition
    cases = definition.cases
    if ids:
        requested = set(ids)
        cases = [case for case in cases if case.id in requested]
        missing = requested - {case.id for case in cases}
        if missing:
            typer.echo(f"Unknown case IDs: {', '.join(sorted(missing))}", err=True)
            raise typer.Exit(2)

    target = create_adapter(definition.target.engine)
    provider = None
    try:
        if definition.validation_mode == "live_source":
            if definition.source.connection_profile is None:
                raise SourceEvidenceError(
                    "No Recorded Output or source connection profile is configured; "
                    "semantic validation is unavailable. Use the transpile command."
                )
            provider = LiveSourceResultProvider(
                create_adapter(definition.source.engine),
                database=definition.source.database,
            )
        else:
            assert definition.recorded_output is not None
            provider = RecordedOutputProvider(
                definition.recorded_output,
                base_dir=loaded.base_dir,
                dialect=definition.source.dialect,
            )
    except (ValueError, SourceEvidenceError) as exc:
        typer.echo(str(exc), err=True)
        raise typer.Exit(2) from exc

    report = ValidationService(
        definition,
        target,
        source_provider=provider,
    ).run_suite(cases)
    resolved_output_dir = output_dir or PROJECT_DIR / "reports" / path.stem
    json_path, markdown_path = write_reports(report, resolved_output_dir, case_file_path=loaded.path)
    typer.echo(f"JSON: {json_path}")
    typer.echo(f"Markdown: {markdown_path}")
    if any(
        case.status != "COMPLETED"
        or case.comparison is None
        or case.comparison.observed_outcome != "MATCH"
        for case in report.cases
    ):
        raise typer.Exit(1)


@app.command("prepare-pg-review")
def prepare_pg_review_command(
    path: Path = typer.Option(..., exists=True, readable=True, help="首轮使用的 PostgreSQL Case YAML"),
    report: Path = typer.Option(..., exists=True, readable=True, help="首轮 validation.json"),
    setup: list[Path] = typer.Option(..., exists=True, readable=True, help="建表、装数和数据依赖文件，可多次指定"),
    output_dir: Path = typer.Option(..., help="新的人工交接目录，非空时拒绝覆盖"),
    preparation_report: Path | None = typer.Option(None, exists=True, readable=True, help="外部数据准备 Skill 的报告，可选"),
) -> None:
    """离线生成原文件引用索引；不复制、不执行 SQL、不调用 AI。"""
    try:
        result = prepare_pg_review(path, report, output_dir, setup_files=setup, preparation_report=preparation_report)
    except (ValueError, OSError) as exc:
        typer.echo(str(exc), err=True)
        raise typer.Exit(2) from exc
    typer.echo(f"人工归因交接说明：{result}")


@app.command("probe-pg-case")
def probe_pg_case_command(
    path: Path = typer.Option(..., exists=True, readable=True, help="当前评估使用的 PostgreSQL YAML"),
    report: Path = typer.Option(..., exists=True, readable=True, help="对应的首轮 validation.json"),
    case_id: str = typer.Option(..., help="YAML 和首轮报告中已有的查询编号"),
    candidate: Path = typer.Option(..., exists=True, readable=True, help="人或 Agent 编写的单条只读 Doris 候选 SQL"),
    output_dir: Path = typer.Option(..., help="新的对照证据目录"),
    source_variant: Path | None = typer.Option(None, exists=True, readable=True, help="可选：明确提供一条 PostgreSQL 边界变体，不覆盖原 SQL"),
) -> None:
    """显式执行 PG/社区 Doris/独立 Doris 对照；不生成改写、不作最终归因。"""
    try:
        result = probe_postgres_case(path, report, case_id, candidate, output_dir, source_variant=source_variant)
    except (ValueError, OSError) as exc:
        typer.echo(str(exc), err=True)
        raise typer.Exit(2) from exc
    typer.echo(f"只读对照报告：{result}")


if __name__ == "__main__":
    app()
