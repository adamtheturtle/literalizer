"""``literalize_call`` golden-file cases driven by language variants.

Covers call inputs that need a non-default language spec, such as
inputs that a default heterogeneous strategy rejects or calls rendered
with a non-default statement terminator.  Sibling to :mod:`call_cases`.
"""

import dataclasses
import functools
from collections.abc import Callable, Iterable

from beartype import beartype

import literalizer

from .call_cases import (
    CALL_CASE_CONFIGS,
    CALL_VARIANT_CASE_CONFIGS,
    CallCaseConfig,
)
from .language_specs import make_spec, sorted_languages
from .variant_cases import (
    Variant,
    build_empty_container_type_hint_variants,
    build_heterogeneous_value_name_variants,
    build_heterogeneous_value_variant_name_variants,
    build_json_type_variants,
)


@dataclasses.dataclass(frozen=True)
class CallVariantCase:
    """A ``literalize_call`` golden-file case run with a non-default
    language spec (e.g. a ``TAGGED_ENUM`` strategy).
    """

    config: CallCaseConfig
    variant: Variant


# Per-case language variants exercised by
# :func:`test_call_variant_golden_file`.  Each entry names a call-case
# directory and pairs it with the variant builders that produce a spec
# capable of representing that case's heterogeneous input — which the
# default spec rejects, causing :func:`test_call_golden_file` to skip.
@functools.cache
@beartype
def build_statement_terminator_style_call_variants() -> list[Variant]:
    """Return variants for every non-default call statement terminator."""
    variants: list[Variant] = []
    for lang_cls in sorted_languages():
        spec = make_spec(lang_cls=lang_cls)
        default_statement_terminator_style = spec.statement_terminator_style
        variants.extend(
            Variant(
                name=(
                    f"{lang_cls.__name__}_statement_terminator_style"
                    f"_{statement_terminator_style.name.lower()}"
                ),
                spec=make_spec(
                    lang_cls=lang_cls,
                    statement_terminator_style=statement_terminator_style,
                ),
                lang_cls=lang_cls,
                collection_layout=literalizer.CollectionLayout.COMPACT,
            )
            for statement_terminator_style in spec.statement_terminator_styles
            if statement_terminator_style
            is not default_statement_terminator_style
        )
    return variants


@functools.cache
@beartype
def build_call_result_json_type_variants() -> list[Variant]:
    """Return JSON-type variants with JSON-aware call-result bindings."""
    return [
        variant
        for variant in build_json_type_variants()
        if variant.lang_cls.supports_json_call_result_binding
    ]


@functools.cache
@beartype
def build_heterogeneous_strategy_call_variants() -> list[Variant]:
    """Return variants for every non-default heterogeneous strategy."""
    variants: list[Variant] = []
    for lang_cls in sorted_languages():
        spec = make_spec(lang_cls=lang_cls)
        default_strategy = spec.heterogeneous_strategy
        variants.extend(
            Variant(
                name=(
                    f"{lang_cls.__name__}_heterogeneous_strategy"
                    f"_{strategy.name.lower()}"
                ),
                spec=make_spec(
                    lang_cls=lang_cls,
                    heterogeneous_strategy=strategy,
                ),
                lang_cls=lang_cls,
                collection_layout=literalizer.CollectionLayout.COMPACT,
            )
            for strategy in spec.heterogeneous_strategies
            if strategy is not default_strategy
        )
    return variants


@functools.cache
@beartype
def build_tagged_enum_call_variants() -> list[Variant]:
    """Return call variants for languages with ``TAGGED_ENUM`` support."""
    variants: list[Variant] = []
    for lang_cls in sorted_languages():
        spec = make_spec(lang_cls=lang_cls)
        tagged_enum = next(
            (
                strategy
                for strategy in spec.heterogeneous_strategies
                if strategy.name == "TAGGED_ENUM"
            ),
            None,
        )
        if tagged_enum is None:
            continue
        variants.append(
            Variant(
                name=(
                    f"{lang_cls.__name__}_heterogeneous_strategy_tagged_enum"
                ),
                spec=make_spec(
                    lang_cls=lang_cls,
                    heterogeneous_strategy=tagged_enum,
                ),
                lang_cls=lang_cls,
                collection_layout=literalizer.CollectionLayout.COMPACT,
            )
        )
    return variants


CALL_VARIANT_SOURCES: list[tuple[str, Callable[[], Iterable[Variant]]]] = [
    (
        "call_empty_container_type_hint",
        build_empty_container_type_hint_variants,
    ),
    ("call_scalar_args", build_statement_terminator_style_call_variants),
    ("call_scalar_args", build_json_type_variants),
    # Bind a call result under each non-default ``json_type`` whose language
    # preserves call expressions while JSON rendering is active.
    ("call_variable_form_new", build_call_result_json_type_variants),
    ("call_mixed_type_dicts", build_heterogeneous_value_name_variants),
    (
        "call_mixed_type_dicts",
        build_heterogeneous_value_variant_name_variants,
    ),
    # Non-default heterogeneous strategies on the cross-call divergent
    # fixtures — covers the Mojo ``VARIANT`` typed-stub fallback (and
    # exercises the corresponding paths in any other language whose
    # non-default strategy can represent these inputs).
    ("call_scalar_args", build_heterogeneous_strategy_call_variants),
    ("call_dotted_method", build_heterogeneous_strategy_call_variants),
    ("call_deep_dotted_method", build_heterogeneous_strategy_call_variants),
    ("call_transform_no_wrapper", build_heterogeneous_strategy_call_variants),
    ("call_dotted_transform_stub", build_heterogeneous_strategy_call_variants),
    ("call_snake_dotted_method", build_heterogeneous_strategy_call_variants),
    (
        "call_deep_dotted_transformed",
        build_heterogeneous_strategy_call_variants,
    ),
    (
        "call_scalar_args_uniform_second_slot",
        build_heterogeneous_strategy_call_variants,
    ),
    (
        "call_scalar_args_with_null",
        build_heterogeneous_strategy_call_variants,
    ),
    (
        "call_sibling_maps",
        build_tagged_enum_call_variants,
    ),
    (
        "call_ref_args_heterogeneous_list",
        build_heterogeneous_strategy_call_variants,
    ),
    (
        "call_ref_args_reused",
        build_heterogeneous_strategy_call_variants,
    ),
    (
        "call_ref_args_trivial_register",
        build_heterogeneous_strategy_call_variants,
    ),
]


@functools.cache
@beartype
def build_call_variant_cases() -> list[CallVariantCase]:
    """Return call-test cases for language variants that accept
    heterogeneous input the default spec rejects.
    """
    cases: list[CallVariantCase] = []
    for case_dir_name, builder in CALL_VARIANT_SOURCES:
        config = next(
            cfg
            for cfg in CALL_CASE_CONFIGS + CALL_VARIANT_CASE_CONFIGS
            if cfg.case_dir_name == case_dir_name
        )
        cases.extend(
            CallVariantCase(config=config, variant=variant)
            for variant in builder()
        )
    return cases
