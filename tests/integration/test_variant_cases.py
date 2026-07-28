"""Focused tests for small variant-case helpers."""

import enum
from collections import Counter

import pytest

from literalizer.languages import Kotlin, Python

from .case_discovery import EMPTY_SIBLING_SEQUENCE_TYPE_HINT_CASE_DIR
from .language_specs import sorted_languages
from .variant_cases import (
    _enum_member_by_name,  # pyright: ignore[reportPrivateUsage]
    build_typed_dict_null_filtering_variants,
    build_variant_cases,
    group_variant_cases_by_language,
    variant_languages,
)

_SampleEnum = enum.Enum("_SampleEnum", ["FIRST"])


def test_enum_member_by_name_raises_for_missing_member() -> None:
    """Missing enum members raise a clear ValueError."""
    with pytest.raises(
        expected_exception=ValueError,
        match=r"^_SampleEnum has no member named 'SECOND'$",
    ):
        _enum_member_by_name(enum_cls=_SampleEnum, name="SECOND")


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


def test_variant_cases_have_unique_golden_paths() -> None:
    """No two variant cases should exercise the same golden file."""
    targets = [
        (
            case.case_dir_name,
            case.variant_name,
            case.variant.spec.extension,
            case.variant.spec.language_version,
        )
        for case in build_variant_cases()
    ]
    duplicates = [
        target for target, count in Counter(targets).items() if count > 1
    ]

    assert duplicates == []


def test_empty_sibling_sequence_type_hints_follow_capability() -> None:
    """The time-union fixture excludes languages that cannot compile
    it.
    """
    cases = [
        case
        for case in build_variant_cases()
        if case.case_dir_name == EMPTY_SIBLING_SEQUENCE_TYPE_HINT_CASE_DIR
    ]

    assert cases
    assert not Kotlin.supports_empty_sibling_sequence_type_hints
    assert all(
        case.variant.lang_cls.supports_empty_sibling_sequence_type_hints
        for case in cases
    )
    assert any(case.variant.lang_cls is Python for case in cases)


def test_typed_dict_null_filtering_follows_capability() -> None:
    """Null-filtering variants select typed dict languages explicitly."""
    variants = list(build_typed_dict_null_filtering_variants())

    assert variants
    assert all(
        variant.lang_cls.supports_typed_dict_open for variant in variants
    )
