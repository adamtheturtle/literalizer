"""Validation tests for ``NewVariable`` names."""

import pytest

from literalizer import (
    InputFormat,
    LanguageCls,
    NewVariable,
    literalize,
    literalize_call,
)
from literalizer.exceptions import (
    InvalidNewVariableNameError,
    ReservedVariableNameError,
)
from literalizer.languages import (
    ALL_LANGUAGES,
    Ada,
    C,
    Cobol,
    Cpp,
    Crystal,
    D,
    Elixir,
    Erlang,
    Fortran,
    Gleam,
    Go,
    Groovy,
    Haskell,
    Haxe,
    Java,
    JavaScript,
    Rust,
    Scala,
    Sml,
    Swift,
    TypeScript,
    V,
    VisualBasic,
    Zig,
)


@pytest.mark.parametrize(
    argnames="language_cls",
    argvalues=[
        C,
        Cpp,
        Crystal,
        D,
        Elixir,
        Erlang,
        Fortran,
        Gleam,
        Go,
        Groovy,
        Haskell,
        Haxe,
        Java,
        JavaScript,
        Rust,
        Scala,
        Sml,
        Swift,
        TypeScript,
        V,
        Zig,
    ],
    ids=lambda language_cls: language_cls.__name__,
)
def test_hyphenated_new_variable_name_raises(
    language_cls: LanguageCls,
) -> None:
    """Declaration names are rejected rather than repaired."""
    with pytest.raises(expected_exception=InvalidNewVariableNameError):
        literalize(
            source="1",
            input_format=InputFormat.JSON,
            language=language_cls(),
            variable_form=NewVariable(name="a-b", modifiers=frozenset()),
            wrap_in_file=True,
        )


@pytest.mark.parametrize(
    argnames=("language_cls", "name"),
    argvalues=[
        (Crystal, "Value"),
        (Elixir, "Value"),
        (Fortran, "_value"),
        (Gleam, "Value"),
        (Haskell, "Value"),
        (Sml, "Value"),
    ],
    ids=(
        "crystal-uppercase",
        "elixir-uppercase",
        "fortran-underscore",
        "gleam-uppercase",
        "haskell-uppercase",
        "sml-uppercase",
    ),
)
def test_language_specific_new_variable_syntax_raises(
    language_cls: LanguageCls,
    name: str,
) -> None:
    """Target-language grammar restrictions are validated before rendering."""
    with pytest.raises(expected_exception=InvalidNewVariableNameError):
        literalize(
            source="1",
            input_format=InputFormat.JSON,
            language=language_cls(),
            variable_form=NewVariable(name=name, modifiers=frozenset()),
            wrap_in_file=True,
        )


@pytest.mark.parametrize(
    argnames=("language_cls", "language_name", "reserved_name"),
    argvalues=[
        (JavaScript, "JavaScript", "class"),
        (Sml, "Sml", "op"),
        (Sml, "Sml", "val"),
        (Swift, "Swift", "class"),
        (TypeScript, "TypeScript", "class"),
        (TypeScript, "TypeScript", "await"),
        (Go, "Go", "var"),
        (Go, "Go", "type"),
        (V, "V", "type"),
        (Zig, "Zig", "error"),
    ],
    ids=(
        "javascript-class",
        "sml-op",
        "sml-val",
        "swift-class",
        "typescript-class",
        "typescript-await",
        "go-var",
        "go-type",
        "v-type",
        "zig-error",
    ),
)
def test_reserved_new_variable_name_raises(
    language_cls: LanguageCls,
    language_name: str,
    reserved_name: str,
) -> None:
    """Reserved names are rejected instead of silently being rewritten."""
    with pytest.raises(
        expected_exception=ReservedVariableNameError,
        match=rf"^{language_name} cannot use NewVariable name "
        rf"'{reserved_name}': "
        r"it is a reserved identifier$",
    ):
        literalize(
            source="1",
            input_format=InputFormat.JSON,
            language=language_cls(),
            variable_form=NewVariable(
                name=reserved_name,
                modifiers=frozenset(),
            ),
            wrap_in_file=True,
        )


@pytest.mark.parametrize(
    argnames="language_cls",
    argvalues=[JavaScript, TypeScript],
    ids=("javascript", "typescript"),
)
def test_ecmascript_reserved_property_call_remains_valid(
    language_cls: LanguageCls,
) -> None:
    """Reserved variable names do not block valid property calls."""
    result = literalize_call(
        source="[1]",
        input_format=InputFormat.JSON,
        language=language_cls(),
        target_function="foo.class",
        parameter_names=["value"],
    )

    assert result.code


@pytest.mark.parametrize(
    argnames=("language_cls", "reserved_name"),
    argvalues=[
        (Ada, "IF"),
        (Cobol, "PROGRAM"),
        (Fortran, "Module"),
        (VisualBasic, "AddHandler"),
    ],
    ids=(
        "ada-if",
        "cobol-program",
        "fortran-module",
        "visual-basic-add-handler",
    ),
)
def test_case_insensitive_reserved_names_raise(
    language_cls: LanguageCls,
    reserved_name: str,
) -> None:
    """Case-insensitive languages reject differently-cased keywords."""
    with pytest.raises(expected_exception=ReservedVariableNameError):
        literalize(
            source="1",
            input_format=InputFormat.JSON,
            language=language_cls(),
            variable_form=NewVariable(
                name=reserved_name,
                modifiers=frozenset(),
            ),
            wrap_in_file=True,
        )


def test_erlang_lowercase_keyword_is_valid_variable_name() -> None:
    """Erlang variables capitalize names, so lowercase keywords are
    valid.
    """
    result = literalize(
        source="1",
        input_format=InputFormat.JSON,
        language=Erlang(),
        variable_form=NewVariable(name="if", modifiers=frozenset()),
        wrap_in_file=True,
    )

    assert "If =" in result.code


_LANGUAGES_WITH_RESERVED_NEW_VARIABLE_NAMES = tuple(
    language_cls
    for language_cls in sorted(ALL_LANGUAGES, key=lambda cls: cls.__name__)
    if language_cls.reserved_variable_identifiers
)


@pytest.mark.parametrize(
    argnames="language_cls",
    argvalues=_LANGUAGES_WITH_RESERVED_NEW_VARIABLE_NAMES,
    ids=lambda language_cls: language_cls.__name__,
)
def test_all_declared_reserved_names_raise(
    language_cls: LanguageCls,
) -> None:
    """Every language-specific reserved declaration name is rejected."""
    for reserved_name in sorted(language_cls.reserved_variable_identifiers):
        with pytest.raises(expected_exception=ReservedVariableNameError):
            literalize(
                source="1",
                input_format=InputFormat.JSON,
                language=language_cls(),
                variable_form=NewVariable(
                    name=reserved_name,
                    modifiers=frozenset(),
                ),
                wrap_in_file=True,
            )
