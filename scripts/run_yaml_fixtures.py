"""Check YAML 1.2 fixtures with the same linter rules as the workflow."""

import shutil

import click

from scripts.bounded_command import run_bounded_command
from tests.integration.list_fixtures import fixture_paths

_RULES = (
    "{extends: default, rules: {document-start: disable, "
    "line-length: disable}}"
)


@click.command()
def main() -> None:
    """Run strict linting on the complete YAML 1.2 fixture population."""
    executable = shutil.which(cmd="yamllint")
    if executable is None:
        raise click.ClickException(
            message="The yamllint executable is required."
        )
    fixtures = fixture_paths(extension=".yaml", version="v1_2")
    if len(fixtures) == 0:
        raise click.ClickException(message="No YAML 1.2 fixtures.")
    batch_size = 512
    for offset in range(0, len(fixtures), batch_size):
        batch = fixtures[offset : offset + batch_size]
        run_bounded_command(
            args=[executable, "--strict", "-d", _RULES, "--", *batch],
            fixture=f"YAML 1.2 lint: {batch[0]} through {batch[-1]}",
            timeout_seconds=120.0,
            cwd=None,
        )


if __name__ == "__main__":
    main()
