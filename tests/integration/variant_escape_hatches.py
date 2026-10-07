"""Variant axes whose expansion is written as typed Python.

``axes.toml`` declares how every other axis expands.  An axis lands here
only when no plan can describe it, and the comment above
:data:`_ESCAPE_HATCH_BUILDERS` states the reason for each one.

This module holds the builders rather than :mod:`variant_cases` so that
:mod:`variant_axis_names` can derive the set of known axis names from
the two places axes are actually registered.
"""

from collections.abc import Callable, Iterable
from typing import ClassVar

from beartype import beartype

import literalizer
from literalizer.languages import CSharp, Dart, Go, Kotlin, Scala

from .language_specs import lang_cls_name, make_spec
from .variant_types import Variant, compact_variant


class _CSharpSkipNullDictValues(CSharp):
    """Filter null dictionary values when rendering C#."""

    skip_null_dict_values: ClassVar[bool] = True


class _DartSkipNullDictValues(Dart):
    """Filter null dictionary values when rendering Dart."""

    skip_null_dict_values: ClassVar[bool] = True


class _GoSkipNullDictValues(Go):
    """Filter null dictionary values when rendering Go."""

    skip_null_dict_values: ClassVar[bool] = True


class _KotlinSkipNullDictValues(Kotlin):
    """Filter null dictionary values when rendering Kotlin."""

    skip_null_dict_values: ClassVar[bool] = True


class _ScalaSkipNullDictValues(Scala):
    """Filter null dictionary values when rendering Scala."""

    skip_null_dict_values: ClassVar[bool] = True


# The capability test requires this registry to cover exactly the languages
# with ``supports_typed_dict_open``, including future capability changes.
_TYPED_DICT_NULL_FILTERING_CLASSES: dict[
    literalizer.LanguageCls, literalizer.LanguageCls
] = {
    CSharp: _CSharpSkipNullDictValues,
    Dart: _DartSkipNullDictValues,
    Go: _GoSkipNullDictValues,
    Kotlin: _KotlinSkipNullDictValues,
    Scala: _ScalaSkipNullDictValues,
}


@beartype
def build_typed_dict_null_filtering_variants() -> Iterable[Variant]:
    """Build null-filtering variants for typed-dict languages."""
    variants: list[Variant] = []
    for lang_cls in sorted(
        _TYPED_DICT_NULL_FILTERING_CLASSES, key=lang_cls_name
    ):
        variant_cls = _TYPED_DICT_NULL_FILTERING_CLASSES[lang_cls]
        variants.append(
            compact_variant(
                name=f"{lang_cls.__name__}_skip_null_dict_values",
                spec=make_spec(lang_cls=variant_cls),
                lang_cls=lang_cls,
            )
        )
    return variants


# Axes whose expansion is genuinely irregular, and so is written as a
# typed Python builder instead of a declared plan in ``axes.toml``.
# ``typed_dict_null_filtering`` renders through a language subclass
# declared here, which no plan builds because nothing else needs one.
# A meta-test holds this set to its current membership: new axes belong
# in ``axes.toml``.
_ESCAPE_HATCH_BUILDERS: dict[str, Callable[[], Iterable[Variant]]] = {
    "typed_dict_null_filtering": build_typed_dict_null_filtering_variants,
}

ESCAPE_HATCH_VARIANT_AXES = frozenset(_ESCAPE_HATCH_BUILDERS)


@beartype
def escape_hatch_variants(*, axis_key: str) -> list[Variant]:
    """Return the variants the escape-hatch builder for *axis_key*
    builds.
    """
    return list(_ESCAPE_HATCH_BUILDERS[axis_key]())
