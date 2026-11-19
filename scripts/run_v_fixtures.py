"""Validate the complete native V fixture population."""

import concurrent.futures
import os
import shutil
import sys
import tempfile
from pathlib import Path

import click

from scripts.bounded_command import run_bounded_command
from scripts.check_v_syntax import check_fixture
from tests.integration.list_fixtures import fixture_paths


@click.command()
def main() -> None:
    """Check formatting syntax, types and execution for every V
    fixture.
    """
    compiler = shutil.which(cmd="v")
    if compiler is None:
        raise click.ClickException(message="The v executable is required.")
    fixtures = fixture_paths(extension=".v")
    if len(fixtures) == 0:
        raise click.ClickException(message="No V fixtures.")
    # Initialize the compiler cache and lazily built formatter serially.
    with tempfile.TemporaryDirectory(suffix="-literalizer-v") as temporary:
        warmup = Path(temporary) / "warmup.v"
        _ = warmup.write_text(data="fn main() {}\n", encoding="utf-8")
        run_bounded_command(
            args=[compiler, "-cc", "gcc", "run", warmup],
            fixture="V compiler warmup",
            timeout_seconds=60.0,
            cwd=None,
        )
        run_bounded_command(
            args=[compiler, "fmt", warmup],
            fixture="V formatter warmup",
            timeout_seconds=60.0,
            cwd=None,
        )
    with concurrent.futures.ThreadPoolExecutor(
        max_workers=os.cpu_count()
    ) as executor:
        syntax = [
            executor.submit(check_fixture, fixture=fixture, v_path=compiler)
            for fixture in fixtures
        ]
        passed = [result.result() for result in syntax]
        if not all(passed):
            sys.exit(1)
        executions = [
            executor.submit(
                run_bounded_command,
                args=[compiler, "-W", "-cc", "gcc", "run", fixture],
                fixture=f"V execution: {fixture}",
                timeout_seconds=60.0,
                cwd=None,
            )
            for fixture in fixtures
        ]
        for execution in executions:
            execution.result()


if __name__ == "__main__":
    main()
