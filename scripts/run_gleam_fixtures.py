"""Select versioned fixtures for the existing warm Gleam helpers."""

import os
import subprocess
import sys
from pathlib import Path

import click

from scripts.bounded_command import bounded_command


@click.command()
@click.option("--version", type=str, default="v1", envvar="GLEAM_FIXTURE_TAG")
@click.option(
    "--check",
    "check_kind",
    type=click.Choice(choices=("all", "syntax", "execution")),
    default="all",
)
def main(*, version: str, check_kind: str) -> None:
    """Keep strict batched builds and the primed dependency project."""
    timeout = 600.0
    fixtures = sorted(
        path
        for path in Path("tests/integration/cases").rglob(pattern="*.gleam")
        if path.name.endswith(f"@{version}.gleam")
    )
    if len(fixtures) == 0:
        raise click.ClickException(message=f"No Gleam {version} fixtures.")
    primed = os.environ.get(key="LINT_GLEAM_PRIMED_DIR")
    if primed is None or not (Path(primed) / "gleam.toml").is_file():
        raise click.ClickException(
            message="LINT_GLEAM_PRIMED_DIR must name a prepared Gleam project."
        )
    payload = "".join(f"{path}\n" for path in fixtures)
    for phase, module in (
        ("syntax", "scripts.check_gleam_syntax"),
        ("execution", "scripts.run_gleam"),
    ):
        if check_kind not in ("all", phase):
            continue
        _ = subprocess.run(
            args=bounded_command(
                args=[sys.executable, "-m", module],
                fixture=f"Gleam {version} {phase}: {len(fixtures)} fixtures",
                timeout_seconds=timeout,
            ),
            input=payload,
            text=True,
            check=True,
        )


if __name__ == "__main__":
    main()
