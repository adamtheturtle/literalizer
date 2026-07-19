"""Builders driven by language-owned integration-variant metadata.

The language classes describe supported behaviors and compatibility rules;
these builders translate that metadata into variants without depending on
individual language classes.
"""

from __future__ import annotations

import enum  # noqa: TC003  # Runtime-resolved by beartype.
from collections.abc import Iterable  # noqa: TC003  # Runtime beartype hint.

from beartype import beartype

import literalizer
from literalizer._language import (
    NestedMapWideningVariant,
    RecordVariant,
)

from .language_specs import make_spec, sorted_languages
from .variant_types import Variant, VariantCase, enum_member_by_name

_enum_member_by_name = enum_member_by_name


@beartype
def build_collection_layout_variants() -> Iterable[Variant]:
    """Build variants for every collection-layout option."""
    variants: list[Variant] = []
    for lang_cls in sorted_languages():
        name_prefix = (
            f"{lang_cls.__name__}_"
            f"{lang_cls.variant_metadata.collection_layout_category}"
        )
        variants.extend(
            Variant(
                name=f"{name_prefix}_{layout.value}",
                spec=make_spec(lang_cls=lang_cls),
                lang_cls=lang_cls,
                collection_layout=layout,
            )
            for layout in literalizer.CollectionLayout
        )
    return variants


@beartype
def build_record_unify_optional_fields_variants() -> Iterable[Variant]:
    """Build every supported ``record_unify_optional_fields`` variant.

    Combines :attr:`Rust.record_unify_optional_fields` with the
    ``RECORD`` heterogeneous strategy so the golden case exercises the
    Option/Some/None rendering.  Only Rust currently has this knob.
    """
    variants: list[Variant] = []
    for lang_cls in sorted_languages():
        if (
            RecordVariant.UNIFY_OPTIONAL_FIELDS
            not in lang_cls.variant_metadata.record_variants
        ):
            continue
        default_spec = make_spec(lang_cls=lang_cls)
        record_strategy = next(
            strategy
            for strategy in default_spec.heterogeneous_strategies
            if strategy.name == "RECORD"
        )
        spec = make_spec(
            lang_cls=lang_cls,
            heterogeneous_strategy=record_strategy,
            record_unify_optional_fields=True,
        )
        variants.append(
            Variant(
                name=f"{lang_cls.__name__}_record_unify_optional_fields",
                spec=spec,
                lang_cls=lang_cls,
                collection_layout=literalizer.CollectionLayout.COMPACT,
            )
        )
    return variants


@beartype
def build_record_nonrecord_dict_field_variants() -> Iterable[Variant]:
    """Build the C# and Nim non-record-dict field variants.

    The input has an empty dict field inside a record-shaped dict.  The
    C# variant renders its documented ``object`` fallback, while the
    integration runner skips Nim after its documented rejection.  This
    covers both outcomes of the cross-language decision in #2317 through
    the public API.
    """
    variants: list[Variant] = []
    for lang_cls in sorted_languages():
        if (
            RecordVariant.NONRECORD_DICT_FIELD
            not in lang_cls.variant_metadata.record_variants
        ):
            continue
        default_spec = make_spec(lang_cls=lang_cls)
        record_strategy = next(
            strategy
            for strategy in default_spec.heterogeneous_strategies
            if strategy.name == "RECORD"
        )
        variants.append(
            Variant(
                name=f"{lang_cls.__name__}_record_nonrecord_dict_field",
                spec=make_spec(
                    lang_cls=lang_cls,
                    heterogeneous_strategy=record_strategy,
                ),
                lang_cls=lang_cls,
                collection_layout=literalizer.CollectionLayout.COMPACT,
            )
        )
    return variants


@beartype
def build_record_keyword_field_variants() -> Iterable[Variant]:
    """Build keyword-field variants for languages that escape them.

    Dict keys that collide with a target-language keyword must render
    as escaped field names in both the generated struct declaration and
    its literals, or the output fails to compile.  Rust escapes its
    keywords (``type``, ``match``) as raw identifiers (``r#type``, issue
    #2880); Zig escapes its keywords (``error``, ``switch``) as quoted
    identifiers (``@"error"``, issue #2963).  The shared case input
    carries every participating language's keywords; a key that is not
    one language's keyword renders verbatim there.  Only languages that
    escape keyword field names opt in via ``RecordVariant.KEYWORD_FIELD``,
    so the case directory stays out of the all-languages base discovery.
    """
    variants: list[Variant] = []
    for lang_cls in sorted_languages():
        if (
            RecordVariant.KEYWORD_FIELD
            not in lang_cls.variant_metadata.record_variants
        ):
            continue
        default_spec = make_spec(lang_cls=lang_cls)
        record_strategy = next(
            strategy
            for strategy in default_spec.heterogeneous_strategies
            if strategy.name == "RECORD"
        )
        variants.append(
            Variant(
                name=f"{lang_cls.__name__}_record_keyword_field",
                spec=make_spec(
                    lang_cls=lang_cls,
                    heterogeneous_strategy=record_strategy,
                ),
                lang_cls=lang_cls,
                collection_layout=literalizer.CollectionLayout.COMPACT,
            )
        )
    return variants


@beartype
def build_record_field_type_split_variants() -> Iterable[Variant]:
    """Build the ``record_field_type_split`` variants.

    Same-key-set dicts whose field types conflict (a nested record
    with different fields, differing scalar types) must resolve to
    distinct generated struct declarations, or the struct declared
    from the field types of the first dict fails to compile against
    the literal for the other dict (issue #2881 for Rust, #2888 for
    the shared non-Rust ports).  The case input keeps every
    conflicting pair out of sibling lists so each group renders as its
    own compiling struct.  Rust splits via its own
    ``_refine_record_shapes`` while Go splits through the shared
    record strategy's field-type refinement, so the two are the only
    consumers and the case directory stays out of the all-languages
    base discovery.
    """
    variants: list[Variant] = []
    for lang_cls in sorted_languages():
        if (
            RecordVariant.FIELD_TYPE_SPLIT
            not in lang_cls.variant_metadata.record_variants
        ):
            continue
        default_spec = make_spec(lang_cls=lang_cls)
        record_strategy = next(
            strategy
            for strategy in default_spec.heterogeneous_strategies
            if strategy.name == "RECORD"
        )
        variants.append(
            Variant(
                name=f"{lang_cls.__name__}_record_field_type_split",
                spec=make_spec(
                    lang_cls=lang_cls,
                    heterogeneous_strategy=record_strategy,
                ),
                lang_cls=lang_cls,
                collection_layout=literalizer.CollectionLayout.COMPACT,
            )
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
        candidate = make_spec(
            lang_cls=lang_cls,
            heterogeneous_strategy=strategy,
        )
        behavior = candidate.heterogeneous_behavior
        if behavior.widens_nested_maps_by_wrapping_scalars:
            return candidate
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
        if lang_cls.variant_metadata.nested_map_widening
        is NestedMapWideningVariant.DEFAULT
        for variant in (
            Variant(
                name=f"{lang_cls.__name__}_nested_map_widening",
                spec=make_spec(lang_cls=lang_cls),
                lang_cls=lang_cls,
                collection_layout=literalizer.CollectionLayout.COMPACT,
            ),
            Variant(
                name=f"{lang_cls.__name__}_nested_map_widening_multiline",
                spec=make_spec(lang_cls=lang_cls),
                lang_cls=lang_cls,
                collection_layout=literalizer.CollectionLayout.MULTILINE,
            ),
        )
    ]
    for lang_cls in sorted_languages():
        if (
            lang_cls.variant_metadata.nested_map_widening
            is NestedMapWideningVariant.UNIFORM_KEYS
        ):
            continue
        spec = _nested_map_scalar_wrapping_spec(lang_cls=lang_cls)
        if spec is None:
            continue
        variants.extend(
            [
                Variant(
                    name=f"{lang_cls.__name__}_nested_map_widening",
                    spec=spec,
                    lang_cls=lang_cls,
                    collection_layout=literalizer.CollectionLayout.COMPACT,
                ),
                Variant(
                    name=(
                        f"{lang_cls.__name__}_nested_map_widening_multiline"
                    ),
                    spec=spec,
                    lang_cls=lang_cls,
                    collection_layout=(literalizer.CollectionLayout.MULTILINE),
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
        if (
            lang_cls.variant_metadata.nested_map_widening
            is not NestedMapWideningVariant.UNIFORM_KEYS
        ):
            continue
        spec = _nested_map_scalar_wrapping_spec(lang_cls=lang_cls)
        assert spec is not None  # noqa: S101
        variants.extend(
            (
                Variant(
                    name=f"{lang_cls.__name__}_nested_map_widening",
                    spec=spec,
                    lang_cls=lang_cls,
                    collection_layout=literalizer.CollectionLayout.COMPACT,
                ),
                Variant(
                    name=(
                        f"{lang_cls.__name__}_nested_map_widening_multiline"
                    ),
                    spec=spec,
                    lang_cls=lang_cls,
                    collection_layout=literalizer.CollectionLayout.MULTILINE,
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
                Variant(
                    name=f"{lang_cls.__name__}_empty_map_narrowing",
                    spec=spec,
                    lang_cls=lang_cls,
                    collection_layout=literalizer.CollectionLayout.COMPACT,
                ),
                Variant(
                    name=f"{lang_cls.__name__}_empty_map_narrowing_multiline",
                    spec=spec,
                    lang_cls=lang_cls,
                    collection_layout=literalizer.CollectionLayout.MULTILINE,
                ),
            )
        )
    return variants


@beartype
def build_language_version_cross_dict_type_variants() -> Iterable[Variant]:
    """Build old-version x non-default dict-value-type variants.

    Exercises the False branch of the ``_any_types`` intersection check
    in the PY38 type-hint preamble builder, where the dict value type is
    not ``Any`` so ``from typing import Any`` is not emitted.
    """
    variants: list[Variant] = []
    for lang_cls in sorted_languages():
        old_version = next(
            (
                version
                for version in lang_cls.VersionFormats
                if version.name == "PY38"
            ),
            None,
        )
        dict_value_type = lang_cls.non_default_kwargs.get(
            "default_dict_value_type"
        )
        if old_version is None or dict_value_type is None:
            continue
        variants.append(
            Variant(
                name=(
                    f"{lang_cls.__name__}_version_{old_version.name.lower()}"
                    f"_default_dict_value_type_{dict_value_type}"
                ),
                spec=make_spec(
                    lang_cls=lang_cls,
                    language_version=old_version,
                    default_dict_value_type=dict_value_type,
                ),
                lang_cls=lang_cls,
                collection_layout=literalizer.CollectionLayout.COMPACT,
            )
        )
    return variants


@beartype
def build_modifier_variant_cases() -> list[VariantCase]:
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
    case_dirs = (
        "scalar_int",
        "simple_dict",
        "set",
        "empty_set",
        "scalar_date",
        "scalar_datetime",
        "scalar_time",
    )
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
            variant = Variant(
                name=f"{lang_cls.__name__}_modifiers_{mod_name}",
                spec=make_spec(lang_cls=lang_cls),
                lang_cls=lang_cls,
                collection_layout=literalizer.CollectionLayout.COMPACT,
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
                )
                for case_dir_name in case_dirs
            )

    # Some modifiers require a non-default sequence representation for typed
    # declarations.  The compatibility mapping belongs to the language; this
    # matrix supplies the sequence inputs that exercise it.
    sequence_cases = (
        ("mixed_numbers", "mixed_number_list"),
        ("array", "simple_sequence"),
    )
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
            for suffix, case_dir_name in sequence_cases:
                variant = Variant(
                    name=(
                        f"{lang_cls.__name__}_modifiers_"
                        f"{modifier_name.lower()}_{suffix}"
                    ),
                    spec=make_spec(
                        lang_cls=lang_cls,
                        sequence_format=sequence_format,
                    ),
                    lang_cls=lang_cls,
                    collection_layout=literalizer.CollectionLayout.COMPACT,
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
                    )
                )

    return cases
