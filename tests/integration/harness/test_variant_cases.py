"""Focused tests for small variant-case helpers."""

import dataclasses
import enum
from pathlib import Path

import pytest

import literalizer.languages
from literalizer._language import redefinition_config
from tests.enum_members import enum_member_by_name
from tests.integration.case_manifests import (
    CaseManifestError,
    VariantCapabilityName,
    load_case_manifest,
    load_case_manifests,
)
from tests.integration.custom_languages import (
    variants_for_custom_language_axis,
)
from tests.integration.language_specs import make_spec, sorted_languages
from tests.integration.manifest_queries import (
    case_dir_names_for_variant_axis,
)
from tests.integration.variant_cases import (
    build_multiline_string_context_cases,
    build_variant_cases,
    group_variant_cases_by_language,
    one_special_input,
    variant_supports_capability,
    variants_for_axis,
)
from tests.integration.variant_types import VariantCase, compact_variant

_SampleEnum = enum.Enum(value="_SampleEnum", names=["FIRST"])


@pytest.mark.parametrize(
    argnames="axis",
    argvalues=["plain_collection_callbacks", "typed_collection_callback"],
)
def test_collection_callback_extensions_cover_every_language_version(
    axis: str,
) -> None:
    """Collection hooks retain native configuration across the matrix."""
    variants = variants_for_custom_language_axis(axis_key=axis)
    assert {
        (variant.lang_cls, variant.spec.language_version)
        for variant in variants
    } == {
        (lang_cls, version)
        for lang_cls in sorted_languages()
        for version in lang_cls.VersionFormats
    }
    for variant in variants:
        native = make_spec(
            lang_cls=variant.lang_cls,
            language_version=variant.spec.language_version,
        )
        for field in dataclasses.fields(class_or_instance=native):
            assert vars(variant.spec)[field.name] == vars(native)[field.name]
        assert variant.spec.sequence_open is not native.sequence_open
        assert (
            variant.spec.dict_format_config.dict_open
            is not native.dict_format_config.dict_open
        )


def test_enum_member_by_name_raises_for_missing_member() -> None:
    """Missing enum members raise a clear ValueError."""
    with pytest.raises(
        expected_exception=ValueError,
        match=r"^_SampleEnum has no member named 'SECOND'$",
    ):
        _ = enum_member_by_name(enum_cls=_SampleEnum, name="SECOND")


def test_special_axis_requires_one_manifest_input() -> None:
    """A special axis fails clearly when its manifest entry is missing."""
    with pytest.raises(
        expected_exception=CaseManifestError,
        match="requires exactly one manifest input",
    ):
        _ = one_special_input(entries=[], axis="modifiers")


def test_group_variant_cases_by_language_groups_by_variant_language() -> None:
    """Grouped cases stay aligned with the key language."""
    groups = group_variant_cases_by_language()

    assert set(groups) == set(literalizer.languages.ALL_LANGUAGES)
    for lang_cls, cases in groups.items():
        assert len(cases) > 0
        misgrouped = [
            case for case in cases if case.variant.lang_cls is not lang_cls
        ]
        assert misgrouped == []


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

    assert len(cases) > 0
    assert {case.variant.lang_cls for case in cases} == {
        lang_cls
        for lang_cls in literalizer.languages.ALL_LANGUAGES
        if lang_cls.supports_empty_sibling_sequence_type_hints
    }


def test_typed_dict_null_filtering_follows_capability() -> None:
    """Configured null-filtering variants cover every typed dict
    language.
    """
    variants = variants_for_axis(axis_key="typed_dict_null_filtering")
    expected = [
        lang_cls
        for lang_cls in sorted_languages()
        if lang_cls.supports_typed_dict_open
    ]

    assert [variant.lang_cls for variant in variants] == expected
    assert [variant.name for variant in variants] == [
        f"{lang_cls.__name__}_skip_null_dict_values" for lang_cls in expected
    ]
    for variant in variants:
        spec_cls = type(variant.spec)
        assert isinstance(spec_cls, literalizer.LanguageCls)
        assert spec_cls is variant.lang_cls
        assert variant.spec.skip_null_dict_values is True
        assert (
            make_spec(lang_cls=variant.lang_cls).skip_null_dict_values is False
        )
        assert make_spec(
            lang_cls=variant.lang_cls, skip_null_dict_values=False
        ) == make_spec(lang_cls=variant.lang_cls)


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

    assert len(case_dir_names) > 0
    for case_dir_name in case_dir_names:
        manifest = load_case_manifest(case_dir=cases_dir / case_dir_name)
        selected = {
            lang_cls
            for lang_cls in expected
            if manifest.selection.admits_language(lang_cls=lang_cls)
        }
        # The same manifest can also own non-multiline string variants.
        actual = {
            case.variant.lang_cls
            for case in build_variant_cases()
            if case.case_dir_name == case_dir_name
            and case.variant.spec.string_format.name == "MULTILINE"
            and not isinstance(
                case.variable_form,
                literalizer.BothVariableForms,
            )
        }
        assert actual == selected
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
        and case.variant.spec.string_format.name == "MULTILINE"
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
    indented_cases = [case for case in cases if case.pre_indent_level != 0]

    assert len(combined_cases) > 0
    misnamed_combined = [
        case
        for case in combined_cases
        if case.case_dir_name != combined_case_dir_name
        or not case.golden_name.endswith(combined_suffix)
    ]
    assert misnamed_combined == []
    assert {case.variant.lang_cls for case in combined_cases} == {
        lang_cls
        for lang_cls in literalizer.languages.ALL_LANGUAGES
        if lang_cls.supports_multiline_string_literals
        and any(
            redefinition_config(style).supports_redefinition
            for style in lang_cls.DeclarationStyles
        )
    }
    assert len(indented_cases) > 0
    misnamed_indented = [
        case
        for case in indented_cases
        if case.case_dir_name != pre_indent_case_dir_name
        or "_pre_indent_1_" not in case.golden_name
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


@pytest.mark.parametrize(
    argnames=("lang_cls", "spec"),
    argvalues=[
        (
            literalizer.languages.Cpp,
            make_spec(
                lang_cls=literalizer.languages.Cpp,
                json_type=enum_member_by_name(
                    enum_cls=literalizer.languages.Cpp.JsonTypes,
                    name="NLOHMANN_JSON",
                ),
                json_rendering=literalizer.languages.Cpp.JsonRenderings.INLINE_DOCUMENT,
            ),
        ),
        (
            literalizer.languages.Haskell,
            make_spec(
                lang_cls=literalizer.languages.Haskell,
                json_type=enum_member_by_name(
                    enum_cls=literalizer.languages.Haskell.JsonTypes,
                    name="AESON_VALUE",
                ),
            ),
        ),
    ],
)
def test_collection_comments_require_the_effective_configuration(
    lang_cls: literalizer.LanguageCls,
    spec: literalizer.Language,
) -> None:
    """JSON variants cannot borrow collection comment support from
    defaults.
    """
    variant = compact_variant(name="effective", lang_cls=lang_cls, spec=spec)
    assert variant_supports_capability(
        variant=dataclasses.replace(variant, spec=lang_cls()),
        capability="collection_comments",
    )
    assert not variant_supports_capability(
        variant=variant,
        capability="collection_comments",
    )
    # Removing the option restores support even after the disabled spec has
    # populated its cached capability property.
    reset_options: dict[str, object] = {"json_type": None}
    if lang_cls is literalizer.languages.Cpp:
        reset_options["json_rendering"] = None
    restored = dataclasses.replace(spec, **reset_options)
    assert variant_supports_capability(
        variant=dataclasses.replace(variant, spec=restored),
        capability="collection_comments",
    )
