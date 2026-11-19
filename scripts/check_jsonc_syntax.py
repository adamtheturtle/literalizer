"""Check JSONC golden files using ``jsonc-document``."""

import sys
from pathlib import Path

import click
import jsonc_document


def check_files(*, filenames: tuple[str, ...]) -> bool:
    """Report syntax errors in the given JSONC files and return
    success.
    """
    failed = False
    for filename in filenames:
        source = Path(filename).read_text(encoding="utf-8")
        try:
            _ = jsonc_document.loads(source=source)
        except jsonc_document.JSONCDecodeError as exc:
            _ = sys.stderr.write(
                f"{filename}:{exc.lineno}:{exc.colno}: {exc.msg}\n"
            )
            failed = True
    return not failed


@click.command()
@click.argument("filenames", nargs=-1)
def main(filenames: tuple[str, ...]) -> None:
    """Report syntax errors in the given JSONC files."""
    if not check_files(filenames=filenames):
        sys.exit(1)


if __name__ == "__main__":
    main()
