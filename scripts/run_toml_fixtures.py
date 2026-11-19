"""Parse generated TOML fixtures and authored TOML documents."""

import sys

import click

from scripts.check_toml_syntax import check_file
from tests.integration.list_fixtures import fixture_paths


@click.command()
def main() -> None:
    """Check the complete TOML corpus, including authored inputs."""
    fixtures = fixture_paths(extension=".toml", include_authored=True)
    if len(fixtures) == 0:
        raise click.ClickException(message="No TOML fixtures or inputs.")
    results = [check_file(path=fixture) for fixture in fixtures]
    if not all(results):
        sys.exit(1)


if __name__ == "__main__":
    main()
