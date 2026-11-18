"""Validate versioned native modules through the existing in-memory
host.
"""

import os
import shutil
import subprocess
import tempfile
from pathlib import Path

import click

from scripts.bounded_command import bounded_command
from tests.integration.list_fixtures import fixture_paths

_HOST = Path(__file__).resolve().with_name(name="run_erlang.escript")


@click.command()
@click.option(
    "--version", type=str, default="otp_25", envvar="ERLANG_FIXTURE_TAG"
)
def main(*, version: str) -> None:
    """Keep warnings fatal and invoke every compiled module's entry
    point.
    """
    timeout = 600.0
    fixtures = fixture_paths(
        extension=".erl", version=version, include_default_module_names=True
    )
    if len(fixtures) == 0:
        raise click.ClickException(message=f"No Erlang {version} fixtures.")
    executable = shutil.which(cmd="escript")
    if executable is None:
        raise click.ClickException(
            message="The escript executable is required."
        )
    with tempfile.TemporaryDirectory(
        suffix="-literalizer-erlang"
    ) as temporary:
        listing = Path(temporary) / "fixtures.list"
        _ = listing.write_bytes(
            data=b"".join(
                os.fsencode(filename=path) + b"\0" for path in fixtures
            )
        )
        _ = subprocess.run(
            args=bounded_command(
                args=[executable, _HOST, listing],
                fixture=f"Erlang {version}: {len(fixtures)} fixtures",
                timeout_seconds=timeout,
            ),
            check=True,
        )


if __name__ == "__main__":
    main()
