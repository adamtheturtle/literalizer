"""Shared discovery for NewVariable identifier golden cases."""

import dataclasses
from pathlib import Path

import literalizer

from .language_specs import (
    lang_cls_name,
    make_golden_path,
    sorted_languages,
)


@dataclasses.dataclass(frozen=True)
class NewVariableNameCase:
    """A malformed or reserved identifier used in a golden case."""

    name: str
    variable_name: str


_BASE_CASES = (
    NewVariableNameCase(name="malformed", variable_name="a-b"),
    NewVariableNameCase(name="leading_digit", variable_name="1value"),
)


def normalizing_languages() -> list[literalizer.LanguageCls]:
    """Return languages that opt into NewVariable name normalization."""
    return [
        lang_cls
        for lang_cls in sorted_languages()
        if getattr(lang_cls, "normalizes_new_variable_names", False)
    ]


def cases_for_language(
    *, lang_cls: literalizer.LanguageCls
) -> tuple[NewVariableNameCase, ...]:
    """Return malformed, leading-digit, and reserved cases for a language."""
    reserved_cases = tuple(
        NewVariableNameCase(
            name=f"reserved_{reserved_identifier}",
            variable_name=reserved_identifier,
        )
        for reserved_identifier in sorted(lang_cls().reserved_identifiers)
    )
    return (*_BASE_CASES, *reserved_cases)


def expected_new_variable_golden_files(*, cases_dir: Path) -> set[Path]:
    """Return every golden path covered by the NewVariable test."""
    parent = cases_dir / "new_variable_names"
    return {
        make_golden_path(
            parent=parent,
            name=f"{case.name}_{lang_cls_name(cls=lang_cls)}",
            extension=lang_cls.extension,
            lang_cls=lang_cls,
            version=version_format,
        )
        for lang_cls in normalizing_languages()
        for case in cases_for_language(lang_cls=lang_cls)
        for version_format in lang_cls.VersionFormats
    }
