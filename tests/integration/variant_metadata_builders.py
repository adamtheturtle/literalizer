"""Builders driven by declared metadata rather than by concrete languages.

The language classes describe supported behaviors and compatibility
rules, and the test-owned language metadata files describe which focused
golden variants a language opts into; these builders translate both into
variants without depending on individual language classes.
"""

from __future__ import annotations

import enum  # noqa: TC003  # Runtime-resolved by beartype.
from collections.abc import Iterable, Mapping  # noqa: TC003

from beartype import beartype

import literalizer

from .language_metadata import language_metadata
from .language_specs import make_spec, sorted_languages
from .variant_types import (
    Variant,
    VariantCase,
    compact_variant,
    enum_member_by_name,
)

_enum_member_by_name = enum_member_by_name


@beartype
def build_collection_layout_variants() -> Iterable[Variant]:
    """Build variants for every collection-layout option."""
    variants: list[Variant] = []
    for lang_cls in sorted_languages():
        golden = language_metadata(language_id=lang_cls.language_id).golden
        name_prefix = (
            f"{lang_cls.__name__}_{golden.collection_layout_category}"
        )
        variants.extend(
            Variant(
                name=f"{name_prefix}_{layout.value}",
                spec=make_spec(lang_cls=lang_cls),
                lang_cls=lang_cls,
                collection_layout=layout,
                fixture_prefix="",
                record_null_substitutions=None,
            )
            for layout in literalizer.CollectionLayout
        )
    return variants


@beartype
def _nested_map_scalar_wrapping_spec(
    *,
    lang_cls: literalizer.LanguageCls,
) -> literalizer.Language | None:
    """Return *lang_cls*'s nested-map scalar-wrapping spec, if any."""
    default_spec = make_spec(lang_cls=lang_cls)
    for strategy in default_spec.heterogeneous_strategies:
        alternative = make_spec(
            lang_cls=lang_cls,
            heterogeneous_strategy=strategy,
        )
        behavior = alternative.heterogeneous_behavior
        if behavior.widens_nested_maps_by_wrapping_scalars:
            return alternative
    return None


@beartype
def build_nested_map_widening_variants() -> Iterable[Variant]:
    """Build the ``nested_map_widening`` variants.

    Sibling dict values that are themselves maps share one declared
    value type in the enclosing container, but each inner map otherwise
    renders with its own narrowed opener, so a map narrower than the
    widened slot type does not compile (issue #2878; the dict-value
    analogue of the sibling widening #1471/#1472 applied to call
    arguments and sequence elements).  Go widens every such inner map to
    ``map[string]any`` (#2878) and Kotlin widens the element maps to
    ``mapOf<String, Map<String, Any?>>`` (#2890) so each literal matches
    its declared type.  Rust's ``TAGGED_ENUM`` strategy instead wraps the
    scalar leaves of every sibling map in the ``Value`` enum (#2879), and
    the Nim ``OBJECT_VARIANT`` strategy wraps them in its object-variant
    ``Value`` so every inner ``Table`` shares one value type (#2898).
    The Mojo ``VARIANT`` strategy wraps them in its ``Value`` alias so
    every inner ``Dict`` shares one value type (#2895).  The V
    ``INTERFACE`` strategy wraps them in ``IVal`` so every inner
    ``map`` shares one value type (#2896). C++'s ``RECORD`` strategy
    wraps them in a shared ``std::variant`` value alias (#2917). Dhall's
    ``UNION_TYPE`` strategy has the analogous fix (#2897) but is covered
    by :func:`build_dhall_nested_map_widening_variants` against a
    dedicated input, because Dhall's record typing cannot represent this
    input's divergent inner key sets.
    Only languages that can widen participate today, so
    the variant stays out of the all-languages base discovery; both
    layouts are covered because the compact and multiline paths render
    the widened literals separately.
    """
    variants: list[Variant] = [
        variant
        for lang_cls in sorted_languages()
        if language_metadata(
            language_id=lang_cls.language_id
        ).variants.nested_map_widening
        == "default"
        for variant in (
            compact_variant(
                name=f"{lang_cls.__name__}_nested_map_widening",
                spec=make_spec(lang_cls=lang_cls),
                lang_cls=lang_cls,
            ),
            Variant(
                name=f"{lang_cls.__name__}_nested_map_widening_multiline",
                spec=make_spec(lang_cls=lang_cls),
                lang_cls=lang_cls,
                collection_layout=literalizer.CollectionLayout.MULTILINE,
                fixture_prefix="",
                record_null_substitutions=None,
            ),
        )
    ]
    for lang_cls in sorted_languages():
        metadata = language_metadata(language_id=lang_cls.language_id)
        if metadata.variants.nested_map_widening == "uniform_keys":
            continue
        spec = _nested_map_scalar_wrapping_spec(lang_cls=lang_cls)
        if spec is None:
            continue
        variants.extend(
            [
                compact_variant(
                    name=f"{lang_cls.__name__}_nested_map_widening",
                    spec=spec,
                    lang_cls=lang_cls,
                ),
                Variant(
                    name=(
                        f"{lang_cls.__name__}_nested_map_widening_multiline"
                    ),
                    spec=spec,
                    lang_cls=lang_cls,
                    collection_layout=(literalizer.CollectionLayout.MULTILINE),
                    fixture_prefix="",
                    record_null_substitutions=None,
                ),
            ]
        )
    return variants


@beartype
def build_dhall_nested_map_widening_variants() -> Iterable[Variant]:
    """Build nested-map variants that require uniform inner keys.

    This mirrors :func:`build_nested_map_widening_variants` for Dhall's
    ``UNION_TYPE`` strategy, but uses a dedicated input.  Dhall renders
    dicts as records whose type is fixed by their field set, so the
    shared ``nested_map_widening`` input (whose sibling inner maps also
    differ in *which* keys they carry) can never type-check as a Dhall
    list regardless of widening.  This input keeps every sibling inner
    map at the same key set while diverging its scalar value types, so
    the widening fix (wrapping every sibling map's scalar leaves in the
    ``Value`` union) is exactly what makes the list type-check (#2897).
    """
    variants: list[Variant] = []
    for lang_cls in sorted_languages():
        metadata = language_metadata(language_id=lang_cls.language_id)
        if metadata.variants.nested_map_widening != "uniform_keys":
            continue
        spec = _nested_map_scalar_wrapping_spec(lang_cls=lang_cls)
        assert spec is not None  # noqa: S101
        variants.extend(
            (
                compact_variant(
                    name=f"{lang_cls.__name__}_nested_map_widening",
                    spec=spec,
                    lang_cls=lang_cls,
                ),
                Variant(
                    name=(
                        f"{lang_cls.__name__}_nested_map_widening_multiline"
                    ),
                    spec=spec,
                    lang_cls=lang_cls,
                    collection_layout=literalizer.CollectionLayout.MULTILINE,
                    fixture_prefix="",
                    record_null_substitutions=None,
                ),
            )
        )
    return variants


@beartype
def build_empty_map_narrowing_variants() -> Iterable[Variant]:
    """Build the ``empty_map_narrowing`` variants.

    An empty map beside a non-empty map sibling must borrow the
    sibling's concrete key/value types, or the empty literal's fallback
    type disagrees with the sibling and the list fails to compile (V
    issue #3015: ``[map[string]IVal{}, {'x': 1}]`` is rejected because
    the ``int`` value cannot coerce to the ``IVal`` interface; Rust
    issue #3013: ``HashMap::<String, String>::from([])`` disagrees with
    the sibling ``HashMap<&str, i32>``).  Only languages whose
    ``dict_format_config`` declares a ``narrowed_empty_form`` narrow the
    empty map this way, so the case stays out of the all-languages base
    discovery (other statically typed languages have their own,
    still-divergent handling of this shape).
    """
    variants: list[Variant] = []
    for lang_cls in sorted_languages():
        spec = make_spec(lang_cls=lang_cls)
        if spec.dict_format_config.narrowed_empty_form is None:
            continue
        variants.extend(
            (
                compact_variant(
                    name=f"{lang_cls.__name__}_empty_map_narrowing",
                    spec=spec,
                    lang_cls=lang_cls,
                ),
                Variant(
                    name=f"{lang_cls.__name__}_empty_map_narrowing_multiline",
                    spec=spec,
                    lang_cls=lang_cls,
                    collection_layout=literalizer.CollectionLayout.MULTILINE,
                    fixture_prefix="",
                    record_null_substitutions=None,
                ),
            )
        )
    return variants


@beartype
def build_modifier_variant_cases(
    *,
    case_dir_names: tuple[str, ...],
    sequence_case_dirs: Mapping[str, str],
) -> list[VariantCase]:
    """Build variants exercising per-language modifier rendering.

    For every language with a non-empty ``modifiers`` enum, emit one
    singleton-modifier variant per member plus one variant per entry
    in ``lang_cls.modifier_combinations``.  Each variant runs against
    inputs covering scalar / dict / set / date / datetime values so
    each branch of typed-declaration inference is exercised;
    combinations the language rejects at literalize time are skipped
    by the test itself.
    """
    cases: list[VariantCase] = []
    for lang_cls in sorted_languages():
        spec = make_spec(lang_cls=lang_cls)
        if len(spec.modifiers) == 0:
            continue
        entries: list[tuple[str, frozenset[enum.Enum]]] = [
            (member.name.lower(), frozenset({member}))
            for member in spec.modifiers
        ]
        entries.extend(
            (combo.name, combo.modifiers)
            for combo in lang_cls.modifier_combinations
        )
        for mod_name, modifiers in entries:
            variant = compact_variant(
                name=f"{lang_cls.__name__}_modifiers_{mod_name}",
                spec=make_spec(lang_cls=lang_cls),
                lang_cls=lang_cls,
            )
            cases.extend(
                VariantCase(
                    variant_name=variant.name,
                    variant=variant,
                    case_dir_name=case_dir_name,
                    variable_form=literalizer.NewVariable(
                        name="my_data",
                        modifiers=modifiers,
                    ),
                    pre_indent_level=0,
                )
                for case_dir_name in case_dir_names
            )

    # Some modifiers require a non-default sequence representation for typed
    # declarations.  The compatibility mapping belongs to the language; this
    # matrix supplies the sequence inputs that exercise it.
    for lang_cls in sorted_languages():
        default_spec = make_spec(lang_cls=lang_cls)
        overrides = (
            lang_cls.variant_metadata.modifier_sequence_format_overrides
        )
        for (
            modifier_name,
            sequence_format_name,
        ) in overrides.items():
            modifier = _enum_member_by_name(
                enum_cls=default_spec.modifiers,
                name=modifier_name,
            )
            sequence_format = _enum_member_by_name(
                enum_cls=default_spec.sequence_formats,
                name=sequence_format_name,
            )
            for suffix, case_dir_name in sequence_case_dirs.items():
                variant = compact_variant(
                    name=(
                        f"{lang_cls.__name__}_modifiers_"
                        f"{modifier_name.lower()}_{suffix}"
                    ),
                    spec=make_spec(
                        lang_cls=lang_cls,
                        sequence_format=sequence_format,
                    ),
                    lang_cls=lang_cls,
                )
                cases.append(
                    VariantCase(
                        variant_name=variant.name,
                        variant=variant,
                        case_dir_name=case_dir_name,
                        variable_form=literalizer.NewVariable(
                            name="my_data",
                            modifiers=frozenset({modifier}),
                        ),
                        pre_indent_level=0,
                    )
                )

    return cases
