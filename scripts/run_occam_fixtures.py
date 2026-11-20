"""Apply the structural checker to every Occam fixture."""

import sys

import click

from scripts.check_occam_syntax import check_file
from tests.integration.list_fixtures import fixture_paths


@click.command()
def main() -> None:
    """Check Occam-pi structure, including the public default fixture."""
    fixtures = fixture_paths(
        extension=".occ", include_default_module_names=True
    )
    if len(fixtures) == 0:
        raise click.ClickException(message="No Occam fixtures.")
    results = [check_file(path=fixture) for fixture in fixtures]
    if not all(results):
        sys.exit(1)


if __name__ == "__main__":
    main()
