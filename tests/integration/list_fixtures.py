"""Print null-byte-terminated fixture paths for a language.

Each CI lint job that compiles per-language fixtures shells out to
this script instead of ``find``.  When the language is registered in
:data:`LANGUAGE_VERSIONS` the script keeps only fixtures whose stem
ends with ``@{pinned-version}`` so the lint job sees exactly the
fixtures generated against its compiler pin; unregistered languages
get every fixture with the requested extension.

Lives next to ``language_versions.py`` for natural relative import;
invoked from CI as
``python -m tests.integration.list_fixtures <Language> <.ext>``.
"""

import sys
from pathlib import Path

from .language_versions import LANGUAGE_VERSIONS

CASES_DIR = Path("tests/integration/cases")


def main(language: str, extension: str) -> int:
    """Emit fixture paths for *language* with *extension*.

    Paths are reported relative to the repository root, matching what
    ``find tests/integration/cases ...`` produced before this script
    existed.  The script must be invoked from the repository root.
    """
    version = LANGUAGE_VERSIONS.get(language)
    suffix = f"@{version}{extension}" if version is not None else extension
    paths = sorted(
        path
        for path in CASES_DIR.rglob(pattern=f"*{extension}")
        if path.name.endswith(suffix)
    )
    sys.stdout.buffer.write(b"".join(f"{p}".encode() + b"\0" for p in paths))
    return 0


if __name__ == "__main__":
    sys.exit(main(language=sys.argv[1], extension=sys.argv[2]))
