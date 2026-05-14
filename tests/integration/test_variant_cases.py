"""Focused tests for small variant-case helpers."""

import enum

import pytest

from literalizer.languages import Python

from .language_specs import sorted_languages
from .variant_cases import (
    _enum_member_by_name,  # pyright: ignore[reportPrivateUsage]
    group_variant_cases_by_language,
    variant_languages,
)

_SAMPLE_ENUM = enum.Enum("_SampleEnum", ["FIRST"])


def test_enum_member_by_name_raises_for_missing_member() -> None:
    """Missing enum members raise a clear ValueError."""
    with pytest.raises(
        expected_exception=ValueError,
        match=r"^_SampleEnum has no member named 'SECOND'$",
    ):
        _enum_member_by_name(enum_cls=_SAMPLE_ENUM, name="SECOND")


def test_group_variant_cases_by_language_groups_by_variant_language() -> None:
    """Grouped cases stay aligned with the key language."""
    groups = group_variant_cases_by_language()

    assert groups
    assert Python in groups
    for lang_cls, cases in groups.items():
        assert cases
        assert all(case.variant.lang_cls is lang_cls for case in cases)


def test_variant_languages_matches_sorted_group_keys() -> None:
    """Variant languages are the sorted subset that actually have
    cases.
    """
    groups = group_variant_cases_by_language()

    assert variant_languages() == [
        lang_cls for lang_cls in sorted_languages() if lang_cls in groups
    ]
