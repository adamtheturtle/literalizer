"""Check the complete Roc fixture inventory with the native compiler."""

import concurrent.futures
import os
import shutil

import click

from scripts.bounded_command import run_bounded_command
from tests.integration.list_fixtures import fixture_paths


@click.command()
def main() -> None:
    """Run the native Roc checker on the full V1 fixture population."""
    compiler = shutil.which(cmd="roc")
    if compiler is None:
        raise click.ClickException(message="The roc executable is required.")
    fixtures = fixture_paths(extension=".roc")
    if len(fixtures) == 0:
        raise click.ClickException(message="No Roc fixtures.")
    with concurrent.futures.ThreadPoolExecutor(
        max_workers=os.cpu_count()
    ) as executor:
        checks = [
            executor.submit(
                run_bounded_command,
                args=[compiler, "check", fixture],
                fixture=f"Roc V1 check: {fixture}",
                timeout_seconds=60.0,
                cwd=None,
            )
            for fixture in fixtures
        ]
        for check in checks:
            check.result()


if __name__ == "__main__":
    main()
