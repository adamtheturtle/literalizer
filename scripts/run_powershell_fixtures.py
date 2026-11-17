"""Check fixture syntax and execution through the existing warm hosts."""

import os
import shutil
import subprocess
from pathlib import Path

import click

from scripts.bounded_command import bounded_command

_ROOT = Path(__file__).resolve().parents[1]


@click.command()
@click.option("--case", "case_name", type=str)
@click.option(
    "--check",
    "check_kind",
    type=click.Choice(choices=("all", "syntax", "execution")),
    default="all",
)
@click.option(
    "--timeout",
    type=click.FloatRange(min=0, min_open=True),
    default=600.0,
)
def main(*, case_name: str | None, check_kind: str, timeout: float) -> None:
    """Select a case or validate the complete native fixture corpus."""
    fixtures = sorted(
        fixture
        for fixture in Path("tests/integration/cases").rglob(pattern="*.ps1")
        if case_name is None or fixture.parent.name == case_name
    )
    if len(fixtures) == 0:
        raise click.ClickException(
            message=f"No PowerShell fixtures: {case_name!r}"
        )
    executable = shutil.which(cmd="pwsh")
    if executable is None:
        raise click.ClickException(message="The pwsh executable is required.")
    payload = b"".join(
        os.fsencode(filename=fixture) + b"\0" for fixture in fixtures
    )
    for phase, script in (
        ("syntax", "lint-powershell.ps1"),
        ("execution", "run-powershell.ps1"),
    ):
        if check_kind not in ("all", phase):
            continue
        _ = subprocess.run(
            args=bounded_command(
                args=[
                    executable,
                    "-NoProfile",
                    "-NonInteractive",
                    "-File",
                    _ROOT / "scripts" / script,
                ],
                fixture=f"PowerShell {phase}: {len(fixtures)} fixtures",
                timeout_seconds=timeout,
            ),
            input=payload,
            check=True,
        )


if __name__ == "__main__":
    main()
