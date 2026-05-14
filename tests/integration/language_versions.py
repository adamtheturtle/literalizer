"""Active compiler/interpreter versions per language for golden-file
selection and CI linters.

A language listed here may have version-specific golden variants on disk
named ``{stem}@{version}{extension}`` alongside the unversioned
``{stem}{extension}``.  Tests prefer the versioned variant when it
exists for the active version; CI linters filter the fixture set the
same way before invoking the compiler.

The active version may be overridden at runtime via the
``LITERALIZER_LANG_VERSION_<NAME>`` env var (e.g.
``LITERALIZER_LANG_VERSION_ODIN=dev-2026-05``) so a one-off run can
exercise a different toolchain without editing this file.
"""

import os

from beartype import beartype

import literalizer

LANGUAGE_VERSIONS: dict[str, str] = {
    "Odin": "dev-2026-04",
}


@beartype
def language_version_for(lang_cls: literalizer.LanguageCls) -> str | None:
    """Return the active version string for *lang_cls*, or ``None``."""
    name = lang_cls.__name__
    env_key = f"LITERALIZER_LANG_VERSION_{name.upper()}"
    if env_key in os.environ:
        return os.environ[env_key]
    return LANGUAGE_VERSIONS.get(name)
