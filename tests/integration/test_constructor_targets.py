"""Golden-file coverage for constructor call targets."""

import enum
from dataclasses import dataclass, field
from pathlib import Path

import pytest
from beartype import beartype
from pytest_regressions.file_regression import FileRegressionFixture

import literalizer
from literalizer import InputFormat, Language, NewVariable, literalize_call
from literalizer.exceptions import IncompatibleFormatsError

from .language_specs import make_golden_path, make_spec, sorted_languages

_CONSTRUCTOR_NAME = "Playlist"
_GOLDEN_DIR = Path(__file__).parent / "constructor_targets"
_MIN_VARIANT_CALL_STYLES = 2


def _empty_spec_kwargs() -> dict[str, object]:
    """Return empty language constructor kwargs."""
    return {}


@dataclass(frozen=True)
class _ConstructorBindingCase:
    """A constructor call-binding golden-file variant."""

    name: str
    lang_cls: literalizer.LanguageCls
    spec_kwargs: dict[str, object] = field(default_factory=_empty_spec_kwargs)
    variable_form: literalizer.VariableForm = field(
        default_factory=lambda: NewVariable(name="p", modifiers=frozenset()),
    )


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
            file_regression.check(
                contents=(
                    spec.format_constructor_target(_CONSTRUCTOR_NAME) + "\n"
                ),
                encoding="utf-8",
                extension=".txt",
                newline="",
                fullpath=_golden_path(
                    name=f"{lang_cls.__name__}_constructor_target",
                    lang_cls=lang_cls,
                    version=version_format,
                ),
            )


@beartype
def _default_binding_languages() -> list[literalizer.LanguageCls]:
    """Return languages with supported zero-argument call bindings."""
    languages: list[literalizer.LanguageCls] = []
    for lang_cls in sorted_languages():
        spec = lang_cls()
        if (
            not isinstance(spec.call_style_config, enum.Enum)
            and lang_cls.supports_variable_names
            and lang_cls.supports_zero_parameter_calls
            and lang_cls.call_returns_expression
        ):
            languages.append(lang_cls)
    return languages


@beartype
def _supports_default_constructor_binding(
    spec: literalizer.Language,
) -> bool:
    """Return whether *spec* supports constructor call bindings here."""
    return (
        not isinstance(spec.call_style_config, enum.Enum)
        and spec.__class__.supports_variable_names
        and spec.supports_zero_parameter_calls
        and spec.call_returns_expression
    )


@beartype
def _call_style_binding_cases() -> list[_ConstructorBindingCase]:
    """Return all non-default call-style constructor binding variants."""
    cases: list[_ConstructorBindingCase] = []
    for lang_cls in sorted_languages():
        spec = make_spec(lang_cls=lang_cls)
        call_styles: list[enum.Enum] = list(spec.call_styles)
        has_variant_call_styles = len(call_styles) >= _MIN_VARIANT_CALL_STYLES
        supports_constructor_binding = _supports_default_constructor_binding(
            spec=spec,
        )
        if not has_variant_call_styles or not supports_constructor_binding:
            continue
        default_call_style_config = spec.call_style_config
        cases.extend(
            _ConstructorBindingCase(
                name=(
                    f"{lang_cls.__name__}_constructor_call_"
                    f"{call_style.name.lower()}"
                ),
                lang_cls=lang_cls,
                spec_kwargs={"call_style": call_style},
            )
            for call_style in call_styles
            if call_style.value != default_call_style_config
        )
    return cases


@beartype
def _modifier_binding_cases() -> list[_ConstructorBindingCase]:
    """Return constructor binding variants for every language modifier."""
    cases: list[_ConstructorBindingCase] = []
    for lang_cls in sorted_languages():
        spec = make_spec(lang_cls=lang_cls)
        if len(
            spec.modifiers
        ) == 0 or not _supports_default_constructor_binding(spec=spec):
            continue
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
                variable_form=NewVariable(name="p", modifiers=modifiers),
            )
            for modifier_name, modifiers in entries
        )
    return cases


@pytest.mark.parametrize(
    argnames="lang_cls",
    argvalues=_default_binding_languages(),
    ids=[lang_cls.__name__ for lang_cls in _default_binding_languages()],
)
def test_constructor_default_call_binding_golden_file(
    *,
    lang_cls: literalizer.LanguageCls,
    file_regression: FileRegressionFixture,
    subtests: pytest.Subtests,
) -> None:
    """Default constructor call bindings are golden-checked per
    language.
    """
    for version_format in lang_cls.VersionFormats:
        with subtests.test(version=version_format.name):
            spec = make_spec(
                lang_cls=lang_cls,
                language_version=version_format,
            )
            result = literalize_call(
                source="[[]]",
                input_format=InputFormat.JSON,
                language=spec,
                target_function=spec.format_constructor_target(
                    _CONSTRUCTOR_NAME,
                ),
                parameter_names=[],
                variable_form=NewVariable(name="p", modifiers=frozenset()),
            )
            file_regression.check(
                contents=result.code + "\n",
                encoding="utf-8",
                extension=".txt",
                newline="",
                fullpath=_golden_path(
                    name=f"{lang_cls.__name__}_constructor_call",
                    lang_cls=lang_cls,
                    version=version_format,
                ),
            )


def _variant_golden_path(
    *,
    name: str,
    lang_cls: literalizer.LanguageCls,
    version: enum.Enum,
) -> Path:
    """Return a checked-in path for a constructor-call variant."""
    return _golden_path(
        name=name,
        lang_cls=lang_cls,
        version=version,
    )


def _check_constructor_binding(
    *,
    file_regression: FileRegressionFixture,
    name: str,
    lang_cls: literalizer.LanguageCls,
    language: Language,
    variable_form: literalizer.VariableForm,
) -> None:
    """Check a constructor call-binding variant against its golden
    file.
    """
    result = literalize_call(
        source="[[]]",
        input_format=InputFormat.JSON,
        language=language,
        target_function=language.format_constructor_target(
            _CONSTRUCTOR_NAME,
        ),
        parameter_names=[],
        variable_form=variable_form,
    )
    file_regression.check(
        contents=result.code + "\n",
        encoding="utf-8",
        extension=".txt",
        newline="",
        fullpath=_variant_golden_path(
            name=name,
            lang_cls=lang_cls,
            version=language.language_version,
        ),
    )


@pytest.mark.parametrize(
    argnames="case",
    argvalues=_call_style_binding_cases(),
    ids=[case.name for case in _call_style_binding_cases()],
)
def test_constructor_call_style_binding_golden_file(
    *,
    case: _ConstructorBindingCase,
    file_regression: FileRegressionFixture,
    subtests: pytest.Subtests,
) -> None:
    """Constructor call-style variants are golden-checked per language."""
    for version_format in case.lang_cls.VersionFormats:
        with subtests.test(version=version_format.name):
            _check_constructor_binding(
                file_regression=file_regression,
                name=case.name,
                lang_cls=case.lang_cls,
                language=make_spec(
                    lang_cls=case.lang_cls,
                    language_version=version_format,
                    **case.spec_kwargs,
                ),
                variable_form=case.variable_form,
            )


@pytest.mark.parametrize(
    argnames="case",
    argvalues=_modifier_binding_cases(),
    ids=[case.name for case in _modifier_binding_cases()],
)
def test_constructor_modifier_binding_golden_file(
    *,
    case: _ConstructorBindingCase,
    file_regression: FileRegressionFixture,
    subtests: pytest.Subtests,
) -> None:
    """Constructor modifier variants are golden-checked per language."""
    for version_format in case.lang_cls.VersionFormats:
        with subtests.test(version=version_format.name):
            try:
                _check_constructor_binding(
                    file_regression=file_regression,
                    name=case.name,
                    lang_cls=case.lang_cls,
                    language=make_spec(
                        lang_cls=case.lang_cls,
                        language_version=version_format,
                        **case.spec_kwargs,
                    ),
                    variable_form=case.variable_form,
                )
            except IncompatibleFormatsError:
                _variant_golden_path(
                    name=case.name,
                    lang_cls=case.lang_cls,
                    version=version_format,
                ).unlink(missing_ok=True)
                pytest.skip(
                    "Modifier combination cannot represent this "
                    "constructor call binding",
                )
