from pathlib import Path

from typer.testing import CliRunner

from doris_sql_validator.case_loader import load_case_file, write_case_file
from doris_sql_validator.cli import app
from doris_sql_validator.models import (
    CaseDefinition,
    CaseFile,
    ImportSummary,
    InputSpec,
    SourceSpec,
    TargetSpec,
)


runner = CliRunner()


def test_import_command_embeds_diagnostics_without_sidecar(tmp_path: Path) -> None:
    source = tmp_path / "queries.sql"
    output = tmp_path / "cases.yaml"
    source.write_text(
        "CREATE TABLE ignored (id INT);\nSELECT 1 AS value;\n",
        encoding="utf-8",
    )

    result = runner.invoke(
        app,
        [
            "import-cases",
            "--format",
            "raw-sql",
            "--dialect",
            "hive",
            "--input",
            str(source),
            "--output",
            str(output),
        ],
    )

    assert result.exit_code == 0, result.output
    definition = load_case_file(output).definition
    assert definition.import_summary.skipped == 1
    assert len(definition.import_diagnostics) == 1
    assert not output.with_suffix(".import.json").exists()


def test_run_without_recorded_output_or_source_profile_is_rejected(
    tmp_path: Path,
) -> None:
    path = tmp_path / "cases.yaml"
    case_file = CaseFile(
        source=SourceSpec(dialect="hive", engine="hive"),
        target=TargetSpec(),
        input=InputSpec(format="manual"),
        import_summary=ImportSummary(
            accepted=1, skipped=0, ambiguous=0, errors=0
        ),
        cases=[
            CaseDefinition(id="constant-one", statement_index=1, sql="SELECT 1")
        ],
    )
    write_case_file(case_file, path)

    result = runner.invoke(app, ["run", "--path", str(path)])

    assert result.exit_code == 2
    assert "Use the transpile command" in result.output
