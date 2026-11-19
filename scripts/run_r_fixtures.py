"""Parse and execute the R fixture corpus with ``Rscript``."""

import concurrent.futures
import os
import shutil

import click

from scripts.bounded_command import run_bounded_command
from tests.integration.list_fixtures import fixture_paths

_PARSE = "for (f in commandArgs(trailingOnly=TRUE)) parse(file=f)"


@click.command()
def main() -> None:
    """Parse the R 4 fixtures in batches, then execute each file."""
    interpreter = shutil.which(cmd="Rscript")
    if interpreter is None:
        raise click.ClickException(
            message="The Rscript executable is required."
        )
    fixtures = fixture_paths(extension=".R")
    if len(fixtures) == 0:
        raise click.ClickException(message="No R fixtures.")

    # Batch parsing to amortize startup and bound argument length.
    batch_size = 128
    for offset in range(0, len(fixtures), batch_size):
        batch = fixtures[offset : offset + batch_size]
        run_bounded_command(
            args=[interpreter, "-e", _PARSE, *batch],
            fixture=f"R V4 parsing: {batch[0]} through {batch[-1]}",
            timeout_seconds=60.0,
            cwd=None,
        )

    with concurrent.futures.ThreadPoolExecutor(
        max_workers=os.cpu_count()
    ) as executor:
        futures = [
            executor.submit(
                run_bounded_command,
                args=[interpreter, fixture],
                fixture=f"R V4 execution: {fixture}",
                timeout_seconds=60.0,
                cwd=None,
            )
            for fixture in fixtures
        ]
        for future in futures:
            future.result()


if __name__ == "__main__":
    main()
