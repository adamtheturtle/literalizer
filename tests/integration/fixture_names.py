"""Fixture paths and identifiers for generation and native staging."""

import functools
from pathlib import Path

_NESTED_CASES = frozenset({"binary", "default_module_name"})


def nested_golden_path(
    *,
    case_dir: Path,
    stem: str,
    language_name: str,
    language_id: str,
    version: str,
    extension: str,
) -> Path | None:
    """Resolve the scenario path for a case using nested goldens."""
    if case_dir.name not in _NESTED_CASES:
        return None
    scenario = (
        "base"
        if stem.lower() == language_name.lower()
        else stem[len(language_name) + 1 :]
    )
    filename = f"{scenario}{extension}"
    return case_dir / "goldens" / language_id / version / filename


def _is_nested_golden(*, path: Path) -> bool:
    """Whether the fixture lives under a case's language and version."""
    return path.parent.parent.parent.name == "goldens"


def is_default_module_fixture(*, path: Path) -> bool:
    """Whether this fixture uses the language's public module name."""
    return _is_nested_golden(path=path) and path.stem == "default_module_name"


@functools.cache
def _fixture_language_name(*, language_id: str) -> str:
    """Look up the spelling used in existing generated identifiers."""
    # Ada staging can run with only the CLI dependencies installed.
    from literalizer.languages import ALL_LANGUAGES  # noqa: PLC0415

    from .language_metadata import language_metadata  # noqa: PLC0415

    language = next(
        cls for cls in ALL_LANGUAGES if cls.language_id == language_id
    )
    name = language.__name__
    if language_metadata(language_id=language_id).golden.filename_lowercase:
        name = name.lower()
    return name


def fixture_module_name(*, golden_path: Path) -> str:
    """Return the generated module name for either layout."""
    if not _is_nested_golden(path=golden_path):
        stem = golden_path.stem.rsplit(sep="@", maxsplit=1)[0]
        return f"Fixture_{golden_path.parent.name}_{stem}"
    case_name = golden_path.parent.parent.parent.parent.name
    language_name = _fixture_language_name(
        language_id=golden_path.parent.parent.name
    )
    scenario = golden_path.stem
    stem = (
        language_name if scenario == "base" else f"{language_name}_{scenario}"
    )
    return f"Fixture_{case_name}_{stem}"
