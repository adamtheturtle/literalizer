"""``literalize_call`` golden-file cases driven by language variants.

Covers call inputs that need a non-default language spec, such as
inputs that a default heterogeneous strategy rejects or calls rendered
with a non-default statement terminator.  Sibling to :mod:`call_cases`.
"""

import dataclasses
import functools
from collections.abc import Callable, Iterable

from beartype import beartype

from literalizer._language import no_data_preamble

from .call_cases import CALL_CASE_CONFIGS, CallCaseConfig
from .language_specs import make_spec, sorted_languages
from .variant_cases import (
    Variant,
    build_heterogeneous_value_name_variants,
    build_heterogeneous_value_variant_name_variants,
)


@dataclasses.dataclass(frozen=True)
class CallVariantCase:
    """A ``literalize_call`` golden-file case run with a non-default
    language spec (e.g. Rust's ``TAGGED_ENUM`` strategy).
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
            )
            for statement_terminator_style in spec.statement_terminator_styles
            if statement_terminator_style
            is not default_statement_terminator_style
        )
    return variants


@functools.cache
@beartype
def _build_call_arg_heterogeneous_value_variant_name_variants() -> list[
    Variant
]:
    """Variant-name variants whose call rendering declares the variant
    type.

    Filters
    :func:`build_heterogeneous_value_variant_name_variants` to languages
    whose ``call_data_dependent_preamble`` actually emits the wrapping
    type's declaration in the call context.  Languages that share the
    no-op default produce a call golden referring to an undefined
    variant type, so they are excluded until their call path emits the
    declaration.
    """
    return [
        variant
        for variant in build_heterogeneous_value_variant_name_variants()
        if variant.spec.call_data_dependent_preamble is not no_data_preamble
    ]


CALL_VARIANT_SOURCES: list[tuple[str, Callable[[], Iterable[Variant]]]] = [
    ("call_scalar_args", build_statement_terminator_style_call_variants),
    ("call_mixed_type_dicts", build_heterogeneous_value_name_variants),
    (
        "call_mixed_type_dicts",
        _build_call_arg_heterogeneous_value_variant_name_variants,
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
            for cfg in CALL_CASE_CONFIGS
            if cfg.case_dir_name == case_dir_name
        )
        cases.extend(
            CallVariantCase(config=config, variant=variant)
            for variant in builder()
        )
    return cases
