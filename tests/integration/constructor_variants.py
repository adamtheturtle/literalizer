"""Language-level constructor bindings before fixture ownership."""

import dataclasses
from collections.abc import Mapping

from beartype import beartype

import literalizer
from literalizer import NewVariable
from literalizer._enums import enum_payload

from .language_specs import (
    make_spec,
    modifier_entries,
    sorted_languages,
    unique_effective_specs,
)


@dataclasses.dataclass(frozen=True, kw_only=True)
class ConstructorBindingSpec:
    """A constructor binding configuration before selecting its owner."""

    name: str
    lang_cls: literalizer.LanguageCls
    spec_overrides: Mapping[str, object]
    variable_form: literalizer.VariableForm

    @property
    def specs(self) -> tuple[literalizer.Language, ...]:
        """Resolve all effective versions of this binding
        configuration.
        """
        return unique_effective_specs(
            specs=(
                make_spec(
                    lang_cls=self.lang_cls,
                    language_version=version,
                    **self.spec_overrides,
                )
                for version in self.lang_cls.VersionFormats
            ),
        )


@beartype
def constructor_binding_specs() -> list[ConstructorBindingSpec]:
    """Collect default, call-style, and modifier variants in order."""
    languages = [
        lang_cls
        for lang_cls in sorted_languages()
        if len(lang_cls.CallStyles) > 0
    ]
    cases = [
        ConstructorBindingSpec(
            name=f"{lang_cls.__name__}_constructor_call",
            lang_cls=lang_cls,
            spec_overrides={},
            variable_form=NewVariable(name="p", modifiers=frozenset()),
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
            )
            for modifier_name, modifiers in modifier_entries(
                lang_cls=lang_cls, spec=spec
            )
        )
    return cases
