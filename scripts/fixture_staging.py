"""Stage unchanged modules for the existing warm compiler drivers."""

import shutil
from collections.abc import Sequence
from pathlib import Path

import click

from tests.integration.fixture_names import fixture_module_name


def stage_fixture_modules(
    *,
    fixtures: Sequence[Path],
    workspace: Path,
    default_module_name: str,
) -> list[str]:
    """Copy modules under their declared identifiers and report their
    paths.
    """
    names: list[str] = []
    for fixture in fixtures:
        name = (
            default_module_name
            if fixture.parent.name == "default_module_names"
            else fixture_module_name(golden_path=fixture)
        )
        destination = workspace / f"{name}{fixture.suffix}"
        _ = shutil.copyfile(src=fixture, dst=destination)
        click.echo(message=f"{destination.name} <- {fixture}")
        names.append(name)
    return names
