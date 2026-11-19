"""Syntax-check, compile and execute the COBOL fixtures with GnuCOBOL."""

import concurrent.futures
import os
import shutil
import tempfile
from pathlib import Path

import click

from scripts.bounded_command import run_bounded_command
from tests.integration.list_fixtures import fixture_paths


def _check(*, fixture: Path, compiler: str, execute: bool) -> None:
    """Stage a short filename within the compiler's name length limit."""
    with tempfile.TemporaryDirectory(suffix="-literalizer-cobol") as temporary:
        directory = Path(temporary)
        source = directory / "check.cob"
        _ = shutil.copyfile(src=fixture, dst=source)
        if not execute:
            run_bounded_command(
                args=[compiler, "-Werror", "-free", "-fsyntax-only", source],
                fixture=f"COBOL 2002 syntax: {fixture}",
                timeout_seconds=60.0,
                cwd=None,
            )
            return
        binary = directory / "run"
        # All fixtures can link cJSON, including those using COBOL records.
        run_bounded_command(
            args=[
                compiler,
                "-Werror",
                "-x",
                "-free",
                source,
                "-o",
                binary,
                "-lcjson",
            ],
            fixture=f"COBOL 2002 compilation: {fixture}",
            timeout_seconds=60.0,
            cwd=None,
        )
        run_bounded_command(
            args=[binary],
            fixture=f"COBOL 2002 execution: {fixture}",
            timeout_seconds=60.0,
            cwd=None,
        )


@click.command()
def main() -> None:
    """Validate all fixtures with fatal compiler warnings."""
    compiler = shutil.which(cmd="cobc")
    if compiler is None:
        raise click.ClickException(message="The cobc executable is required.")
    fixtures = fixture_paths(extension=".cob")
    if len(fixtures) == 0:
        raise click.ClickException(message="No COBOL fixtures.")
    with concurrent.futures.ThreadPoolExecutor(
        max_workers=os.cpu_count()
    ) as executor:
        for execute in (False, True):
            checks = [
                executor.submit(
                    _check, fixture=fixture, compiler=compiler, execute=execute
                )
                for fixture in fixtures
            ]
            for check in checks:
                check.result()


if __name__ == "__main__":
    main()
