"""Project skill discovery, explicit-only invocation and local asset contracts."""
from pathlib import Path
import re

import pytest
import yaml


ROOT = Path(__file__).resolve().parents[2] / ".agents/skills"


@pytest.mark.parametrize("name", ["pg-doris-prepare-data", "pg-doris-attribute", "pg-doris-fix"])
def test_skill_metadata_and_referenced_assets(name):
    directory = ROOT / name
    source = (directory / "SKILL.md").read_text()
    frontmatter = source.split("---", 2)[1]
    assert yaml.safe_load(frontmatter)["name"] == name
    metadata = yaml.safe_load((directory / "agents/openai.yaml").read_text())
    assert metadata["policy"]["allow_implicit_invocation"] is False
    assert "$" + name in metadata["interface"]["default_prompt"]
    assets = re.findall(r"\]\((assets/[^)]+)\)", source)
    assert assets
    for asset in assets:
        assert (directory / asset).is_file(), asset
        assert (directory / asset).resolve().is_relative_to(directory.resolve())
