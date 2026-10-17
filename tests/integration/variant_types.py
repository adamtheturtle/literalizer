"""Shared data types for integration-test language variants."""

import dataclasses
from collections.abc import Mapping

from beartype import beartype

import literalizer
from literalizer import ValueInput


@dataclasses.dataclass(frozen=True, kw_only=True)
class Variant:
    """A formatting variant for a language (date, sequence, set, etc.)."""

    name: str
    spec: literalizer.Language
    lang_cls: literalizer.LanguageCls
    collection_layout: literalizer.CollectionLayout
    extra_preamble: tuple[str, ...]
    initialize_variable: bool
    record_null_substitutions: Mapping[str, ValueInput] | None
    wrap_in_file: bool


@beartype
def compact_variant(
    *,
    name: str,
    spec: literalizer.Language,
    lang_cls: literalizer.LanguageCls,
) -> Variant:
    """Return a variant carrying the shared default render context.

    Nearly every axis renders compactly, without extra preamble entries and
    without record null substitutions; the handful that vary one of
    those build a :class:`Variant` naming all three instead of
    restating the defaults at every construction site.
    """
    return Variant(
        name=name,
        spec=spec,
        lang_cls=lang_cls,
        collection_layout=literalizer.CollectionLayout.COMPACT,
        extra_preamble=(),
        initialize_variable=False,
        record_null_substitutions=None,
        wrap_in_file=True,
    )


@dataclasses.dataclass(frozen=True)
class VariantCase:
    """A format-variant golden-file test case."""

    variant_name: str
    variant: Variant
    case_dir_name: str
    variable_form: literalizer.VariableForm
    pre_indent_level: int

    @property
    def extension(self) -> str:
        """Keep intentionally indented fragments out of compiler
        inputs.
        """
        if self.pre_indent_level > 0 and not self.variant.wrap_in_file:
            return ".txt"
        return self.variant.spec.extension
