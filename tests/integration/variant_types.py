"""Shared data types for integration-test language variants."""

import dataclasses
from collections.abc import Mapping

from beartype import beartype

import literalizer
from literalizer._types import ValueInput


@beartype
def wrap_variable_form() -> literalizer.NewVariable:
    """Return the canonical new-variable form for variant tests.

    Callers that pass the result to ``literalize`` should treat
    :class:`~literalizer.exceptions.VariableNameNotSupportedError` as
    the signal that the language cannot wrap output in a named variable,
    rather than pre-filtering on ``supports_variable_names``.
    """
    return literalizer.NewVariable(name="my_data", modifiers=frozenset())


@dataclasses.dataclass(frozen=True, kw_only=True)
class Variant:
    """A formatting variant for a language (date, sequence, set, etc.)."""

    name: str
    spec: literalizer.Language
    lang_cls: literalizer.LanguageCls
    collection_layout: literalizer.CollectionLayout
    fixture_prefix: str
    record_null_substitutions: Mapping[str, ValueInput] | None


@beartype
def compact_variant(
    *,
    name: str,
    spec: literalizer.Language,
    lang_cls: literalizer.LanguageCls,
) -> Variant:
    """Return a variant carrying the shared default render context.

    Nearly every axis renders compactly, without a fixture preamble and
    without record null substitutions; the handful that vary one of
    those build a :class:`Variant` naming all three instead of
    restating the defaults at every construction site.
    """
    return Variant(
        name=name,
        spec=spec,
        lang_cls=lang_cls,
        collection_layout=literalizer.CollectionLayout.COMPACT,
        fixture_prefix="",
        record_null_substitutions=None,
    )


@dataclasses.dataclass(frozen=True)
class VariantCase:
    """A format-variant golden-file test case."""

    variant_name: str
    variant: Variant
    case_dir_name: str
    variable_form: literalizer.VariableForm
    pre_indent_level: int
