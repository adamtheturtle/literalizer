"""Check syntax of a TOML file using ``tomli``."""

import sys
from pathlib import Path

import click
import tomli


def check_file(*, path: Path) -> bool:
    """Report any syntax error and return whether parsing succeeded."""
    with path.open(mode="rb") as fp:
        try:
            _ = tomli.load(fp)
        except tomli.TOMLDecodeError as e:
            _ = sys.stderr.write(f"{path}: {e}\n")
            return False
    return True


@click.command()
@click.argument("filename")
def main(filename: str) -> None:
    """Check syntax of the given TOML file."""
    if not check_file(path=Path(filename)):
        sys.exit(1)


if __name__ == "__main__":
    main()
