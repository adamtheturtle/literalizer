"""Check syntax of a TOML file using ``tomli``."""

import sys
from pathlib import Path

import tomli


def main() -> None:
    """Check syntax of the given TOML file."""
    filename = sys.argv[1]
    with Path(filename).open(mode="rb") as fp:
        try:
            tomli.load(__fp=fp)
        except tomli.TOMLDecodeError as e:
            sys.stderr.write(f"{filename}: {e}\n")
            sys.exit(1)


if __name__ == "__main__":
    main()
