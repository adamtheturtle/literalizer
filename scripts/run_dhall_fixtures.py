"""Validate native documents through the existing standard-input
command.
"""

import concurrent.futures
import os
import shutil
import subprocess
from pathlib import Path

import click

from scripts.bounded_command import bounded_command
from tests.integration.list_fixtures import fixture_paths


def _check(*, fixture: Path, executable: str, timeout: float) -> None:
    """Keep document input, diagnostics and discarded output unchanged."""
    with fixture.open(mode="rb") as source:
        _ = subprocess.run(
            args=bounded_command(
                args=[executable],
                fixture=str(object=fixture),
                timeout_seconds=timeout,
            ),
            stdin=source,
            stdout=subprocess.DEVNULL,
            check=True,
        )


@click.command()
def main() -> None:
    """Validate every generated native document."""
    jobs = os.cpu_count()
    timeout = 60.0
    fixtures = fixture_paths(extension=".dhall")
    if len(fixtures) == 0:
        raise click.ClickException(message="No Dhall fixtures.")
    executable = shutil.which(cmd="dhall")
    if executable is None:
        raise click.ClickException(message="The dhall executable is required.")
    with concurrent.futures.ThreadPoolExecutor(max_workers=jobs) as executor:
        for future in [
            executor.submit(
                _check, fixture=fixture, executable=executable, timeout=timeout
            )
            for fixture in fixtures
        ]:
            future.result()


if __name__ == "__main__":
    main()
