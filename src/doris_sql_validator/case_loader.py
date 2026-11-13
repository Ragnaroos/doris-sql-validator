from __future__ import annotations

from pathlib import Path

import yaml
from pydantic import ValidationError

from .models import (
    CaseDefinition,
    CaseFile,
    LoadedCaseFile,
)


class CaseFileError(ValueError):
    pass


def load_case_file(path: Path) -> LoadedCaseFile:
    resolved = path.resolve()
    try:
        document = yaml.safe_load(resolved.read_text(encoding="utf-8"))
    except (OSError, yaml.YAMLError) as exc:
        raise CaseFileError(f"Cannot read case file {resolved}: {exc}") from exc

    try:
        case_file = CaseFile.model_validate(document)
    except ValidationError as exc:
        raise CaseFileError(f"{resolved} is invalid:\n{exc}") from exc
    return LoadedCaseFile(definition=case_file, path=resolved)


def load_cases(path: Path) -> list[CaseDefinition]:
    """Compatibility helper for callers that only need Case objects."""
    return load_case_file(path).definition.cases


def write_case_file(case_file: CaseFile, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    payload = case_file.model_dump(mode="json", exclude_none=True)
    path.write_text(
        yaml.dump(
            payload,
            Dumper=_LiteralSafeDumper,
            allow_unicode=True,
            sort_keys=False,
        ),
        encoding="utf-8",
    )


class _LiteralSafeDumper(yaml.SafeDumper):
    pass


def _represent_string(dumper: yaml.SafeDumper, value: str):
    style = "|" if "\n" in value else None
    return dumper.represent_scalar("tag:yaml.org,2002:str", value, style=style)


_LiteralSafeDumper.add_representer(str, _represent_string)
