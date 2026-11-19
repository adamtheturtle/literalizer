"""Run the native Nix lint pass over the complete fixture inventory."""

import concurrent.futures
import os
import shutil
import subprocess
from pathlib import Path

import click

from scripts.bounded_command import bounded_command
from tests.integration.list_fixtures import fixture_paths


def _parse(*, executable: str, fixture: Path) -> None:
    """Discard the printed syntax tree and keep native diagnostics."""
    _ = subprocess.run(
        args=bounded_command(
            args=[executable, "--parse", fixture],
            fixture=f"Nix V2 parse: {fixture}",
            timeout_seconds=60.0,
        ),
        stdout=subprocess.DEVNULL,
        check=True,
    )


@click.command()
def main() -> None:
    """Parse every generated Nix expression."""
    executable = shutil.which(cmd="nix-instantiate")
    if executable is None:
        raise click.ClickException(
            message="The nix-instantiate executable is required."
        )
    fixtures = fixture_paths(extension=".nix")
    if len(fixtures) == 0:
        raise click.ClickException(message="No Nix fixtures.")
    with concurrent.futures.ThreadPoolExecutor(
        max_workers=os.cpu_count()
    ) as executor:
        checks = [
            executor.submit(_parse, executable=executable, fixture=fixture)
            for fixture in fixtures
        ]
        for check in checks:
            check.result()


if __name__ == "__main__":
    main()
