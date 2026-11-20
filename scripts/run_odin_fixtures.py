"""Run the selected Odin fixtures serially with the native helper."""

import shutil
import subprocess
from pathlib import Path

import click

from tests.integration.list_fixtures import fixture_paths

_RUNNER = Path(__file__).resolve().with_name(name="lint-odin-fixture.sh")


@click.command()
@click.argument("version", type=click.Choice(choices=("dev_2024",)))
@click.option(
    "--shard", type=click.IntRange(min=0), default=0, show_default=True
)
@click.option(
    "--shards", type=click.IntRange(min=1), default=1, show_default=True
)
def main(version: str, *, shard: int, shards: int) -> None:
    """Compile and run Odin fixtures for VERSION and the selected
    shard.
    """
    if shard >= shards:
        raise click.UsageError(
            message="The shard index must be below --shards."
        )
    if shutil.which(cmd="odin") is None:
        raise click.ClickException(message="The odin executable is required.")
    fixtures = fixture_paths(extension=".odin", version=version)
    selected = fixtures[shard::shards]
    if len(selected) == 0:
        raise click.ClickException(
            message=f"No Odin {version} fixtures for this shard."
        )
    for fixture in selected:
        source = fixture.resolve()
        click.echo(message=f"Running {source}")
        _ = subprocess.run(args=[_RUNNER, source], check=True)


if __name__ == "__main__":
    main()
