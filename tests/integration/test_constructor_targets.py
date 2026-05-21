"""Golden-file coverage for constructor call targets."""

import enum
from pathlib import Path

import pytest
from beartype import beartype
from pytest_regressions.file_regression import FileRegressionFixture

import literalizer
from literalizer import InputFormat, Language, NewVariable, literalize_call
from literalizer.languages import JavaScript, Rust

from .check_golden import check_golden
from .language_specs import make_golden_path, make_spec, sorted_languages

_CONSTRUCTOR_NAME = "Playlist"
_GOLDEN_DIR = Path(__file__).parent / "constructor_targets"


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
                file_regression=file_regression,
                contents=(
                    spec.format_constructor_target(_CONSTRUCTOR_NAME) + "\n"
                ),
                extension=".txt",
                newline="",
                golden_path=_golden_path(
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
                variable_form=NewVariable(name="p"),
            )
            check_golden(
                file_regression=file_regression,
                contents=result.code + "\n",
                extension=".txt",
                newline="",
                golden_path=_golden_path(
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
    check_golden(
        file_regression=file_regression,
        contents=result.code + "\n",
        extension=".txt",
        newline="",
        golden_path=_variant_golden_path(
            name=name,
            lang_cls=lang_cls,
            version=language.language_version,
        ),
    )


def test_constructor_rust_mutable_call_binding_golden_file(
    file_regression: FileRegressionFixture,
) -> None:
    """Rust mutable constructor binding is golden-checked."""
    _check_constructor_binding(
        file_regression=file_regression,
        name="Rust_constructor_call_mutable",
        lang_cls=Rust,
        language=Rust(),
        variable_form=NewVariable(
            name="p",
            modifiers=frozenset({Rust.modifiers.MUT}),
        ),
    )


def test_constructor_javascript_positional_call_binding_golden_file(
    file_regression: FileRegressionFixture,
) -> None:
    """JavaScript positional constructor binding is golden-checked."""
    _check_constructor_binding(
        file_regression=file_regression,
        name="JavaScript_constructor_call_positional",
        lang_cls=JavaScript,
        language=JavaScript(call_style=JavaScript.call_styles.POSITIONAL),
        variable_form=NewVariable(name="p"),
    )
