"""Validate authored and generated JSON5 and JSONC documents."""

import concurrent.futures
import os
import shutil
import subprocess
import sys
from pathlib import Path

import click

from scripts.bounded_command import bounded_command
from scripts.check_jsonc_syntax import check_files
from tests.integration.list_fixtures import fixture_paths


def _check_json5(*, executable: str, fixture: Path) -> None:
    """Run the native parser and discard its converted document."""
    _ = subprocess.run(
        args=bounded_command(
            args=[executable, fixture],
            fixture=f"JSON5 parsing: {fixture}",
            timeout_seconds=60.0,
        ),
        stdout=subprocess.DEVNULL,
        check=True,
    )


@click.command()
@click.argument("format_name", type=click.Choice(choices=("json5", "jsonc")))
def main(format_name: str) -> None:
    """Parse fixtures and authored inputs in the given format."""
    fixtures = fixture_paths(
        extension=f".{format_name}", include_authored=True
    )
    if len(fixtures) == 0:
        raise click.ClickException(
            message=f"No {format_name} fixtures or inputs."
        )
    if format_name == "jsonc":
        if not check_files(
            filenames=tuple(str(object=fixture) for fixture in fixtures)
        ):
            sys.exit(1)
        return
    executable = shutil.which(cmd="json5")
    if executable is None:
        raise click.ClickException(message="The json5 executable is required.")
    with concurrent.futures.ThreadPoolExecutor(
        max_workers=os.cpu_count()
    ) as executor:
        checks = [
            executor.submit(
                _check_json5, executable=executable, fixture=fixture
            )
            for fixture in fixtures
        ]
        for check in checks:
            check.result()


if __name__ == "__main__":
    main()
