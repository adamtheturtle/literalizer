"""Focused tests for small variant-case helpers."""

import enum
from collections import Counter
from pathlib import Path

import pytest

import literalizer.languages
from literalizer.languages import Kotlin, Python
from tests.enum_members import enum_member_by_name

from .case_manifests import (
    CaseManifestError,
    ManifestVariant,
    RenderContext,
    VariantCapabilityName,
    case_dir_names_for_variant_axis,
    load_case_manifests,
)
from .language_specs import sorted_languages
from .variant_cases import (
    _case_for_manifest_variant,  # pyright: ignore[reportPrivateUsage]
    _one_special_input,  # pyright: ignore[reportPrivateUsage]
    build_multiline_string_context_cases,
    build_variant_cases,
    group_variant_cases_by_language,
    variant_languages,
)
from .variant_escape_hatches import build_typed_dict_null_filtering_variants
from .variant_types import VariantCase

_SampleEnum = enum.Enum(value="_SampleEnum", names=["FIRST"])


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
        misgrouped = [
            case for case in cases if case.variant.lang_cls is not lang_cls
        ]
        assert misgrouped == []


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


def _cases_requiring(
    *,
    cases_dir: Path,
    capability: VariantCapabilityName,
) -> list[VariantCase]:
    """Return the variant cases whose manifest declares *capability*."""
    declared = {
        manifest.case_dir.name
        for manifest in load_case_manifests(cases_dir=cases_dir)
        for variant in manifest.variants
        if capability in variant.requires
    }
    return [
        case
        for case in build_variant_cases()
        if case.case_dir_name in declared
    ]


def test_empty_sibling_sequence_type_hints_follow_capability(
    cases_dir: Path,
) -> None:
    """A case requiring empty sibling sequence hints excludes languages
    that cannot compile it.
    """
    cases = _cases_requiring(
        cases_dir=cases_dir,
        capability="empty_sibling_sequence_type_hints",
    )

    assert cases
    assert not Kotlin.supports_empty_sibling_sequence_type_hints
    incapable = [
        case
        for case in cases
        if not case.variant.lang_cls.supports_empty_sibling_sequence_type_hints
    ]
    assert incapable == []
    assert any(case.variant.lang_cls is Python for case in cases)


def test_typed_dict_null_filtering_follows_capability() -> None:
    """Null-filtering variants select typed dict languages explicitly."""
    variants = list(build_typed_dict_null_filtering_variants())

    assert variants
    incapable = [
        variant
        for variant in variants
        if not variant.lang_cls.supports_typed_dict_open
    ]
    assert incapable == []


def test_multiline_string_variants_follow_capability(
    cases_dir: Path,
) -> None:
    """Only explicit multiline-capability languages join the axis."""
    expected = {
        lang_cls
        for lang_cls in literalizer.languages.ALL_LANGUAGES
        if lang_cls.supports_multiline_string_literals
    }
    case_dir_names = case_dir_names_for_variant_axis(
        cases_dir=cases_dir,
        axis="multiline_string",
    )

    assert case_dir_names
    for case_dir_name in case_dir_names:
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
    multiline_members = {
        lang_cls: enum_member_by_name(
            enum_cls=lang_cls.StringFormats,
            name="MULTILINE",
        ).name
        for lang_cls in expected
    }
    assert multiline_members == dict.fromkeys(expected, "MULTILINE")

    context_cases = [
        case
        for case in build_variant_cases()
        if case.case_dir_name in set(case_dir_names)
    ]
    assert {case.variant.lang_cls for case in context_cases} == expected
    incapable = [
        case
        for case in context_cases
        if not case.variant.lang_cls.supports_multiline_string_literals
    ]
    assert incapable == []


def test_multiline_context_cases_follow_capabilities(
    cases_dir: Path,
) -> None:
    """Assignment and indentation contexts follow language metadata."""
    combined_suffix = "_combined"
    (combined_case_dir_name,) = case_dir_names_for_variant_axis(
        cases_dir=cases_dir,
        axis="multiline_string_combined",
    )
    (pre_indent_case_dir_name,) = case_dir_names_for_variant_axis(
        cases_dir=cases_dir,
        axis="multiline_string_pre_indent",
    )
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
    misnamed_combined = [
        case
        for case in combined_cases
        if case.case_dir_name != combined_case_dir_name
        or not case.variant_name.endswith(combined_suffix)
    ]
    assert misnamed_combined == []
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
    misnamed_indented = [
        case
        for case in indented_cases
        if case.case_dir_name != pre_indent_case_dir_name
        or "_pre_indent_1_" not in case.variant_name
    ]
    assert misnamed_indented == []
    assert [case.pre_indent_level for case in indented_cases] == [1] * len(
        indented_cases
    )
    incapable_indented = [
        case
        for case in indented_cases
        if not case.variant.lang_cls.supports_multiline_string_literals
    ]
    assert incapable_indented == []
