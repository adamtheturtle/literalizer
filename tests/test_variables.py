"""Tests for variable declaration and assignment in literalizer
converter.
"""

import dataclasses

import pytest

from literalizer import (
    Language,
    literalize_json,
    literalize_yaml,
)
from literalizer.languages import (
    Clojure,
    Cpp,
    CSharp,
    Dart,
    Elixir,
    FSharp,
    Go,
    Haskell,
    Java,
    JavaScript,
    Kotlin,
    Php,
    Python,
    R,
    Ruby,
    Rust,
    Scala,
    Swift,
    TypeScript,
)

CLOJURE = Clojure(
    sequence_format=Clojure.SequenceFormat.VECTOR,
)
CPP = Cpp(
    date_format=Cpp.DateFormat.ISO,
    datetime_format=Cpp.DatetimeFormat.ISO,
    sequence_format=Cpp.SequenceFormat.INITIALIZER_LIST,
)
CSHARP = CSharp(
    date_format=CSharp.DateFormat.ISO,
    datetime_format=CSharp.DatetimeFormat.ISO,
    sequence_format=CSharp.SequenceFormat.ARRAY,
)
DART = Dart(
    date_format=Dart.DateFormat.ISO,
    datetime_format=Dart.DatetimeFormat.ISO,
    sequence_format=Dart.SequenceFormat.LIST,
)
ELIXIR = Elixir(
    sequence_format=Elixir.SequenceFormat.LIST,
)
FSHARP = FSharp(
    sequence_format=FSharp.SequenceFormat.LIST,
)
GO = Go(
    date_format=Go.DateFormat.ISO,
    datetime_format=Go.DatetimeFormat.ISO,
    sequence_format=Go.SequenceFormat.SLICE,
)
HASKELL = Haskell(
    sequence_format=Haskell.SequenceFormat.LIST,
)
JAVA = Java(
    date_format=Java.DateFormat.ISO,
    datetime_format=Java.DatetimeFormat.ISO,
    sequence_format=Java.SequenceFormat.ARRAY,
)
JAVASCRIPT = JavaScript(
    date_format=JavaScript.DateFormat.ISO,
    datetime_format=JavaScript.DatetimeFormat.ISO,
    sequence_format=JavaScript.SequenceFormat.ARRAY,
)
KOTLIN = Kotlin(
    date_format=Kotlin.DateFormat.ISO,
    datetime_format=Kotlin.DatetimeFormat.ISO,
    sequence_format=Kotlin.SequenceFormat.LIST,
)
PHP = Php(
    sequence_format=Php.SequenceFormat.ARRAY,
)
PYTHON = Python(
    date_format=Python.DateFormat.ISO,
    datetime_format=Python.DatetimeFormat.ISO,
    bytes_format=Python.BytesFormat.HEX,
    sequence_format=Python.SequenceFormat.TUPLE,
    set_format=Python.SetFormat.SET,
)
RUBY = Ruby(
    date_format=Ruby.DateFormat.ISO,
    datetime_format=Ruby.DatetimeFormat.ISO,
    sequence_format=Ruby.SequenceFormat.ARRAY,
)
RUST = Rust(
    date_format=Rust.DateFormat.ISO,
    datetime_format=Rust.DatetimeFormat.ISO,
    sequence_format=Rust.SequenceFormat.VEC,
)
SCALA = Scala(
    sequence_format=Scala.SequenceFormat.LIST,
)
SWIFT = Swift(
    sequence_format=Swift.SequenceFormat.ARRAY,
)
TYPESCRIPT = TypeScript(
    date_format=TypeScript.DateFormat.ISO,
    datetime_format=TypeScript.DatetimeFormat.ISO,
    sequence_format=TypeScript.SequenceFormat.ARRAY,
)


@dataclasses.dataclass(frozen=True)
class _VariableSyntax:
    """Expected output for variable declaration and assignment."""

    declaration: str
    assignment: str


# Maps each language to its declaration and assignment expected output for a
# scalar integer. Both _DECLARATION_PARAMS and _ASSIGNMENT_PARAMS are derived
# from this single source of truth so that adding a language to one
# automatically adds it to the other.
_VARIABLE_SYNTAX: dict[Language, _VariableSyntax] = {
    PYTHON: _VariableSyntax(
        declaration="my_var = 42", assignment="my_var = 42"
    ),
    JAVASCRIPT: _VariableSyntax(
        declaration="const my_var = 42;", assignment="my_var = 42;"
    ),
    TYPESCRIPT: _VariableSyntax(
        declaration="const my_var = 42;", assignment="my_var = 42;"
    ),
    GO: _VariableSyntax(declaration="my_var := 42", assignment="my_var = 42"),
    RUBY: _VariableSyntax(declaration="my_var = 42", assignment="my_var = 42"),
    CSHARP: _VariableSyntax(
        declaration="var my_var = 42;", assignment="my_var = 42;"
    ),
    CPP: _VariableSyntax(
        declaration="auto my_var = 42;", assignment="my_var = 42;"
    ),
    JAVA: _VariableSyntax(
        declaration="var my_var = 42;", assignment="my_var = 42;"
    ),
    KOTLIN: _VariableSyntax(
        declaration="val my_var = 42", assignment="my_var = 42"
    ),
    SWIFT: _VariableSyntax(
        declaration="let my_var = 42", assignment="my_var = 42"
    ),
    RUST: _VariableSyntax(
        declaration="let my_var = 42;", assignment="my_var = 42;"
    ),
    PHP: _VariableSyntax(
        declaration="$my_var = 42;", assignment="$my_var = 42;"
    ),
    HASKELL: _VariableSyntax(
        declaration="my_var = 42", assignment="my_var = 42"
    ),
    DART: _VariableSyntax(
        declaration="final my_var = 42;", assignment="my_var = 42;"
    ),
    ELIXIR: _VariableSyntax(
        declaration="my_var = 42", assignment="my_var = 42"
    ),
    FSHARP: _VariableSyntax(
        declaration="let my_var: Val = FInt 42L",
        assignment="let my_var: Val = FInt 42L",
    ),
    CLOJURE: _VariableSyntax(
        declaration="(def my_var 42)", assignment="(def my_var 42)"
    ),
    SCALA: _VariableSyntax(
        declaration="val my_var = 42", assignment="my_var = 42"
    ),
    R(
        date_format=R.DateFormat.ISO,
        datetime_format=R.DatetimeFormat.ISO,
        empty_dict_key=R.EmptyDictKey.POSITIONAL,
        sequence_format=R.SequenceFormat.LIST,
    ): _VariableSyntax(declaration="my_var <- 42", assignment="my_var <- 42"),
}

_DECLARATION_PARAMS = [
    (lang, syntax.declaration) for lang, syntax in _VARIABLE_SYNTAX.items()
]
_ASSIGNMENT_PARAMS = [
    (lang, syntax.assignment) for lang, syntax in _VARIABLE_SYNTAX.items()
]


@pytest.mark.parametrize(
    argnames=("language", "expected"), argvalues=_DECLARATION_PARAMS
)
def test_variable_declaration_json(
    *, language: Language, expected: str
) -> None:
    """Each language produces correct variable declaration syntax."""
    result = literalize_json(
        json_string="42",
        language=language,
        line_prefix="",
        indent="    ",
        wrap=False,
        variable_name="my_var",
        new_variable=True,
    )
    assert result == expected


@pytest.mark.parametrize(
    argnames=("language", "expected"), argvalues=_DECLARATION_PARAMS
)
def test_variable_declaration_yaml(
    *, language: Language, expected: str
) -> None:
    """Each language produces correct variable declaration syntax for YAML."""
    result = literalize_yaml(
        yaml_string="42\n",
        language=language,
        line_prefix="",
        indent="    ",
        wrap=False,
        variable_name="my_var",
        new_variable=True,
    )
    assert result == expected


def test_variable_declaration_none_no_wrap() -> None:
    """Omitting variable_name leaves output unchanged."""
    result = literalize_json(
        json_string="[1, 2]",
        language=PYTHON,
        line_prefix="",
        indent="    ",
        wrap=True,
        variable_name=None,
        new_variable=True,
    )
    assert result == "(\n    1,\n    2,\n)"


@pytest.mark.parametrize(
    argnames=("language", "expected"), argvalues=_ASSIGNMENT_PARAMS
)
def test_existing_variable_assignment_json(
    *, language: Language, expected: str
) -> None:
    """Each language produces correct existing-variable assignment
    syntax.
    """
    result = literalize_json(
        json_string="42",
        language=language,
        line_prefix="",
        indent="    ",
        wrap=False,
        variable_name="my_var",
        new_variable=False,
    )
    assert result == expected


@pytest.mark.parametrize(
    argnames=("language", "expected"), argvalues=_ASSIGNMENT_PARAMS
)
def test_existing_variable_assignment_yaml(
    *, language: Language, expected: str
) -> None:
    """Each language produces correct existing-variable assignment syntax
    for YAML.
    """
    result = literalize_yaml(
        yaml_string="42\n",
        language=language,
        line_prefix="",
        indent="    ",
        wrap=False,
        variable_name="my_var",
        new_variable=False,
    )
    assert result == expected
