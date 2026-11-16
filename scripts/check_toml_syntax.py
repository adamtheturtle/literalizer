"""Check syntax of a TOML file using ``tomli``."""

import sys
from pathlib import Path

import click
import tomli


@click.command()
@click.argument("filename")
def main(filename: str) -> None:
    """Check syntax of the given TOML file."""
    with Path(filename).open(mode="rb") as fp:
        try:
            _ = tomli.load(fp)
        except tomli.TOMLDecodeError as e:
            _ = sys.stderr.write(f"{filename}: {e}\n")
            sys.exit(1)


if __name__ == "__main__":
    main()
