"""Compile and execute the complete PureScript fixture corpus."""

import concurrent.futures
import functools
import os
import shutil
import sys

import click

from scripts.check_purescript_syntax import check_fixture
from scripts.run_purescript import run_fixtures
from tests.integration.list_fixtures import fixture_paths


@click.command()
def main() -> None:
    """Compile the fixtures in parallel, then run them in a warm workspace."""
    purs = shutil.which(cmd="purs")
    if purs is None:
        raise click.ClickException(message="The purs executable is required.")
    node = shutil.which(cmd="node")
    if node is None:
        raise click.ClickException(message="The node executable is required.")
    fixtures = fixture_paths(extension=".purs")
    if len(fixtures) == 0:
        raise click.ClickException(message="No PureScript fixtures.")
    filenames = tuple(str(object=fixture) for fixture in fixtures)
    check = functools.partial(check_fixture, purs_path=purs)
    with concurrent.futures.ThreadPoolExecutor(
        max_workers=os.cpu_count()
    ) as executor:
        results = list(executor.map(check, filenames))
    if not all(results) or not run_fixtures(
        filenames=filenames, purs_path=purs, node_path=node
    ):
        sys.exit(1)


if __name__ == "__main__":
    main()
