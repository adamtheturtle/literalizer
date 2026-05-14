"""Print null-byte-separated fixture paths for a language, filtered by
the pinned compiler version.

Each CI lint job that compiles per-language fixtures shells out to
this script instead of ``find``.  When the language is registered in
:data:`LANGUAGE_VERSIONS` the script keeps a ``{stem}@{version}{ext}``
variant in place of the base file and drops variants tagged for any
other version, so the lint job only sees code valid under the pinned
release.

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
    paths: list[Path] = []
    for path in sorted(CASES_DIR.rglob(pattern=f"*{extension}")):
        stem = path.stem
        if "@" in stem:
            if version is None or not stem.endswith(f"@{version}"):
                continue
        elif (
            version is not None
            and path.with_name(name=f"{stem}@{version}{extension}").is_file()
        ):
            continue
        paths.append(path)
    sys.stdout.buffer.write(b"".join(f"{p}".encode() + b"\0" for p in paths))
    return 0


if __name__ == "__main__":
    sys.exit(main(language=sys.argv[1], extension=sys.argv[2]))
