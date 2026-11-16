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
@click.option("--case", "case_name", type=str)
@click.option("--jobs", type=click.IntRange(min=1), default=os.cpu_count)
@click.option(
    "--timeout", type=click.FloatRange(min=0, min_open=True), default=60.0
)
def main(*, case_name: str | None, jobs: int, timeout: float) -> None:
    """Validate a named case or every generated native document."""
    fixtures = sorted(
        fixture
        for fixture in Path("tests/integration/cases").rglob(pattern="*.dhall")
        if case_name is None or fixture.parent.name == case_name
    )
    if len(fixtures) == 0:
        raise click.ClickException(message=f"No Dhall fixtures: {case_name!r}")
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
