"""Check syntax of TOML files using ``tomli``."""

import sys
from pathlib import Path

import tomli


def main() -> None:
    """Check syntax of each given TOML file."""
    for filename in sys.argv[1:]:
        with Path(filename).open(mode="rb") as fp:
            try:
                tomli.load(fp)
            except tomli.TOMLDecodeError as e:
                sys.stderr.write(f"{filename}: {e}\n")
                sys.exit(1)


if __name__ == "__main__":
    main()
