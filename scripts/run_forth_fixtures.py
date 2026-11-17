"""Execute native visitor streams with their existing support
definitions.
"""

import concurrent.futures
import os
import shutil
import subprocess
from pathlib import Path

import click

from scripts.bounded_command import bounded_command

_PRELUDE = Path(__file__).resolve().with_name(name="forth_visitor_lint.fs")


def _check(*, fixture: Path, executable: str, timeout: float) -> None:
    """Load the same visitor support and source that native CI
    validates.
    """
    _ = subprocess.run(
        args=bounded_command(
            args=[executable, _PRELUDE, fixture, "-e", "bye"],
            fixture=str(object=fixture),
            timeout_seconds=timeout,
        ),
        check=True,
    )


@click.command()
def main() -> None:
    """Validate every generated visitor stream."""
    jobs = os.cpu_count()
    timeout = 60.0
    fixtures = sorted(
        fixture
        for fixture in Path("tests/integration/cases").rglob(pattern="*.fth")
    )
    if len(fixtures) == 0:
        raise click.ClickException(message="No Forth fixtures.")
    executable = shutil.which(cmd="gforth")
    if executable is None:
        raise click.ClickException(
            message="The gforth executable is required."
        )
    with concurrent.futures.ThreadPoolExecutor(max_workers=jobs) as executor:
        for future in [
            executor.submit(
                _check, fixture=fixture, executable=executable, timeout=timeout
            )
            for fixture in fixtures
        ]:
            future.result()


if __name__ == "__main__":
    main()
