"""Compile and execute Nim fixtures with all pinned warnings fatal."""

import concurrent.futures
import os
import shutil
import tempfile
from pathlib import Path

import click

from scripts.bounded_command import run_bounded_command
from scripts.nim_warning_flags import NIM_WARNING_FLAGS
from tests.integration.list_fixtures import fixture_paths


def _check(*, fixture: Path, compiler: str) -> None:
    """Stage a valid module name and use a private compiler cache."""
    with tempfile.TemporaryDirectory(suffix="-literalizer-nim") as temporary:
        source = Path(temporary) / "check.nim"
        _ = shutil.copyfile(src=fixture, dst=source)
        run_bounded_command(
            args=[
                compiler,
                "c",
                "-r",
                "--hints:off",
                *NIM_WARNING_FLAGS,
                f"--nimcache:{temporary}",
                source,
            ],
            fixture=f"Nim V2 compile/execution: {fixture}",
            timeout_seconds=60.0,
            cwd=None,
        )


@click.command()
def main() -> None:
    """Compile and execute the full Nim V2 fixture population."""
    compiler = shutil.which(cmd="nim")
    if compiler is None:
        raise click.ClickException(message="The nim executable is required.")
    fixtures = fixture_paths(extension=".nim")
    if len(fixtures) == 0:
        raise click.ClickException(message="No Nim fixtures.")
    with concurrent.futures.ThreadPoolExecutor(
        max_workers=os.cpu_count()
    ) as executor:
        checks = [
            executor.submit(_check, fixture=fixture, compiler=compiler)
            for fixture in fixtures
        ]
        for check in checks:
            check.result()


if __name__ == "__main__":
    main()
