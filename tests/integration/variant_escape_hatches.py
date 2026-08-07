"""Variant axes whose expansion is written as typed Python.

``axes.toml`` declares how every other axis expands.  An axis lands here
only when no plan can describe it, and the comment above
:data:`_ESCAPE_HATCH_BUILDERS` states the reason for each one.

This module holds the builders rather than :mod:`variant_cases` so that
:mod:`variant_axis_names` can derive the set of known axis names from
the two places axes are actually registered.
"""

from collections.abc import Callable, Iterable

from beartype import beartype

import literalizer

from .language_specs import make_spec, sorted_languages
from .variant_types import Variant, compact_variant


@beartype
def build_typed_dict_null_filtering_variants() -> Iterable[Variant]:
    """Build null-filtering variants for typed-dict languages."""
    variants: list[Variant] = []
    for lang_cls in sorted_languages():
        if not lang_cls.supports_typed_dict_open:
            continue
        variant_cls = type(
            f"_{lang_cls.__name__}SkipNullDictValues",
            (lang_cls,),
            {"skip_null_dict_values": True},
        )
        assert isinstance(variant_cls, literalizer.LanguageCls)  # noqa: S101
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
# synthesized here, which no plan builds because nothing else needs one.
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
