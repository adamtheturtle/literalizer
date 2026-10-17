"""Shared discovery and fixture ownership for constructor bindings."""

import dataclasses
import enum
from collections.abc import Mapping
from pathlib import Path

from beartype import beartype

import literalizer
from literalizer import NewVariable
from literalizer.exceptions import IncompatibleFormatsError

from .case_manifests import CaseManifest, load_case_manifests
from .golden_checks import NO_SKIPS, SkipPolicy, SkipReason
from .language_specs import make_golden_path, make_spec, sorted_languages

CASES_DIR = Path(__file__).parent / "cases"
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
class ConstructorBindingCase:
    """A constructor call-binding golden-file variant."""

    name: str
    lang_cls: literalizer.LanguageCls
    spec_overrides: Mapping[str, object]
    variable_form: literalizer.VariableForm
    skip: SkipPolicy
    manifest: CaseManifest | None


@beartype
def constructor_golden_path(
    *, case: ConstructorBindingCase, version: enum.Enum
) -> Path:
    """Locate a compiling fixture or a remaining legacy fragment."""
    parent = Path(__file__).parent / "constructor_targets"
    extension = ".txt"
    if case.manifest is not None:
        parent = case.manifest.case_dir
        extension = case.lang_cls.extension
    return make_golden_path(
        parent=parent,
        name=case.name,
        extension=extension,
        lang_cls=case.lang_cls,
        version=version,
    )


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
def _default_binding_cases() -> list[ConstructorBindingCase]:
    """Return the plain constructor binding for each language."""
    return [
        ConstructorBindingCase(
            name=f"{lang_cls.__name__}_constructor_call",
            lang_cls=lang_cls,
            spec_overrides={},
            variable_form=NewVariable(name="p", modifiers=frozenset()),
            skip=NO_SKIPS,
            manifest=None,
        )
        for lang_cls in _binding_languages()
    ]


@beartype
def _call_style_binding_cases() -> list[ConstructorBindingCase]:
    """Return all non-default call-style constructor binding variants."""
    cases: list[ConstructorBindingCase] = []
    for lang_cls in _binding_languages():
        spec = make_spec(lang_cls=lang_cls)
        call_styles: list[enum.Enum] = list(spec.call_styles)
        if len(call_styles) < _MIN_VARIANT_CALL_STYLES:
            continue
        default_call_style_config = spec.call_style_config
        cases.extend(
            ConstructorBindingCase(
                name=(
                    f"{lang_cls.__name__}_constructor_call_"
                    f"{call_style.name.lower()}"
                ),
                lang_cls=lang_cls,
                spec_overrides={"call_style": call_style},
                variable_form=NewVariable(name="p", modifiers=frozenset()),
                skip=NO_SKIPS,
                manifest=None,
            )
            for call_style in call_styles
            if call_style.value != default_call_style_config
        )
    return cases


@beartype
def _modifier_binding_cases() -> list[ConstructorBindingCase]:
    """Return constructor binding variants for every language modifier."""
    cases: list[ConstructorBindingCase] = []
    for lang_cls in _binding_languages():
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
            ConstructorBindingCase(
                name=f"{lang_cls.__name__}_constructor_call_{modifier_name}",
                lang_cls=lang_cls,
                spec_overrides={},
                variable_form=NewVariable(name="p", modifiers=modifiers),
                skip=_MODIFIER_SKIPS,
                manifest=None,
            )
            for modifier_name, modifiers in entries
        )
    return cases


@beartype
def constructor_binding_cases() -> list[ConstructorBindingCase]:
    """Return every declared constructor call-binding variant."""
    manifests = [
        manifest
        for manifest in load_case_manifests(cases_dir=CASES_DIR)
        if manifest.owner == "constructor-binding"
    ]
    return [
        dataclasses.replace(
            case,
            manifest=next(
                (
                    manifest
                    for manifest in manifests
                    if manifest.selection.admits_language(
                        lang_cls=case.lang_cls
                    )
                ),
                None,
            ),
        )
        for case in [
            *_default_binding_cases(),
            *_call_style_binding_cases(),
            *_modifier_binding_cases(),
        ]
    ]
