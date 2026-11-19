"""Compile and execute every native Standard ML fixture with MLton."""

import concurrent.futures
import os
import shutil
import tempfile
from pathlib import Path

import click

from scripts.bounded_command import run_bounded_command
from tests.integration.list_fixtures import fixture_paths


def _check(*, fixture: Path, compiler: str) -> None:
    """Give each staged source and executable a private directory."""
    with tempfile.TemporaryDirectory(suffix="-literalizer-sml") as temporary:
        directory = Path(temporary)
        source = directory / "check.sml"
        binary = directory / "out"
        _ = shutil.copyfile(src=fixture, dst=source)
        run_bounded_command(
            args=[compiler, "-output", binary, source],
            fixture=f"SML '97 compilation: {fixture}",
            timeout_seconds=60.0,
            cwd=None,
        )
        run_bounded_command(
            args=[binary],
            fixture=f"SML '97 execution: {fixture}",
            timeout_seconds=60.0,
            cwd=None,
        )


@click.command()
def main() -> None:
    """Compile and execute all Standard ML '97 fixtures."""
    compiler = shutil.which(cmd="mlton")
    if compiler is None:
        raise click.ClickException(message="The mlton executable is required.")
    fixtures = fixture_paths(extension=".sml")
    if len(fixtures) == 0:
        raise click.ClickException(message="No Standard ML fixtures.")
    with concurrent.futures.ThreadPoolExecutor(
        max_workers=os.cpu_count()
    ) as executor:
        futures = [
            executor.submit(_check, fixture=fixture, compiler=compiler)
            for fixture in fixtures
        ]
        for future in futures:
            future.result()


if __name__ == "__main__":
    main()
