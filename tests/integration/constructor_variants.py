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
from .language_specs import make_spec, modifier_entries, sorted_languages

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
def constructor_binding_specs() -> list[ConstructorBindingSpec]:
    """Collect default, call-style, and modifier variants in order."""
    languages = [
        lang_cls
        for lang_cls in sorted_languages()
        if _supports_default_constructor_binding(
            spec=make_spec(lang_cls=lang_cls),
        )
    ]
    cases = [
        ConstructorBindingSpec(
            name=f"{lang_cls.__name__}_constructor_call",
            lang_cls=lang_cls,
            spec_overrides={},
            variable_form=NewVariable(name="p", modifiers=frozenset()),
            skip=NO_SKIPS,
        )
        for lang_cls in languages
    ]
    for lang_cls in languages:
        spec = make_spec(lang_cls=lang_cls)
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
            for call_style in spec.call_styles
            if enum_payload(member=call_style, payload_type=object)
            != default_call_style_config
        )
    for lang_cls in languages:
        spec = make_spec(lang_cls=lang_cls)
        cases.extend(
            ConstructorBindingSpec(
                name=f"{lang_cls.__name__}_constructor_call_{modifier_name}",
                lang_cls=lang_cls,
                spec_overrides={},
                variable_form=NewVariable(name="p", modifiers=modifiers),
                skip=_MODIFIER_SKIPS,
            )
            for modifier_name, modifiers in modifier_entries(
                lang_cls=lang_cls, spec=spec
            )
        )
    return cases
