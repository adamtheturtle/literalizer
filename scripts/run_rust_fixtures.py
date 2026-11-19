"""Compile and execute Rust fixtures against prepared dependency artifacts."""

import shutil
import tempfile
from pathlib import Path

import click

from scripts.bounded_command import run_bounded_command
from scripts.reference_observations import run_reference_fixture
from tests.integration.list_fixtures import fixture_paths


@click.command()
@click.option(
    "--deps",
    type=click.Path(path_type=Path, exists=True, file_okay=False),
    envvar="RUST_DEPS",
    required=True,
)
@click.option(
    "--chrono",
    type=click.Path(path_type=Path, exists=True, dir_okay=False),
    envvar="RUST_CHRONO_RLIB",
    required=True,
)
@click.option(
    "--serde-json",
    type=click.Path(path_type=Path, exists=True, dir_okay=False),
    envvar="RUST_SERDE_JSON_RLIB",
    required=True,
)
def main(*, deps: Path, chrono: Path, serde_json: Path) -> None:
    """Preserve the 2021 edition, fatal warnings and serial compiler
    use.
    """
    timeout = 60.0
    fixtures = fixture_paths(extension=".rs")
    if len(fixtures) == 0:
        raise click.ClickException(message="No Rust fixtures.")
    executable = shutil.which(cmd="rustc")
    if executable is None:
        raise click.ClickException(message="The rustc executable is required.")
    for fixture in fixtures:
        with tempfile.TemporaryDirectory(
            suffix="-literalizer-rust"
        ) as directory:
            binary = Path(directory) / "run"
            crate = fixture.stem.replace("@", "_")
            run_bounded_command(
                args=[
                    executable,
                    "--edition",
                    "2021",
                    "-D",
                    "warnings",
                    "--crate-name",
                    crate,
                    "-L",
                    f"dependency={deps}",
                    "--extern",
                    f"chrono={chrono}",
                    "--extern",
                    f"serde_json={serde_json}",
                    fixture,
                    "-o",
                    binary,
                ],
                fixture=f"Rust compile: {fixture}",
                timeout_seconds=timeout,
                cwd=None,
            )
            run_reference_fixture(
                fixture=fixture, executable=binary, timeout_seconds=timeout
            )


if __name__ == "__main__":
    main()
