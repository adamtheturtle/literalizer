"""Print null-byte-terminated fixture paths for a CI lint job.

Each per-language lint workflow shells out to this script instead of
``find``.  The script keeps only fixtures whose stem ends with
``@<version>`` so the lint job sees exactly the fixtures generated
under its compiler pin.

Invoked from CI as
``python -m tests.integration.list_fixtures <.ext> <version>``.
"""

import sys
from pathlib import Path

CASES_DIR = Path("tests/integration/cases")


def main(extension: str, version: str) -> int:
    """Emit fixture paths matching *extension* and *version*."""
    suffix = f"@{version}{extension}"
    paths = sorted(
        path
        for path in CASES_DIR.rglob(pattern=f"*{extension}")
        if path.name.endswith(suffix)
    )
    sys.stdout.buffer.write(b"".join(f"{p}".encode() + b"\0" for p in paths))
    return 0


if __name__ == "__main__":
    sys.exit(main(extension=sys.argv[1], version=sys.argv[2]))
