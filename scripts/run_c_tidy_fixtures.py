"""Run the native C lint pass over the complete fixture inventory."""

import concurrent.futures
import os
import shutil

import click

from scripts.bounded_command import run_bounded_command
from tests.integration.list_fixtures import fixture_paths


@click.command()
def main() -> None:
    """Run the C99 lint pass, including the public default module."""
    executable = shutil.which(cmd="clang-tidy")
    if executable is None:
        raise click.ClickException(
            message="The clang-tidy executable is required."
        )
    fixtures = fixture_paths(extension=".c", include_default_module_names=True)
    if len(fixtures) == 0:
        raise click.ClickException(message="No C fixtures.")
    with concurrent.futures.ThreadPoolExecutor(
        max_workers=os.cpu_count()
    ) as executor:
        checks = [
            executor.submit(
                run_bounded_command,
                args=[executable, fixture, "--", "-std=c99"],
                fixture=f"C lint: {fixture}",
                timeout_seconds=300.0,
                cwd=None,
            )
            for fixture in fixtures
        ]
        for check in checks:
            check.result()


if __name__ == "__main__":
    main()
