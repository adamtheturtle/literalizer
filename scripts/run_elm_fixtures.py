"""Run the Elm formatter, compiler and runtime checks."""

import shutil
import subprocess
import sys
from pathlib import Path

import click

from scripts.check_elm_syntax import check_files
from scripts.run_elm import run_files
from tests.integration.list_fixtures import fixture_paths

_BOUNDED = Path(__file__).resolve().with_name(name="run-bounded.sh")


def _require(*, tool: str) -> str:
    """Locate a required native tool."""
    executable = shutil.which(cmd=tool)
    if executable is None:
        raise click.ClickException(
            message=f"The {tool} executable is required."
        )
    return executable


@click.command()
@click.argument("stage", type=click.Choice(choices=("lint", "run")))
def main(stage: str) -> None:
    """Lint or execute the complete Elm 0.19 fixture population."""
    _ = _require(tool="elm")
    fixtures = fixture_paths(extension=".elm")
    if len(fixtures) == 0:
        raise click.ClickException(message="No Elm fixtures.")
    filenames = tuple(str(object=fixture) for fixture in fixtures)
    if stage == "run":
        _ = _require(tool="node")
        if not run_files(filenames=filenames):
            sys.exit(1)
        return
    formatter = _require(tool="elm-format")
    for fixture in fixtures:
        with fixture.open(mode="rb") as source:
            _ = subprocess.run(
                args=[
                    _BOUNDED,
                    f"Elm formatting: {fixture}",
                    "--kill-after=5s",
                    "60s",
                    formatter,
                    "--stdin",
                ],
                stdin=source,
                stdout=subprocess.DEVNULL,
                check=True,
            )
    if not check_files(filenames=filenames):
        sys.exit(1)


if __name__ == "__main__":
    main()
