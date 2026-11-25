"""Fixture paths and identifiers for generation and native staging."""

import functools
from pathlib import Path


def is_default_module_fixture(*, path: Path) -> bool:
    """Whether this fixture uses the language's public module name."""
    return path.stem == "default_module_name"


@functools.cache
def _fixture_language_name(*, language_id: str) -> str:
    """Look up the spelling used in existing generated identifiers."""
    # Ada staging can run with only the command-line dependencies installed.
    # pylint: disable=import-outside-toplevel
    from literalizer.languages import ALL_LANGUAGES  # noqa: PLC0415

    from .language_metadata import language_metadata  # noqa: PLC0415
    # pylint: enable=import-outside-toplevel

    language = next(
        cls for cls in ALL_LANGUAGES if cls.language_id == language_id
    )
    name = language.__name__
    if language_metadata(language_id=language_id).golden.filename_lowercase:
        name = name.lower()
    return name


def fixture_module_name(*, golden_path: Path) -> str:
    """Reconstruct the module identifier embedded in the fixture."""
    case_name = golden_path.parents[3].name
    language_name = _fixture_language_name(
        language_id=golden_path.parents[1].name
    )
    scenario = golden_path.stem
    stem = (
        language_name if scenario == "base" else f"{language_name}_{scenario}"
    )
    return f"Fixture_{case_name}_{stem}"
