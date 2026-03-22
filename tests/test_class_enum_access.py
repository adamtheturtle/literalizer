"""Test class-level format Enum access via HasFormatEnums."""

from literalizer import HasFormatEnums
from literalizer.languages import (
    Ada,
    Bash,
    Cpp,
    Python,
)

_LANGUAGE_TYPES: dict[str, HasFormatEnums] = {
    "ada": Ada,
    "bash": Bash,
    "cpp": Cpp,
    "python": Python,
}

_SEQUENCE_FORMATS: dict[tuple[str, str], object] = {
    (lang_name, member.name.lower()): member
    for lang_name, lang_cls in _LANGUAGE_TYPES.items()
    for member in lang_cls.SequenceFormats
}

_SET_FORMATS: dict[tuple[str, str], object] = {
    (lang_name, member.name.lower()): member
    for lang_name, lang_cls in _LANGUAGE_TYPES.items()
    for member in lang_cls.SetFormats
}

_BYTES_FORMATS: dict[tuple[str, str], object] = {
    (lang_name, member.name.lower()): member
    for lang_name, lang_cls in _LANGUAGE_TYPES.items()
    for member in lang_cls.BytesFormats
}

_DATE_FORMATS: dict[tuple[str, str], object] = {
    (lang_name, member.name.lower()): member
    for lang_name, lang_cls in _LANGUAGE_TYPES.items()
    for member in lang_cls.DateFormats
}

_DATETIME_FORMATS: dict[tuple[str, str], object] = {
    (lang_name, member.name.lower()): member
    for lang_name, lang_cls in _LANGUAGE_TYPES.items()
    for member in lang_cls.DatetimeFormats
}

_VARIABLE_TYPE_HINTS: dict[tuple[str, str], object] = {
    (lang_name, member.name.lower()): member
    for lang_name, lang_cls in _LANGUAGE_TYPES.items()
    for member in lang_cls.VariableTypeHints
}


def test_sequence_formats_populated() -> None:
    """Each language contributes at least one sequence format."""
    for lang_name in _LANGUAGE_TYPES:
        assert any(k[0] == lang_name for k in _SEQUENCE_FORMATS)


def test_set_formats_populated() -> None:
    """Each language contributes at least one set format."""
    for lang_name in _LANGUAGE_TYPES:
        assert any(k[0] == lang_name for k in _SET_FORMATS)


def test_bytes_formats_populated() -> None:
    """Each language contributes at least one bytes format."""
    for lang_name in _LANGUAGE_TYPES:
        assert any(k[0] == lang_name for k in _BYTES_FORMATS)


def test_date_formats_populated() -> None:
    """Each language contributes at least one date format."""
    for lang_name in _LANGUAGE_TYPES:
        assert any(k[0] == lang_name for k in _DATE_FORMATS)


def test_datetime_formats_populated() -> None:
    """Each language contributes at least one datetime format."""
    for lang_name in _LANGUAGE_TYPES:
        assert any(k[0] == lang_name for k in _DATETIME_FORMATS)


def test_variable_type_hints_populated() -> None:
    """Each language contributes at least one variable type hint
    option.
    """
    for lang_name in _LANGUAGE_TYPES:
        assert any(k[0] == lang_name for k in _VARIABLE_TYPE_HINTS)
