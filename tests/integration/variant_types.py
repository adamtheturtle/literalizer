"""Shared data types for integration-test language variants."""

import dataclasses
import enum

from beartype import beartype

import literalizer


@beartype
def wrap_variable_form() -> literalizer.NewVariable:
    """Return the canonical new-variable form for variant tests.

    Callers that pass the result to ``literalize`` should treat
    :class:`~literalizer.exceptions.VariableNameNotSupportedError` as
    the signal that the language cannot wrap output in a named variable,
    rather than pre-filtering on ``supports_variable_names``.
    """
    return literalizer.NewVariable(name="my_data", modifiers=frozenset())


@beartype
def enum_member_by_name(
    *,
    enum_cls: type[enum.Enum],
    name: str,
) -> enum.Enum:
    """Return the enum member in *enum_cls* whose ``.name`` matches."""
    for member in enum_cls:
        if member.name == name:
            return member
    msg = f"{enum_cls.__name__} has no member named {name!r}"
    raise ValueError(msg)


@dataclasses.dataclass(frozen=True)
class Variant:
    """A formatting variant for a language (date, sequence, set, etc.)."""

    name: str
    spec: literalizer.Language
    lang_cls: literalizer.LanguageCls
    collection_layout: literalizer.CollectionLayout


@dataclasses.dataclass(frozen=True)
class VariantCase:
    """A format-variant golden-file test case."""

    variant_name: str
    variant: Variant
    case_dir_name: str
    variable_form: literalizer.VariableForm


@dataclasses.dataclass(frozen=True, kw_only=True)
class CaseInput:
    """An input case directory plus a variant-name suffix."""

    case_dir_name: str
    suffix: str
