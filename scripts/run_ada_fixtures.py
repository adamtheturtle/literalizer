"""Check and execute the complete native Ada fixture population."""

import concurrent.futures
import os
import shutil
import sys

import click

from scripts import check_ada_syntax, run_ada
from tests.integration.list_fixtures import fixture_paths


@click.command()
def main() -> None:
    """Syntax-check and execute Ada 2022 fixtures, including the
    default.
    """
    compiler = shutil.which(cmd="gnatmake")
    if compiler is None:
        raise click.ClickException(
            message="The gnatmake executable is required."
        )
    fixtures = fixture_paths(
        extension=".adb", include_default_module_names=True
    )
    if len(fixtures) == 0:
        raise click.ClickException(message="No Ada fixtures.")
    with concurrent.futures.ThreadPoolExecutor(
        max_workers=os.cpu_count()
    ) as executor:
        for check in (check_ada_syntax.check_fixture, run_ada.check_fixture):
            results = [
                executor.submit(check, fixture=fixture, gnatmake_path=compiler)
                for fixture in fixtures
            ]
            passed = [result.result() for result in results]
            if not all(passed):
                sys.exit(1)


if __name__ == "__main__":
    main()
