"""Select a Mojo fixture shard and run the existing bounded compiler
pool.
"""

import os
import shutil
import subprocess
import tempfile
from pathlib import Path

import click

from tests.integration.list_fixtures import fixture_paths

_RUNNER = Path(__file__).resolve().with_name(name="lint-mojo.sh")


@click.command()
@click.option(
    "--shard", type=click.IntRange(min=0), default=0, show_default=True
)
@click.option(
    "--shards", type=click.IntRange(min=1), default=1, show_default=True
)
def main(*, shard: int, shards: int) -> None:
    """Compile the complete Mojo corpus or one shard on Linux using
    ``systemd``.
    """
    if shard >= shards:
        raise click.UsageError(
            message="The shard index must be below --shards."
        )
    for executable in ("mojo", "free", "df", "systemd-run"):
        if shutil.which(cmd=executable) is None:
            raise click.ClickException(
                message=f"The {executable} executable is required."
            )
    fixtures = fixture_paths(extension=".mojo")
    selected = fixtures[shard::shards]
    if len(selected) == 0:
        raise click.ClickException(message="No Mojo fixtures for this shard.")
    click.echo(
        message=(
            f"Mojo shard {shard + 1}/{shards}: "
            f"{len(selected)} of {len(fixtures)} fixtures"
        )
    )
    click.echo(
        message=(
            "Mojo compiler workers: 4; compiler threads per worker: 1; "
            "pool ceiling: 4 GiB; hard fixture deadline: 60s"
        )
    )
    _ = subprocess.run(args=["free", "-m"], check=True)  # noqa: S607
    _ = subprocess.run(args=["df", "-h", tempfile.gettempdir()], check=True)  # noqa: S607
    inputs = b"".join(
        os.fsencode(filename=fixture) + b"\0" for fixture in selected
    )
    _ = subprocess.run(args=[_RUNNER], input=inputs, check=True)


if __name__ == "__main__":
    main()
