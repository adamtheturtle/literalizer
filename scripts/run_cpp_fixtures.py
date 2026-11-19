"""Select and validate C++ fixtures through the existing native
adapter.
"""

import concurrent.futures
import os
import shutil
import subprocess
from pathlib import Path

import click

from tests.integration.list_fixtures import fixture_paths

_ADAPTER = Path(__file__).resolve().with_name(name="lint-cpp-fixture.sh")


def _check(*, stage: str, fixture: Path) -> None:
    """Let the native adapter select the standard and enforce
    deadlines.
    """
    _ = subprocess.run(args=[_ADAPTER, stage, fixture.resolve()], check=True)


@click.command()
@click.argument("stage", type=click.Choice(choices=("tidy", "run")))
@click.option(
    "--shard", type=click.IntRange(min=0), default=0, show_default=True
)
@click.option(
    "--shards", type=click.IntRange(min=1), default=1, show_default=True
)
def main(stage: str, *, shard: int, shards: int) -> None:
    """Run one C++ validation STAGE over all fixtures or one shard."""
    if shard >= shards:
        raise click.UsageError(
            message="The shard index must be below --shards."
        )
    tool = "clang-tidy" if stage == "tidy" else "clang++"
    if shutil.which(cmd=tool) is None:
        raise click.ClickException(
            message=f"The {tool} executable is required."
        )
    fixtures = fixture_paths(
        extension=".cpp", include_default_module_names=True
    )
    selected = fixtures[shard::shards]
    if len(selected) == 0:
        raise click.ClickException(message="No C++ fixtures for this shard.")
    with concurrent.futures.ThreadPoolExecutor(
        max_workers=os.cpu_count()
    ) as executor:
        checks = [
            executor.submit(_check, stage=stage, fixture=fixture)
            for fixture in selected
        ]
        for check in checks:
            check.result()


if __name__ == "__main__":
    main()
