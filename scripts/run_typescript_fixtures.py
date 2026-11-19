"""Validate TypeScript fixtures with the native compiler and runtime."""

import concurrent.futures
import os
import shutil
import sys

import click

from scripts.bounded_command import run_bounded_command
from scripts.check_typescript_consumers import check_files
from tests.integration.list_fixtures import fixture_paths


@click.command()
@click.argument("stage", type=click.Choice(choices=("typecheck", "run")))
def main(stage: str) -> None:
    """Type-check consumer probes or execute all TypeScript V5
    fixtures.
    """
    tool = "tsc" if stage == "typecheck" else "tsx"
    executable = shutil.which(cmd=tool)
    if executable is None:
        raise click.ClickException(
            message=f"The {tool} executable is required."
        )
    fixtures = fixture_paths(extension=".ts")
    if len(fixtures) == 0:
        raise click.ClickException(message="No TypeScript fixtures.")
    if stage == "typecheck":
        # Bound the command line while retaining batched compiler invocations.
        batch_size = 1024
        for offset in range(0, len(fixtures), batch_size):
            batch = fixtures[offset : offset + batch_size]
            if not check_files(
                filenames=tuple(str(object=fixture) for fixture in batch)
            ):
                sys.exit(1)
        return
    with concurrent.futures.ThreadPoolExecutor(
        max_workers=os.cpu_count()
    ) as executor:
        runs = [
            executor.submit(
                run_bounded_command,
                args=[executable, fixture],
                fixture=f"TypeScript V5 execution: {fixture}",
                timeout_seconds=60.0,
                cwd=None,
            )
            for fixture in fixtures
        ]
        for run in runs:
            run.result()


if __name__ == "__main__":
    main()
