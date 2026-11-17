"""Compile and execute Rust fixtures against prepared dependency artifacts."""

import shutil
import subprocess
import tempfile
from pathlib import Path

import click

from scripts.bounded_command import bounded_command


def _run(*, arguments: list[str | Path], label: str, timeout: float) -> None:
    """Bound each native phase and retain its original fixture label."""
    _ = subprocess.run(
        args=bounded_command(
            args=arguments, fixture=label, timeout_seconds=timeout
        ),
        check=True,
    )


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
    fixtures = sorted(
        path for path in Path("tests/integration/cases").rglob(pattern="*.rs")
    )
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
            _run(
                arguments=[
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
                label=f"Rust compile: {fixture}",
                timeout=timeout,
            )
            _run(
                arguments=[binary],
                label=f"Rust execution: {fixture}",
                timeout=timeout,
            )


if __name__ == "__main__":
    main()
