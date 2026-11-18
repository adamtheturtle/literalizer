"""Validate all Norg fixtures with a built native parser."""

import shutil
from pathlib import Path

import click

from scripts.bounded_command import run_bounded_command
from tests.integration.list_fixtures import fixture_paths


@click.command()
@click.option(
    "--parser",
    required=True,
    type=click.Path(exists=True, dir_okay=False, path_type=Path),
)
def main(*, parser: Path) -> None:
    """Parse the complete Norg corpus with the provided grammar library."""
    executable = shutil.which(cmd="tree-sitter")
    if executable is None:
        raise click.ClickException(
            message="The tree-sitter executable is required."
        )
    fixtures = fixture_paths(extension=".norg")
    if len(fixtures) == 0:
        raise click.ClickException(message="No Norg fixtures.")
    # Reuse the loaded grammar across fixtures and bound the command line.
    batch_size = 512
    for offset in range(0, len(fixtures), batch_size):
        batch = fixtures[offset : offset + batch_size]
        run_bounded_command(
            args=[
                executable,
                "parse",
                "--lib-path",
                parser.resolve(),
                "--lang-name",
                "norg",
                "--quiet",
                *batch,
            ],
            fixture=f"Norg parsing: {batch[0]} through {batch[-1]}",
            timeout_seconds=120.0,
            cwd=None,
        )


if __name__ == "__main__":
    main()
