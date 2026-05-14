"""Active compiler version per language for golden-file selection.

A language listed in :data:`LANGUAGE_VERSIONS` may have version-tagged
golden variants named ``{stem}@{version}{extension}`` alongside the
base ``{stem}{extension}``.  The integration tests prefer the tagged
variant when the active version matches; the CI compile step filters
fixtures the same way so it only compiles variants for the pinned
release.

This module is kept import-free so ``list_fixtures.py`` can read the
same registry without pulling in the project test dependencies.
"""

LANGUAGE_VERSIONS: dict[str, str] = {
    "Elixir": "1.18",
    "Erlang": "27",
    "Gleam": "v1.16.0",
    "Kotlin": "2.3.20",
    "Odin": "dev-2026-04",
    "Zig": "0.14.0",
}
