"""Language-level constructor bindings before fixture ownership."""

import dataclasses
import enum
from collections.abc import Mapping

from beartype import beartype

import literalizer
from literalizer import NewVariable
from literalizer._enums import enum_payload
from literalizer.exceptions import IncompatibleFormatsError

from .golden_checks import NO_SKIPS, SkipPolicy, SkipReason
from .language_specs import make_spec, sorted_languages

_MIN_VARIANT_CALL_STYLES = 2
# A declared modifier may reject a constructor binding; other errors fail.
_MODIFIER_SKIPS = SkipPolicy(
    reasons=(
        SkipReason(
            error=IncompatibleFormatsError,
            reason=(
                "modifier combination cannot represent this constructor "
                "call binding"
            ),
            unlink=True,
        ),
    ),
    suffix="",
)


@dataclasses.dataclass(frozen=True, kw_only=True)
class ConstructorBindingSpec:
    """A constructor binding configuration before selecting its owner."""

    name: str
    lang_cls: literalizer.LanguageCls
    spec_overrides: Mapping[str, object]
    variable_form: literalizer.VariableForm
    skip: SkipPolicy


@beartype
def _supports_default_constructor_binding(
    spec: literalizer.Language,
) -> bool:
    """Return whether *spec* supports constructor call bindings here."""
    return (
        not isinstance(spec.call_style_config, enum.Enum)
        and spec.supports_variable_names
        and spec.supports_zero_parameter_calls
        and spec.call_returns_expression
    )


@beartype
def _binding_languages() -> list[literalizer.LanguageCls]:
    """Return languages with supported zero-argument call bindings."""
    return [
        lang_cls
        for lang_cls in sorted_languages()
        if _supports_default_constructor_binding(
            spec=make_spec(lang_cls=lang_cls),
        )
    ]


@beartype
def _default_binding_cases(
    *, languages: list[literalizer.LanguageCls]
) -> list[ConstructorBindingSpec]:
    """Return the plain constructor binding for each language."""
    return [
        ConstructorBindingSpec(
            name=f"{lang_cls.__name__}_constructor_call",
            lang_cls=lang_cls,
            spec_overrides={},
            variable_form=NewVariable(name="p", modifiers=frozenset()),
            skip=NO_SKIPS,
        )
        for lang_cls in languages
    ]


@beartype
def _call_style_binding_cases(
    *, languages: list[literalizer.LanguageCls]
) -> list[ConstructorBindingSpec]:
    """Return all non-default call-style constructor binding variants."""
    cases: list[ConstructorBindingSpec] = []
    for lang_cls in languages:
        spec = make_spec(lang_cls=lang_cls)
        call_styles: list[enum.Enum] = list(spec.call_styles)
        if len(call_styles) < _MIN_VARIANT_CALL_STYLES:
            continue
        default_call_style_config = spec.call_style_config
        cases.extend(
            ConstructorBindingSpec(
                name=(
                    f"{lang_cls.__name__}_constructor_call_"
                    f"{call_style.name.lower()}"
                ),
                lang_cls=lang_cls,
                spec_overrides={"call_style": call_style},
                variable_form=NewVariable(name="p", modifiers=frozenset()),
                skip=NO_SKIPS,
            )
            for call_style in call_styles
            if enum_payload(member=call_style, payload_type=object)
            != default_call_style_config
        )
    return cases


@beartype
def _modifier_binding_cases(
    *, languages: list[literalizer.LanguageCls]
) -> list[ConstructorBindingSpec]:
    """Return constructor binding variants for every language modifier."""
    cases: list[ConstructorBindingSpec] = []
    for lang_cls in languages:
        spec = make_spec(lang_cls=lang_cls)
        entries: list[tuple[str, frozenset[enum.Enum]]] = [
            (member.name.lower(), frozenset({member}))
            for member in spec.modifiers
        ]
        entries.extend(
            (combo.name, combo.modifiers)
            for combo in lang_cls.modifier_combinations
        )
        cases.extend(
            ConstructorBindingSpec(
                name=f"{lang_cls.__name__}_constructor_call_{modifier_name}",
                lang_cls=lang_cls,
                spec_overrides={},
                variable_form=NewVariable(name="p", modifiers=modifiers),
                skip=_MODIFIER_SKIPS,
            )
            for modifier_name, modifiers in entries
        )
    return cases


@beartype
def constructor_binding_specs() -> list[ConstructorBindingSpec]:
    """Collect default, call-style, and modifier variants in order."""
    languages = _binding_languages()
    return [
        *_default_binding_cases(languages=languages),
        *_call_style_binding_cases(languages=languages),
        *_modifier_binding_cases(languages=languages),
    ]
