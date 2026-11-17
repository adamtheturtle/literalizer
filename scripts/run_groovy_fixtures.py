"""Select native sources for the existing isolated warm compiler host."""

import os
import shutil
import subprocess
from pathlib import Path

import click

from scripts.bounded_command import bounded_command

_HOST = Path(__file__).resolve().with_name(name="lint-groovy.groovy")


@click.command()
@click.option(
    "--timeout", type=click.FloatRange(min=0, min_open=True), default=600.0
)
def main(*, timeout: float) -> None:
    """Compile and run selected fixtures in one host with private
    shells.
    """
    fixtures = sorted(
        path
        for path in Path("tests/integration/cases").rglob(pattern="*.groovy")
    )
    if len(fixtures) == 0:
        raise click.ClickException(message="No Groovy fixtures.")
    executable = shutil.which(cmd="groovy")
    if executable is None:
        raise click.ClickException(
            message="The groovy executable is required."
        )
    _ = subprocess.run(
        args=bounded_command(
            args=[executable, _HOST],
            fixture=f"Groovy: {len(fixtures)} fixtures",
            timeout_seconds=timeout,
        ),
        input=b"".join(
            os.fsencode(filename=path) + b"\0" for path in fixtures
        ),
        check=True,
    )


if __name__ == "__main__":
    main()
