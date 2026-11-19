"""Load every Common Lisp fixture through the configured Roswell
runtime.
"""

import concurrent.futures
import os
import shutil

import click

from scripts.bounded_command import run_bounded_command
from tests.integration.list_fixtures import fixture_paths


@click.command()
def main() -> None:
    """Load the ANSI Common Lisp fixtures with the SBCL debugger
    disabled.
    """
    roswell = shutil.which(cmd="ros")
    if roswell is None:
        raise click.ClickException(message="The ros executable is required.")
    fixtures = fixture_paths(extension=".lisp")
    if len(fixtures) == 0:
        raise click.ClickException(message="No Common Lisp fixtures.")
    with concurrent.futures.ThreadPoolExecutor(
        max_workers=os.cpu_count()
    ) as executor:
        futures = [
            executor.submit(
                run_bounded_command,
                args=[
                    roswell,
                    "run",
                    "--eval",
                    "(sb-ext:disable-debugger)",
                    "--load",
                    fixture,
                    "--quit",
                ],
                fixture=f"ANSI Common Lisp load: {fixture}",
                timeout_seconds=60.0,
                cwd=None,
            )
            for fixture in fixtures
        ]
        for future in futures:
            future.result()


if __name__ == "__main__":
    main()
