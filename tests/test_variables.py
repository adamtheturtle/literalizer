"""Tests for variable declaration and assignment in literalizer
converter.
"""

import dataclasses
import textwrap

import pytest

from literalizer import (
    ExistingVariable,
    InputFormat,
    Language,
    NewVariable,
    literalize,
)
from literalizer.exceptions import IncompatibleFormatsError
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
        declaration="let my_var: Any = 42", assignment="my_var = 42"
    ),
    RUST: _VariableSyntax(
        declaration="let my_var = 42;", assignment="my_var = 42;"
    ),
    PHP: _VariableSyntax(
        declaration="$my_var = 42;", assignment="$my_var = 42;"
    ),
    HASKELL: _VariableSyntax(
        declaration=textwrap.dedent(
            text="""\
            data Val = HInt Integer
            instance Num Val where
                fromInteger = HInt
                a + b = error "not implemented"
                a * b = error "not implemented"
                abs a = error "not implemented"
                signum a = error "not implemented"
                negate (HInt n) = HInt (negate n)
                negate _ = error "not implemented"
            my_var :: Val
            my_var = 42"""
        ),
        assignment=textwrap.dedent(
            text="""\
            data Val = HInt Integer
            instance Num Val where
                fromInteger = HInt
                a + b = error "not implemented"
                a * b = error "not implemented"
                abs a = error "not implemented"
                signum a = error "not implemented"
                negate (HInt n) = HInt (negate n)
                negate _ = error "not implemented"
            my_var = 42"""
        ),
    ),
    DART: _VariableSyntax(
        declaration="final my_var = 42;", assignment="my_var = 42;"
    ),
    ELIXIR: _VariableSyntax(
        declaration="my_var = 42", assignment="my_var = 42"
    ),
    FSHARP: _VariableSyntax(
        declaration=textwrap.dedent(
            text="""\
            type Val =
                | FInt of int64
            let my_var: Val = FInt 42L"""
        ),
        assignment=textwrap.dedent(
            text="""\
            type Val =
                | FInt of int64
            let my_var: Val = FInt 42L"""
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
        empty_dict_key=R.empty_dict_keys.POSITIONAL,
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
    result = literalize(
        source="42",
        input_format=InputFormat.JSON,
        language=language,
        pre_indent_level=0,
        include_delimiters=False,
        variable_form=NewVariable(name="my_var"),
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
    result = literalize(
        source="42",
        input_format=InputFormat.JSON,
        language=language,
        pre_indent_level=0,
        include_delimiters=False,
        variable_form=ExistingVariable(name="my_var"),
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
    result = literalize(
        source=json_input,
        input_format=InputFormat.JSON,
        language=PYTHON_ALWAYS_HINTS,
        pre_indent_level=0,
        include_delimiters=False,
        variable_form=NewVariable(name="my_var"),
        error_on_coercion=False,
    )
    assert result.code == expected


def test_python_always_type_hints_assignment_no_hint() -> None:
    """Python ALWAYS hints do not add type hints for assignments."""
    result = literalize(
        source="42",
        input_format=InputFormat.JSON,
        language=PYTHON_ALWAYS_HINTS,
        pre_indent_level=0,
        include_delimiters=False,
        variable_form=ExistingVariable(name="my_var"),
        error_on_coercion=False,
    )
    assert result.code == "my_var = 42"


def test_python_always_type_hints_set_with_colon_in_string() -> None:
    """A set element containing ``": `` is not misidentified as a dict."""
    yaml_string = "!!set\n? 'a\": b'\n"
    result = literalize(
        source=yaml_string,
        input_format=InputFormat.YAML,
        language=PYTHON_ALWAYS_HINTS,
        pre_indent_level=0,
        include_delimiters=True,
        variable_form=NewVariable(name="my_var"),
        error_on_coercion=False,
    )
    expected = textwrap.dedent(
        text="""\
        my_var: set[str] = {
            "a\\": b",
        }"""
    )
    assert result.code == expected


def test_python_always_type_hints_nested_list_in_list() -> None:
    """Nested collections get recursive type hints, not Any."""
    result = literalize(
        source='[true, "hi", [1, 2], null]',
        input_format=InputFormat.JSON,
        language=PYTHON_ALWAYS_HINTS,
        pre_indent_level=0,
        include_delimiters=True,
        variable_form=NewVariable(name="my_var"),
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
    result = literalize(
        source='{"key": [1, 2, 3]}',
        input_format=InputFormat.JSON,
        language=PYTHON_ALWAYS_HINTS,
        pre_indent_level=0,
        include_delimiters=True,
        variable_form=NewVariable(name="my_var"),
        error_on_coercion=False,
    )
    expected = textwrap.dedent(
        text="""\
        my_var: dict[str, tuple[int, ...]] = {
            "key": (1, 2, 3),
        }"""
    )
    assert result.code == expected


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
    result = literalize(
        source=yaml_input,
        input_format=InputFormat.YAML,
        language=PYTHON_ALWAYS_HINTS,
        pre_indent_level=0,
        include_delimiters=True,
        variable_form=NewVariable(name="my_var"),
        error_on_coercion=False,
    )
    expected = textwrap.dedent(
        text="""\
        my_var: tuple[OrderedDict[str, str | bool], ...] = (
            OrderedDict([("name", "Alice"), ("draft", True)]),
            OrderedDict([("name", "Bob")]),
        )""",
    )
    assert result.code == expected


RUST_CONST = Rust(
    date_format=Rust.date_formats.ISO,
    datetime_format=Rust.datetime_formats.ISO,
    bytes_format=Rust.bytes_formats.HEX,
    sequence_format=Rust.sequence_formats.ARRAY,
    declaration_style=Rust.declaration_styles.CONST,
)


def test_rust_const_bytes() -> None:
    """Rust CONST with bytes uses ``&str`` type."""
    yaml_input = "!!binary |\n  SGVsbG8="
    result = literalize(
        source=yaml_input,
        input_format=InputFormat.YAML,
        language=RUST_CONST,
        pre_indent_level=0,
        include_delimiters=False,
        variable_form=NewVariable(name="my_var"),
        error_on_coercion=False,
    )
    assert result.code == 'const my_var: &str = "48656c6c6f";'


def test_rust_const_date() -> None:
    """Rust CONST with ISO dates uses ``&str`` type."""
    result = literalize(
        source="2024-01-15",
        input_format=InputFormat.YAML,
        language=RUST_CONST,
        pre_indent_level=0,
        include_delimiters=False,
        variable_form=NewVariable(name="my_var"),
        error_on_coercion=False,
    )
    assert result.code == 'const my_var: &str = "2024-01-15";'


def test_rust_const_datetime() -> None:
    """Rust CONST with ISO datetimes uses ``&str`` type."""
    result = literalize(
        source="2024-01-15T12:30:00",
        input_format=InputFormat.YAML,
        language=RUST_CONST,
        pre_indent_level=0,
        include_delimiters=False,
        variable_form=NewVariable(name="my_var"),
        error_on_coercion=False,
    )
    assert result.code == 'const my_var: &str = "2024-01-15T12:30:00";'


def test_rust_const_single_element_tuple() -> None:
    """Rust CONST single-element tuple has trailing comma in type."""
    rust_tuple = Rust(
        date_format=Rust.date_formats.ISO,
        datetime_format=Rust.datetime_formats.ISO,
        bytes_format=Rust.bytes_formats.HEX,
        sequence_format=Rust.sequence_formats.TUPLE,
        declaration_style=Rust.declaration_styles.CONST,
    )
    result = literalize(
        source="[42]",
        input_format=InputFormat.JSON,
        language=rust_tuple,
        pre_indent_level=0,
        include_delimiters=True,
        variable_form=NewVariable(name="my_var"),
        error_on_coercion=False,
    )
    expected = textwrap.dedent(
        text="""\
        const my_var: (i32,) = (
            42,
        );"""
    )
    assert result.code == expected


def test_rust_const_set() -> None:
    """Rust CONST with set produces ``HashSet`` type annotation."""
    yaml_input = "!!set\n? a\n? b\n"
    result = literalize(
        source=yaml_input,
        input_format=InputFormat.YAML,
        language=RUST_CONST,
        pre_indent_level=0,
        include_delimiters=True,
        variable_form=NewVariable(name="my_var"),
        error_on_coercion=False,
    )
    expected = textwrap.dedent(
        text="""\
        const my_var: HashSet<&str> = HashSet::from([
            "a",
            "b",
        ]);"""
    )
    assert result.code == expected


def test_rust_const_empty_set() -> None:
    """Rust CONST with empty set uses default element type."""
    yaml_input = "!!set {}"
    result = literalize(
        source=yaml_input,
        input_format=InputFormat.YAML,
        language=RUST_CONST,
        pre_indent_level=0,
        include_delimiters=True,
        variable_form=NewVariable(name="my_var"),
        error_on_coercion=False,
    )
    assert result.code == (
        "const my_var: HashSet<String> = HashSet::<String>::new();"
    )


def test_rust_const_dict() -> None:
    """Rust CONST with dict produces ``HashMap`` type annotation."""
    result = literalize(
        source='{"a": "b"}',
        input_format=InputFormat.JSON,
        language=RUST_CONST,
        pre_indent_level=0,
        include_delimiters=True,
        variable_form=NewVariable(name="my_var"),
        error_on_coercion=False,
    )
    expected = textwrap.dedent(
        text="""\
        const my_var: HashMap<&str, &str> = HashMap::from([
            ("a", "b"),
        ]);"""
    )
    assert result.code == expected


def test_rust_const_empty_dict() -> None:
    """Rust CONST with empty dict uses default key/value types."""
    result = literalize(
        source="{}",
        input_format=InputFormat.JSON,
        language=RUST_CONST,
        pre_indent_level=0,
        include_delimiters=True,
        variable_form=NewVariable(name="my_var"),
        error_on_coercion=False,
    )
    assert result.code == (
        "const my_var: HashMap<String, String>"
        " = HashMap::<String, String>::from([]);"
    )


def test_rust_const_dict_mixed_values() -> None:
    """Rust CONST with mixed dict values falls back to ``&str``."""
    result = literalize(
        source='{"a": 1, "b": "x"}',
        input_format=InputFormat.JSON,
        language=RUST_CONST,
        pre_indent_level=0,
        include_delimiters=True,
        variable_form=NewVariable(name="my_var"),
        error_on_coercion=False,
    )
    expected = textwrap.dedent(
        text="""\
        const my_var: HashMap<&str, &str> = HashMap::from([
            ("a", "1"),
            ("b", "x"),
        ]);"""
    )
    assert result.code == expected


def test_rust_const_btree_set() -> None:
    """Rust CONST with ``BTREE_SET`` uses ``BTreeSet`` type annotation."""
    rust_btree_set = Rust(
        date_format=Rust.date_formats.ISO,
        datetime_format=Rust.datetime_formats.ISO,
        bytes_format=Rust.bytes_formats.HEX,
        sequence_format=Rust.sequence_formats.ARRAY,
        set_format=Rust.set_formats.BTREE_SET,
        declaration_style=Rust.declaration_styles.CONST,
    )
    result = literalize(
        source="!!set\n? a\n? b\n",
        input_format=InputFormat.YAML,
        language=rust_btree_set,
        pre_indent_level=0,
        include_delimiters=True,
        variable_form=NewVariable(name="my_var"),
        error_on_coercion=False,
    )
    expected = textwrap.dedent(
        text="""\
        const my_var: BTreeSet<&str> = BTreeSet::from([
            "a",
            "b",
        ]);"""
    )
    assert result.code == expected


def test_rust_const_btree_map() -> None:
    """Rust CONST with ``BTREE_MAP`` uses ``BTreeMap`` type annotation."""
    rust_btree_map = Rust(
        date_format=Rust.date_formats.ISO,
        datetime_format=Rust.datetime_formats.ISO,
        bytes_format=Rust.bytes_formats.HEX,
        sequence_format=Rust.sequence_formats.ARRAY,
        dict_format=Rust.dict_formats.BTREE_MAP,
        declaration_style=Rust.declaration_styles.CONST,
    )
    result = literalize(
        source='{"a": "b"}',
        input_format=InputFormat.JSON,
        language=rust_btree_map,
        pre_indent_level=0,
        include_delimiters=True,
        variable_form=NewVariable(name="my_var"),
        error_on_coercion=False,
    )
    expected = textwrap.dedent(
        text="""\
        const my_var: BTreeMap<&str, &str> = BTreeMap::from([
            ("a", "b"),
        ]);"""
    )
    assert result.code == expected


def test_rust_const_widened_int_array() -> None:
    """Rust CONST with mixed-size integers widens to the largest type."""
    result = literalize(
        source="[1, 2147483648]",
        input_format=InputFormat.JSON,
        language=RUST_CONST,
        pre_indent_level=0,
        include_delimiters=True,
        variable_form=NewVariable(name="my_var"),
        error_on_coercion=False,
    )
    expected = textwrap.dedent(
        text="""\
        const my_var: [i64; 2] = [
            1,
            2147483648i64,
        ];"""
    )
    assert result.code == expected


def test_rust_const_i128_array() -> None:
    """Rust CONST with an integer exceeding i64 range uses i128."""
    result = literalize(
        source="[9223372036854775808]",
        input_format=InputFormat.JSON,
        language=RUST_CONST,
        pre_indent_level=0,
        include_delimiters=True,
        variable_form=NewVariable(name="my_var"),
        error_on_coercion=False,
    )
    expected = textwrap.dedent(
        text="""\
        const my_var: [i128; 1] = [
            9223372036854775808i128,
        ];"""
    )
    assert result.code == expected


def test_rust_const_nested_list() -> None:
    """Rust CONST with nested list produces recursive type."""
    result = literalize(
        source="[[1, 2], [3, 4]]",
        input_format=InputFormat.JSON,
        language=RUST_CONST,
        pre_indent_level=0,
        include_delimiters=True,
        variable_form=NewVariable(name="my_var"),
        error_on_coercion=False,
    )
    expected = textwrap.dedent(
        text="""\
        const my_var: [[i32; 2]; 2] = [
            [1, 2],
            [3, 4],
        ];"""
    )
    assert result.code == expected


def test_rust_tuple_format_type_annotation_raises() -> None:
    """TUPLE.format_type_annotation raises for incompatible format."""
    with pytest.raises(expected_exception=IncompatibleFormatsError):
        Rust.sequence_formats.TUPLE.format_type_annotation(
            element_type="i32",
            length=2,
        )


def test_rust_vec_format_type_annotation() -> None:
    """``format_type_annotation`` returns ``Vec<T>`` for vector format."""
    result = Rust.sequence_formats.VEC.format_type_annotation(
        element_type="i32",
        length=3,
    )
    assert result == "Vec<i32>"


def test_rust_const_vec_raises() -> None:
    """Rust CONST with vector format raises."""
    with pytest.raises(
        expected_exception=IncompatibleFormatsError, match="VEC"
    ):
        Rust(
            declaration_style=Rust.declaration_styles.CONST,
            sequence_format=Rust.sequence_formats.VEC,
        )


def test_rust_static_vec_raises() -> None:
    """Rust STATIC with vector format raises."""
    with pytest.raises(
        expected_exception=IncompatibleFormatsError, match="VEC"
    ):
        Rust(
            declaration_style=Rust.declaration_styles.STATIC,
            sequence_format=Rust.sequence_formats.VEC,
        )
