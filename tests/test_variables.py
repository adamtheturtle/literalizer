"""Tests for variable declaration and assignment in literalizer
converter.
"""

import dataclasses
import textwrap

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
    date_format=Clojure.date_formats.ISO,
    datetime_format=Clojure.datetime_formats.ISO,
    bytes_format=Clojure.bytes_formats.HEX,
    sequence_format=Clojure.sequence_formats.VECTOR,
)
CPP = Cpp(
    date_format=Cpp.date_formats.CPP,
    datetime_format=Cpp.datetime_formats.CPP,
    bytes_format=Cpp.bytes_formats.HEX,
    sequence_format=Cpp.sequence_formats.INITIALIZER_LIST,
)
CSHARP = CSharp(
    date_format=CSharp.date_formats.CSHARP,
    datetime_format=CSharp.datetime_formats.CSHARP,
    bytes_format=CSharp.bytes_formats.HEX,
    sequence_format=CSharp.sequence_formats.ARRAY,
)
DART = Dart(
    date_format=Dart.date_formats.DART,
    datetime_format=Dart.datetime_formats.DART,
    bytes_format=Dart.bytes_formats.HEX,
    sequence_format=Dart.sequence_formats.LIST,
)
ELIXIR = Elixir(
    date_format=Elixir.date_formats.ISO,
    datetime_format=Elixir.datetime_formats.ISO,
    bytes_format=Elixir.bytes_formats.HEX,
    sequence_format=Elixir.sequence_formats.LIST,
)
FSHARP = FSharp(
    date_format=FSharp.date_formats.ISO,
    datetime_format=FSharp.datetime_formats.ISO,
    bytes_format=FSharp.bytes_formats.HEX,
    sequence_format=FSharp.sequence_formats.LIST,
)
GO = Go(
    date_format=Go.date_formats.GO,
    datetime_format=Go.datetime_formats.GO,
    bytes_format=Go.bytes_formats.HEX,
    sequence_format=Go.sequence_formats.SLICE,
)
HASKELL = Haskell(
    date_format=Haskell.date_formats.ISO,
    datetime_format=Haskell.datetime_formats.ISO,
    bytes_format=Haskell.bytes_formats.HEX,
    sequence_format=Haskell.sequence_formats.LIST,
)
JAVA = Java(
    date_format=Java.date_formats.JAVA,
    datetime_format=Java.datetime_formats.INSTANT,
    bytes_format=Java.bytes_formats.HEX,
    sequence_format=Java.sequence_formats.ARRAY,
)
JAVASCRIPT = JavaScript(
    date_format=JavaScript.date_formats.JS,
    datetime_format=JavaScript.datetime_formats.JS,
    bytes_format=JavaScript.bytes_formats.HEX,
    sequence_format=JavaScript.sequence_formats.ARRAY,
)
KOTLIN = Kotlin(
    date_format=Kotlin.date_formats.KOTLIN,
    datetime_format=Kotlin.datetime_formats.KOTLIN,
    bytes_format=Kotlin.bytes_formats.HEX,
    sequence_format=Kotlin.sequence_formats.LIST,
)
PHP = Php(
    date_format=Php.date_formats.PHP,
    datetime_format=Php.datetime_formats.PHP,
    bytes_format=Php.bytes_formats.HEX,
    sequence_format=Php.sequence_formats.ARRAY,
)
PYTHON = Python(
    date_format=Python.date_formats.PYTHON,
    datetime_format=Python.datetime_formats.PYTHON,
    bytes_format=Python.bytes_formats.HEX,
    sequence_format=Python.sequence_formats.TUPLE,
    set_format=Python.set_formats.SET,
    variable_type_hints=Python.variable_type_hints_formats.AUTO,
)
PYTHON_ALWAYS_HINTS = Python(
    date_format=Python.date_formats.PYTHON,
    datetime_format=Python.datetime_formats.PYTHON,
    bytes_format=Python.bytes_formats.HEX,
    sequence_format=Python.sequence_formats.TUPLE,
    set_format=Python.set_formats.SET,
    variable_type_hints=Python.variable_type_hints_formats.ALWAYS,
)
RUBY = Ruby(
    date_format=Ruby.date_formats.RUBY,
    datetime_format=Ruby.datetime_formats.RUBY,
    bytes_format=Ruby.bytes_formats.HEX,
    sequence_format=Ruby.sequence_formats.ARRAY,
)
RUST = Rust(
    date_format=Rust.date_formats.RUST,
    datetime_format=Rust.datetime_formats.RUST,
    bytes_format=Rust.bytes_formats.HEX,
    sequence_format=Rust.sequence_formats.VEC,
)
SCALA = Scala(
    date_format=Scala.date_formats.ISO,
    datetime_format=Scala.datetime_formats.ISO,
    bytes_format=Scala.bytes_formats.HEX,
    sequence_format=Scala.sequence_formats.LIST,
)
SWIFT = Swift(
    date_format=Swift.date_formats.ISO,
    datetime_format=Swift.datetime_formats.ISO,
    bytes_format=Swift.bytes_formats.HEX,
    sequence_format=Swift.sequence_formats.ARRAY,
)
TYPESCRIPT = TypeScript(
    date_format=TypeScript.date_formats.JS,
    datetime_format=TypeScript.datetime_formats.JS,
    bytes_format=TypeScript.bytes_formats.HEX,
    sequence_format=TypeScript.sequence_formats.ARRAY,
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
_VARIABLE_SYNTAX: dict[Language, _VariableSyntax] = {  # pyrefly: ignore[bad-assignment]
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
        declaration="_Any my_var = 42;", assignment="my_var = 42;"
    ),
    JAVA: _VariableSyntax(
        declaration="var my_var = 42;", assignment="my_var = 42;"
    ),
    KOTLIN: _VariableSyntax(
        declaration="val my_var = 42", assignment="my_var = 42"
    ),
    SWIFT: _VariableSyntax(
        declaration="let my_var: Any = 42", assignment="my_var = 42"
    ),
    RUST: _VariableSyntax(
        declaration="let my_var = 42;", assignment="my_var = 42;"
    ),
    PHP: _VariableSyntax(
        declaration="$my_var = 42;", assignment="$my_var = 42;"
    ),
    HASKELL: _VariableSyntax(
        declaration=(
            "data Val = HInt Integer\n"
            "instance Num Val where\n"
            "    fromInteger = HInt\n"
            '    a + b = error "not implemented"\n'
            '    a * b = error "not implemented"\n'
            '    abs a = error "not implemented"\n'
            '    signum a = error "not implemented"\n'
            "    negate (HInt n) = HInt (negate n)\n"
            '    negate _ = error "not implemented"\n'
            "my_var = 42"
        ),
        assignment=(
            "data Val = HInt Integer\n"
            "instance Num Val where\n"
            "    fromInteger = HInt\n"
            '    a + b = error "not implemented"\n'
            '    a * b = error "not implemented"\n'
            '    abs a = error "not implemented"\n'
            '    signum a = error "not implemented"\n'
            "    negate (HInt n) = HInt (negate n)\n"
            '    negate _ = error "not implemented"\n'
            "my_var = 42"
        ),
    ),
    DART: _VariableSyntax(
        declaration="final my_var = 42;", assignment="my_var = 42;"
    ),
    ELIXIR: _VariableSyntax(
        declaration="my_var = 42", assignment="my_var = 42"
    ),
    FSHARP: _VariableSyntax(
        declaration=(
            "type Val =\n    | FInt of int64\nlet my_var: Val = FInt 42L"
        ),
        assignment=(
            "type Val =\n    | FInt of int64\nlet my_var: Val = FInt 42L"
        ),
    ),
    CLOJURE: _VariableSyntax(
        declaration="(def my_var 42)", assignment="(def my_var 42)"
    ),
    SCALA: _VariableSyntax(
        declaration="val my_var = 42", assignment="my_var = 42"
    ),
    R(
        date_format=R.date_formats.R,
        datetime_format=R.datetime_formats.R,
        empty_dict_key=R.EmptyDictKey.POSITIONAL,
        bytes_format=R.bytes_formats.HEX,
        sequence_format=R.sequence_formats.LIST,
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
        pre_indent_level=0,
        include_delimiters=False,
        variable_name="my_var",
        new_variable=True,
        error_on_coercion=False,
    )
    assert result.code == expected


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
        pre_indent_level=0,
        include_delimiters=False,
        variable_name="my_var",
        new_variable=True,
        error_on_coercion=False,
    )
    assert result.code == expected


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
        pre_indent_level=0,
        include_delimiters=False,
        variable_name="my_var",
        new_variable=False,
        error_on_coercion=False,
    )
    assert result.code == expected


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
        pre_indent_level=0,
        include_delimiters=False,
        variable_name="my_var",
        new_variable=False,
        error_on_coercion=False,
    )
    assert result.code == expected


@pytest.mark.parametrize(
    argnames=("json_input", "expected"),
    argvalues=[
        ("42", "my_var: int = 42"),
        ("3.14", "my_var: float = 3.14"),
        ("true", "my_var: bool = True"),
        ("false", "my_var: bool = False"),
        ("null", "my_var: None = None"),
        ('"hello"', 'my_var: str = "hello"'),
    ],
)
def test_python_always_type_hints_scalars(
    *, json_input: str, expected: str
) -> None:
    """Python with ALWAYS variable_type_hints adds type annotations
    for scalar values.
    """
    result = literalize_json(
        json_string=json_input,
        language=PYTHON_ALWAYS_HINTS,
        pre_indent_level=0,
        include_delimiters=False,
        variable_name="my_var",
        new_variable=True,
        error_on_coercion=False,
    )
    assert result.code == expected


def test_python_always_type_hints_dict() -> None:
    """Python ALWAYS hints infer dict type for wrapped dicts."""
    result = literalize_json(
        json_string='{"a": 1}',
        language=PYTHON_ALWAYS_HINTS,
        pre_indent_level=0,
        include_delimiters=True,
        variable_name="my_var",
        new_variable=True,
        error_on_coercion=False,
    )
    expected = textwrap.dedent(
        text="""\
        my_var: dict[str, int] = {
            "a": 1,
        }"""
    )
    assert result.code == expected


def test_python_always_type_hints_tuple() -> None:
    """Python ALWAYS hints infer tuple type for wrapped sequences."""
    result = literalize_json(
        json_string="[1, 2]",
        language=PYTHON_ALWAYS_HINTS,
        pre_indent_level=0,
        include_delimiters=True,
        variable_name="my_var",
        new_variable=True,
        error_on_coercion=False,
    )
    expected = textwrap.dedent(
        text="""\
        my_var: tuple[int, ...] = (
            1,
            2,
        )"""
    )
    assert result.code == expected


def test_python_always_type_hints_list() -> None:
    """Python ALWAYS hints infer list type when sequence_format is
    LIST.
    """
    lang = Python(
        date_format=Python.date_formats.PYTHON,
        datetime_format=Python.datetime_formats.PYTHON,
        bytes_format=Python.bytes_formats.HEX,
        sequence_format=Python.sequence_formats.LIST,
        set_format=Python.set_formats.SET,
        variable_type_hints=Python.variable_type_hints_formats.ALWAYS,
    )
    result = literalize_json(
        json_string="[1, 2]",
        language=lang,
        pre_indent_level=0,
        include_delimiters=True,
        variable_name="my_var",
        new_variable=True,
        error_on_coercion=False,
    )
    expected = textwrap.dedent(
        text="""\
        my_var: list[int] = [
            1,
            2,
        ]"""
    )
    assert result.code == expected


def test_python_always_type_hints_assignment_no_hint() -> None:
    """Python ALWAYS hints do not add type hints for assignments."""
    result = literalize_json(
        json_string="42",
        language=PYTHON_ALWAYS_HINTS,
        pre_indent_level=0,
        include_delimiters=False,
        variable_name="my_var",
        new_variable=False,
        error_on_coercion=False,
    )
    assert result.code == "my_var = 42"


def test_python_always_type_hints_set_with_colon_in_string() -> None:
    """A set element containing ``": `` is not misidentified as a dict."""
    yaml_string = "!!set\n? 'a\": b'\n"
    result = literalize_yaml(
        yaml_string=yaml_string,
        language=PYTHON_ALWAYS_HINTS,
        pre_indent_level=0,
        include_delimiters=True,
        variable_name="my_var",
        new_variable=True,
        error_on_coercion=False,
    )
    expected = textwrap.dedent(
        text="""\
        my_var: set[str] = {
            "a\\": b",
        }"""
    )
    assert result.code == expected


def test_python_always_type_hints_set_of_integers() -> None:
    """A set of integers is correctly identified as set, not dict."""
    yaml_string = "!!set\n? 1\n? 2\n? 3\n"
    result = literalize_yaml(
        yaml_string=yaml_string,
        language=PYTHON_ALWAYS_HINTS,
        pre_indent_level=0,
        include_delimiters=True,
        variable_name="my_var",
        new_variable=True,
        error_on_coercion=False,
    )
    expected = textwrap.dedent(
        text="""\
        my_var: set[int] = {
            1,
            2,
            3,
        }"""
    )
    assert result.code == expected


def test_python_always_type_hints_nested_list_in_list() -> None:
    """Nested collections get recursive type hints, not Any."""
    result = literalize_json(
        json_string='[true, "hi", [1, 2], null]',
        language=PYTHON_ALWAYS_HINTS,
        pre_indent_level=0,
        include_delimiters=True,
        variable_name="my_var",
        new_variable=True,
        error_on_coercion=False,
    )
    expected = textwrap.dedent(
        text="""\
        my_var: tuple[bool | str | tuple[int, ...] | None, ...] = (
            True,
            "hi",
            (1, 2),
            None,
        )"""
    )
    assert result.code == expected


def test_python_always_type_hints_dict_with_list_values() -> None:
    """Dict with list values infers recursive type hints."""
    result = literalize_json(
        json_string='{"key": [1, 2, 3]}',
        language=PYTHON_ALWAYS_HINTS,
        pre_indent_level=0,
        include_delimiters=True,
        variable_name="my_var",
        new_variable=True,
        error_on_coercion=False,
    )
    expected = textwrap.dedent(
        text="""\
        my_var: dict[str, tuple[int, ...]] = {
            "key": (1, 2, 3),
        }"""
    )
    assert result.code == expected


def test_python_always_type_hints_empty_list() -> None:
    """Empty collections still use Any since element type is unknown."""
    result = literalize_json(
        json_string="[]",
        language=PYTHON_ALWAYS_HINTS,
        pre_indent_level=0,
        include_delimiters=True,
        variable_name="my_var",
        new_variable=True,
        error_on_coercion=False,
    )
    assert "tuple[Any, ...]" in result.code


def test_python_always_type_hints_ordered_dicts_in_sequence() -> None:
    """Ordered dicts in a sequence merge value types into one hint."""
    yaml_input = textwrap.dedent(
        text="""\
        ---
        - !!omap
          - name: Alice
          - draft: true
        - !!omap
          - name: Bob"""
    )
    result = literalize_yaml(
        yaml_string=yaml_input,
        language=PYTHON_ALWAYS_HINTS,
        pre_indent_level=0,
        include_delimiters=True,
        variable_name="my_var",
        new_variable=True,
        error_on_coercion=False,
    )
    assert "tuple[OrderedDict[str, str | bool], ...]" in result.code
