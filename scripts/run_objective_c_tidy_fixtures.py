"""Run the native Objective-C lint pass over the complete fixture
inventory.
"""

import concurrent.futures
import os
import shutil

import click

from scripts.bounded_command import run_bounded_command
from tests.integration.list_fixtures import fixture_paths


@click.command()
def main() -> None:
    """Lint Objective-C 2.0 fixtures, including the public default
    module.
    """
    executable = shutil.which(cmd="clang-tidy")
    if executable is None:
        raise click.ClickException(
            message="The clang-tidy executable is required."
        )
    fixtures = fixture_paths(
        extension=".m",
        language="ObjectiveC",
        include_default_module_names=True,
    )
    if len(fixtures) == 0:
        raise click.ClickException(message="No Objective-C fixtures.")
    with concurrent.futures.ThreadPoolExecutor(
        max_workers=os.cpu_count()
    ) as executor:
        checks = [
            executor.submit(
                run_bounded_command,
                args=[executable, "--extra-arg=-fobjc-arc", fixture],
                fixture=f"Objective-C lint: {fixture}",
                timeout_seconds=60.0,
                cwd=None,
            )
            for fixture in fixtures
        ]
        for check in checks:
            check.result()


if __name__ == "__main__":
    main()
