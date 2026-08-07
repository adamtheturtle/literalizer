"""Golden-file coverage for constructor call targets.

Two things are checked here: how each language spells a constructor as
a call target, and what binding that call to a variable looks like.
The bindings vary by call style and by variable modifier, so they are
declared as cases and driven through the one runner below rather than
written out a test body at a time.
"""

import dataclasses
import enum
from collections.abc import Mapping
from pathlib import Path

import pytest
from beartype import beartype
from pytest_regressions.file_regression import FileRegressionFixture

import literalizer
from literalizer import InputFormat, NewVariable, literalize_call
from literalizer.exceptions import IncompatibleFormatsError

from .golden_checks import (
    NO_SKIPS,
    SkipPolicy,
    SkipReason,
    check_golden,
    skip_for_error,
)
from .language_specs import make_golden_path, make_spec, sorted_languages

_CONSTRUCTOR_NAME = "Playlist"
_GOLDEN_DIR = Path(__file__).parent / "constructor_targets"
_MIN_VARIANT_CALL_STYLES = 2

# A modifier a language declares need not be legal on every binding it
# can otherwise produce, so a combination the call rejects skips; every
# other error is a real failure.
_MODIFIER_SKIPS: SkipPolicy = SkipPolicy(
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
class _ConstructorBindingCase:
    """A constructor call-binding golden-file variant."""

    name: str
    lang_cls: literalizer.LanguageCls
    spec_overrides: Mapping[str, object]
    variable_form: literalizer.VariableForm
    skip: SkipPolicy


@beartype
def _golden_path(
    *,
    name: str,
    lang_cls: literalizer.LanguageCls,
    version: enum.Enum,
) -> Path:
    """Return the checked-in golden path for a constructor-target case."""
    return make_golden_path(
        parent=_GOLDEN_DIR,
        name=name,
        extension=".txt",
        lang_cls=lang_cls,
        version=version,
    )


@pytest.mark.parametrize(
    argnames="lang_cls",
    argvalues=sorted_languages(),
    ids=[lang_cls.__name__ for lang_cls in sorted_languages()],
)
def test_constructor_targets_golden_file(
    *,
    lang_cls: literalizer.LanguageCls,
    file_regression: FileRegressionFixture,
    subtests: pytest.Subtests,
) -> None:
    """Every language's constructor target helper is golden-checked."""
    for version_format in lang_cls.VersionFormats:
        with subtests.test(version=version_format.name):
            spec = make_spec(
                lang_cls=lang_cls,
                language_version=version_format,
            )
            check_golden(
                contents=(
                    spec.format_constructor_target(_CONSTRUCTOR_NAME) + "\n"
                ),
                extension=".txt",
                golden_path=_golden_path(
                    name=f"{lang_cls.__name__}_constructor_target",
                    lang_cls=lang_cls,
                    version=version_format,
                ),
                file_regression=file_regression,
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
def _default_binding_cases() -> list[_ConstructorBindingCase]:
    """Return the plain constructor binding for each language."""
    return [
        _ConstructorBindingCase(
            name=f"{lang_cls.__name__}_constructor_call",
            lang_cls=lang_cls,
            spec_overrides={},
            variable_form=NewVariable(name="p", modifiers=frozenset()),
            skip=NO_SKIPS,
        )
        for lang_cls in _binding_languages()
    ]


@beartype
def _call_style_binding_cases() -> list[_ConstructorBindingCase]:
    """Return all non-default call-style constructor binding variants."""
    cases: list[_ConstructorBindingCase] = []
    for lang_cls in _binding_languages():
        spec = make_spec(lang_cls=lang_cls)
        call_styles: list[enum.Enum] = list(spec.call_styles)
        if len(call_styles) < _MIN_VARIANT_CALL_STYLES:
            continue
        default_call_style_config = spec.call_style_config
        cases.extend(
            _ConstructorBindingCase(
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
            if call_style.value != default_call_style_config
        )
    return cases


@beartype
def _modifier_binding_cases() -> list[_ConstructorBindingCase]:
    """Return constructor binding variants for every language modifier."""
    cases: list[_ConstructorBindingCase] = []
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
            _ConstructorBindingCase(
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
def _constructor_binding_cases() -> list[_ConstructorBindingCase]:
    """Return every declared constructor call-binding variant."""
    return [
        *_default_binding_cases(),
        *_call_style_binding_cases(),
        *_modifier_binding_cases(),
    ]


_BINDING_CASES = _constructor_binding_cases()


@pytest.mark.parametrize(
    argnames="case",
    argvalues=_BINDING_CASES,
    ids=[case.name for case in _BINDING_CASES],
)
def test_constructor_binding_golden_file(
    *,
    case: _ConstructorBindingCase,
    file_regression: FileRegressionFixture,
    subtests: pytest.Subtests,
) -> None:
    """Every declared constructor binding matches its golden file."""
    for version_format in case.lang_cls.VersionFormats:
        with subtests.test(version=version_format.name):
            golden_path = _golden_path(
                name=case.name,
                lang_cls=case.lang_cls,
                version=version_format,
            )
            language = make_spec(
                lang_cls=case.lang_cls,
                language_version=version_format,
                **case.spec_overrides,
            )
            try:
                result = literalize_call(
                    source="[[]]",
                    input_format=InputFormat.JSON,
                    language=language,
                    target_function=language.format_constructor_target(
                        _CONSTRUCTOR_NAME,
                    ),
                    parameter_names=[],
                    variable_form=case.variable_form,
                )
            except case.skip.errors as exc:
                skip_for_error(
                    exc=exc,
                    reasons=case.skip.reasons,
                    golden_path=golden_path,
                    prefix=case.lang_cls.__name__,
                    suffix=case.skip.suffix,
                )
            check_golden(
                contents=result.code + "\n",
                extension=".txt",
                golden_path=golden_path,
                file_regression=file_regression,
            )
