"""Select versioned native fixtures for the existing warm compiler
host.
"""

import os
import shutil
import subprocess
from pathlib import Path

import click

from scripts.bounded_command import bounded_command
from tests.integration.list_fixtures import fixture_paths

_HOST = Path(__file__).resolve().with_name(name="lint-elixir.exs")


@click.command()
@click.option(
    "--version", type=str, default="v1_14", envvar="ELIXIR_FIXTURE_TAG"
)
def main(*, version: str) -> None:
    """Compile and execute the complete selected version."""
    timeout = 600.0
    fixtures = fixture_paths(extension=".ex", version=version)
    if len(fixtures) == 0:
        raise click.ClickException(message=f"No Elixir {version} fixtures.")
    executable = shutil.which(cmd="elixir")
    if executable is None:
        raise click.ClickException(
            message="The elixir executable is required."
        )
    payload = b"".join(os.fsencode(filename=path) + b"\0" for path in fixtures)
    _ = subprocess.run(
        args=bounded_command(
            args=[executable, _HOST],
            fixture=f"Elixir {version}: {len(fixtures)} fixtures",
            timeout_seconds=timeout,
        ),
        input=payload,
        check=True,
    )


if __name__ == "__main__":
    main()
