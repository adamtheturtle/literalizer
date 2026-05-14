"""Active compiler version per language for golden-file selection.

A language listed in :data:`LANGUAGE_VERSIONS` may have version-tagged
golden variants named ``{stem}@{version}{extension}`` alongside the
base ``{stem}{extension}``.  The integration tests prefer the tagged
variant when the active version matches; the CI compile job filters
fixtures the same way so it only compiles variants for the pinned
release.
"""

from beartype import beartype

import literalizer

LANGUAGE_VERSIONS: dict[str, str] = {
    "Odin": "dev-2026-04",
}


@beartype
def language_version_for(lang_cls: literalizer.LanguageCls) -> str | None:
    """Return the active version string for *lang_cls*, or ``None``."""
    return LANGUAGE_VERSIONS.get(lang_cls.__name__)
