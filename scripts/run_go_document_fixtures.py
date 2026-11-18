"""Validate HCL and Jsonnet fixtures with their native command-line tools."""

import concurrent.futures
import os
import shutil
import subprocess
from pathlib import Path

import click

from scripts.bounded_command import bounded_command
from tests.integration.list_fixtures import fixture_paths

_TOOLS = {"hcl": "hcl2json", "jsonnet": "jsonnet"}


def _check(*, backend: str, executable: str, fixture: Path) -> None:
    """Discard parsed output while retaining tool diagnostics."""
    _ = subprocess.run(
        args=bounded_command(
            args=[executable, fixture],
            fixture=f"{backend} validation: {fixture}",
            timeout_seconds=60.0,
        ),
        stdout=subprocess.DEVNULL,
        check=True,
    )


@click.command()
@click.argument("backend", type=click.Choice(choices=tuple(_TOOLS)))
def main(backend: str) -> None:
    """Validate the selected BACKEND's entire native corpus."""
    tool = _TOOLS[backend]
    executable = shutil.which(cmd=tool)
    if executable is None:
        raise click.ClickException(
            message=f"The {tool} executable is required."
        )
    fixtures = fixture_paths(extension=f".{backend}")
    if len(fixtures) == 0:
        raise click.ClickException(message=f"No {backend} fixtures.")
    with concurrent.futures.ThreadPoolExecutor(
        max_workers=os.cpu_count()
    ) as executor:
        checks = [
            executor.submit(
                _check, backend=backend, executable=executable, fixture=fixture
            )
            for fixture in fixtures
        ]
        for check in checks:
            check.result()


if __name__ == "__main__":
    main()
