"""Lint the complete SystemVerilog fixture corpus using ``verilator``."""

import concurrent.futures
import os
import shutil

import click

from scripts.bounded_command import run_bounded_command
from tests.integration.list_fixtures import fixture_paths


@click.command()
def main() -> None:
    """Lint IEEE 1800-2017 fixtures, including the public default
    module.
    """
    compiler = shutil.which(cmd="verilator")
    if compiler is None:
        raise click.ClickException(
            message="The verilator executable is required."
        )
    fixtures = fixture_paths(
        extension=".sv", include_default_module_names=True
    )
    if len(fixtures) == 0:
        raise click.ClickException(message="No SystemVerilog fixtures.")
    # Keep warnings fatal except REALCVT, matching the native lint job.
    with concurrent.futures.ThreadPoolExecutor(
        max_workers=os.cpu_count()
    ) as executor:
        futures = [
            executor.submit(
                run_bounded_command,
                args=[
                    compiler,
                    "--lint-only",
                    "--language",
                    "1800-2017",
                    "-Wno-REALCVT",
                    fixture,
                ],
                fixture=f"SystemVerilog 1800-2017 lint: {fixture}",
                timeout_seconds=60.0,
                cwd=None,
            )
            for fixture in fixtures
        ]
        for future in futures:
            future.result()


if __name__ == "__main__":
    main()
