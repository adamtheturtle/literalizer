"""Fixture identifiers shared by generation and native staging."""

from pathlib import Path


def fixture_module_name(*, golden_path: Path) -> str:
    """Return a fixture's module name without its version suffix."""
    stem = golden_path.stem.rsplit(sep="@", maxsplit=1)[0]
    return f"Fixture_{golden_path.parent.name}_{stem}"
