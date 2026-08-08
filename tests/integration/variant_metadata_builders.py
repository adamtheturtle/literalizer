"""Builders driven by declared metadata rather than by concrete languages.

The language classes describe supported behaviors and compatibility
rules, and the test-owned language metadata files describe which focused
golden variants a language opts into; this builder translates both into
cases without depending on individual language classes.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from beartype import beartype

import literalizer

from .language_specs import make_spec, sorted_languages
from .variant_types import (
    VariantCase,
    compact_variant,
    enum_member_by_name,
)

if TYPE_CHECKING:
    import enum
    from collections.abc import Mapping

_enum_member_by_name = enum_member_by_name


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
