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

_HOST = Path(__file__).resolve().with_name(name="run_erlang.escript")


@click.command()
@click.option("--case", "case_name", type=str)
@click.option(
    "--version", type=str, default="otp_25", envvar="ERLANG_FIXTURE_TAG"
)
@click.option(
    "--timeout", type=click.FloatRange(min=0, min_open=True), default=600.0
)
def main(*, case_name: str | None, version: str, timeout: float) -> None:
    """Keep warnings fatal and invoke every compiled module's entry
    point.
    """
    roots = (
        Path("tests/integration/cases"),
        Path("tests/integration/default_module_names"),
    )
    fixtures = sorted(
        path
        for root in roots
        for path in root.rglob(pattern="*.erl")
        if path.name.endswith(f"@{version}.erl")
        if case_name is None or path.parent.name == case_name
    )
    if len(fixtures) == 0:
        raise click.ClickException(
            message=f"No Erlang {version} fixtures: {case_name!r}"
        )
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
