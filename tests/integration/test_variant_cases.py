"""Focused tests for small variant-case helpers."""

import enum
from collections import Counter

import pytest

import literalizer.languages
from literalizer.languages import Kotlin, Python

from .case_discovery import EMPTY_SIBLING_SEQUENCE_TYPE_HINT_CASE_DIR
from .case_manifests import CaseManifestError, ManifestVariant, RenderContext
from .language_specs import sorted_languages
from .variant_cases import (
    _case_for_manifest_variant,  # pyright: ignore[reportPrivateUsage]
    _one_special_input,  # pyright: ignore[reportPrivateUsage]
    build_multiline_string_context_cases,
    build_typed_dict_null_filtering_variants,
    build_variant_cases,
    group_variant_cases_by_language,
    variant_languages,
)
from .variant_types import enum_member_by_name

_SampleEnum = enum.Enum("_SampleEnum", ["FIRST"])


def test_enum_member_by_name_raises_for_missing_member() -> None:
    """Missing enum members raise a clear ValueError."""
    with pytest.raises(
        expected_exception=ValueError,
        match=r"^_SampleEnum has no member named 'SECOND'$",
    ):
        enum_member_by_name(enum_cls=_SampleEnum, name="SECOND")


def test_manifest_variant_context_overrides_collection_layout() -> None:
    """A manifest variant can select multiline collection rendering."""
    source_case = build_variant_cases()[0]
    case = _case_for_manifest_variant(
        case_dir_name="example",
        manifest_variant=ManifestVariant(
            axis="date",
            context=RenderContext(collection_layout="multiline"),
        ),
        variant=source_case.variant,
    )

    assert (
        case.variant.collection_layout
        is literalizer.CollectionLayout.MULTILINE
    )


def test_special_axis_requires_one_manifest_input() -> None:
    """A special axis fails clearly when its manifest entry is missing."""
    with pytest.raises(
        expected_exception=CaseManifestError,
        match="requires exactly one manifest input",
    ):
        _one_special_input(entries=[], axis="modifiers")


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


def test_multiline_string_variants_follow_capability() -> None:
    """Only explicit multiline-capability languages join the axis."""
    expected = {
        lang_cls
        for lang_cls in literalizer.languages.ALL_LANGUAGES
        if lang_cls.supports_multiline_string_literals
    }

    for case_dir_name in (
        "multiline_string",
        "multiline_string_scalar",
        "multiline_string_nested",
    ):
        actual = {
            case.variant.lang_cls
            for case in build_variant_cases()
            if case.case_dir_name == case_dir_name
            and not isinstance(
                case.variable_form,
                literalizer.BothVariableForms,
            )
        }
        assert actual == expected
    assert all(
        enum_member_by_name(
            enum_cls=lang_cls.StringFormats,
            name="MULTILINE",
        ).name
        == "MULTILINE"
        for lang_cls in expected
    )

    context_cases = [
        case
        for case in build_variant_cases()
        if case.case_dir_name
        in {
            "multiline_string",
            "multiline_string_scalar",
            "multiline_string_nested",
        }
    ]
    assert {case.variant.lang_cls for case in context_cases} == expected
    assert all(
        case.variant.lang_cls.supports_multiline_string_literals
        for case in context_cases
    )


def test_multiline_context_cases_follow_capabilities() -> None:
    """Assignment and indentation contexts follow language metadata."""
    combined_suffix = "_combined"
    combined_case_dir_name = "multiline_string_scalar"
    pre_indent_case_dir_name = "multiline_string_scalar"
    cases = build_multiline_string_context_cases(
        combined_case_dir_name=combined_case_dir_name,
        combined_suffix=combined_suffix,
        combined_variable_form=literalizer.BothVariableForms(
            name="my_data",
            modifiers=frozenset(),
        ),
        pre_indent_case_dir_name=pre_indent_case_dir_name,
        pre_indent_level=1,
    )
    combined_cases = [
        case
        for case in cases
        if isinstance(case.variable_form, literalizer.BothVariableForms)
    ]
    indented_cases = [case for case in cases if case.pre_indent_level]

    assert combined_cases
    assert all(
        isinstance(case.variable_form, literalizer.BothVariableForms)
        for case in combined_cases
    )
    assert all(
        case.case_dir_name == combined_case_dir_name
        and case.variant_name.endswith(combined_suffix)
        for case in combined_cases
    )
    assert {case.variant.lang_cls for case in combined_cases} == {
        lang_cls
        for lang_cls in literalizer.languages.ALL_LANGUAGES
        if lang_cls.supports_multiline_string_literals
        and any(
            style.value.supports_redefinition
            for style in lang_cls.DeclarationStyles
        )
    }
    assert indented_cases
    assert all(
        case.case_dir_name == pre_indent_case_dir_name
        and "_pre_indent_1_" in case.variant_name
        for case in indented_cases
    )
    assert all(case.pre_indent_level == 1 for case in indented_cases)
    assert all(
        case.variant.lang_cls.supports_multiline_string_literals
        for case in indented_cases
    )
