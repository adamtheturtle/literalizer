"""Language-specific tests for literalizer converter."""

import json
import textwrap

import pytest

from literalizer import (
    Language,
    literalize_json,
    literalize_yaml,
)
from literalizer.languages import (
    Cobol,
    Cpp,
    CSharp,
    Fortran,
    Go,
    Java,
    JavaScript,
    Kotlin,
    Matlab,
    Python,
    Ruby,
    Rust,
    Toml,
    TypeScript,
)

COBOL = Cobol(
    date_format=Cobol.date_formats.ISO,
    datetime_format=Cobol.datetime_formats.ISO,
    bytes_format=Cobol.bytes_formats.HEX,
    sequence_format=Cobol.sequence_formats.SEQUENCE,
)
CPP = Cpp(
    date_format=Cpp.date_formats.CPP,
    datetime_format=Cpp.datetime_formats.CPP,
    bytes_format=Cpp.bytes_formats.HEX,
    sequence_format=Cpp.sequence_formats.INITIALIZER_LIST,
)
FORTRAN = Fortran(
    date_format=Fortran.date_formats.ISO,
    datetime_format=Fortran.datetime_formats.ISO,
    bytes_format=Fortran.bytes_formats.HEX,
    sequence_format=Fortran.sequence_formats.LIST,
)
CSHARP = CSharp(
    date_format=CSharp.date_formats.CSHARP,
    datetime_format=CSharp.datetime_formats.CSHARP,
    bytes_format=CSharp.bytes_formats.HEX,
    sequence_format=CSharp.sequence_formats.ARRAY,
)
GO = Go(
    date_format=Go.date_formats.GO,
    datetime_format=Go.datetime_formats.GO,
    bytes_format=Go.bytes_formats.HEX,
    sequence_format=Go.sequence_formats.SLICE,
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
PYTHON = Python(
    date_format=Python.date_formats.PYTHON,
    datetime_format=Python.datetime_formats.PYTHON,
    bytes_format=Python.bytes_formats.HEX,
    sequence_format=Python.sequence_formats.TUPLE,
    set_format=Python.set_formats.SET,
    variable_type_hints=Python.VariableTypeHints.NONE,
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
TOML = Toml(
    date_format=Toml.date_formats.TOML,
    datetime_format=Toml.datetime_formats.TOML,
    bytes_format=Toml.bytes_formats.HEX,
    sequence_format=Toml.sequence_formats.ARRAY,
)
TYPESCRIPT = TypeScript(
    date_format=TypeScript.date_formats.JS,
    datetime_format=TypeScript.datetime_formats.JS,
    bytes_format=TypeScript.bytes_formats.HEX,
    sequence_format=TypeScript.sequence_formats.ARRAY,
)


@pytest.mark.parametrize(
    argnames=("language", "expected"),
    argvalues=[
        (PYTHON, '(True, None, "hi", (1, 2)),'),
        (JAVASCRIPT, '[true, null, "hi", [1, 2]],'),
        (TYPESCRIPT, '[true, null, "hi", [1, 2]],'),
        (GO, '[]any{true, nil, "hi", []int{1, 2}},'),
        (CPP, '{true, nullptr, "hi", std::vector<int>{1, 2}},'),
        (JAVA, 'new Object[]{true, null, "hi", new int[]{1, 2}}'),
        (CSHARP, 'new object[] {true, (object?)null, "hi", new int[] {1, 2}}'),
        (RUBY, '[true, nil, "hi", [1, 2]],'),
        (KOTLIN, 'listOf<Any?>(true, null, "hi", intArrayOf(1, 2)),'),
        (RUST, 'vec!["True", "None", "hi", "[1, 2]"],'),
    ],
)
def test_language_sequence(*, language: Language, expected: str) -> None:
    """Each language produces the correct sequence literal."""
    result = literalize_json(
        json_string=json.dumps(obj=[[True, None, "hi", [1, 2]]]),
        language=language,
        line_prefix="",
        indent="    ",
        wrap=False,
        variable_name=None,
        new_variable=True,
        error_on_coercion=False,
    )
    assert result == expected


def test_ruby_dict() -> None:
    """Ruby dicts use => syntax and nil."""
    result = literalize_json(
        json_string=json.dumps(obj=[{"key": None}]),
        language=RUBY,
        line_prefix="",
        indent="    ",
        wrap=False,
        variable_name=None,
        new_variable=True,
        error_on_coercion=False,
    )
    assert result == '{"key" => nil},'


def test_dict_ruby() -> None:
    """Ruby dict renders with => syntax."""
    result = literalize_json(
        json_string=json.dumps(obj={"user_1": "team_alpha"}),
        language=RUBY,
        line_prefix="  ",
        indent="    ",
        wrap=False,
        variable_name=None,
        new_variable=True,
        error_on_coercion=False,
    )
    assert result == '  "user_1" => "team_alpha",'


def test_java_dict_wrap_no_multiline_trailing_comma() -> None:
    """Java Map.ofEntries() must not have a trailing comma before the
    closing paren.
    """
    result = literalize_json(
        json_string=json.dumps(obj={"name": "Alice", "age": 30}),
        language=JAVA,
        line_prefix="",
        indent="    ",
        wrap=True,
        variable_name=None,
        new_variable=True,
        error_on_coercion=False,
    )
    expected = textwrap.dedent(
        text="""\
        Map.ofEntries(
            Map.entry("name", "Alice"),
            Map.entry("age", 30)
        )"""
    )
    assert result == expected


def test_java_dict_skips_null_values() -> None:
    """Java Map.ofEntries() omits entries with null values."""
    data = {"name": "Alice", "score": None, "age": 30}
    result = literalize_json(
        json_string=json.dumps(obj=data),
        language=JAVA,
        line_prefix="",
        indent="    ",
        wrap=True,
        variable_name=None,
        new_variable=True,
        error_on_coercion=False,
    )
    expected = textwrap.dedent(
        text="""\
        Map.ofEntries(
            Map.entry("name", "Alice"),
            Map.entry("age", 30)
        )"""
    )
    assert result == expected


def test_java_dict_skips_null_values_no_wrap() -> None:
    """Java dict omits null entries even without wrap."""
    result = literalize_json(
        json_string=json.dumps(obj={"a": None, "b": 1}),
        language=JAVA,
        line_prefix="",
        indent="    ",
        wrap=False,
        variable_name=None,
        new_variable=True,
        error_on_coercion=False,
    )
    expected = 'Map.entry("b", 1)'
    assert result == expected


def test_java_dict_all_null_values_wrap() -> None:
    """Java dict where all values are null produces empty
    Map.ofEntries().
    """
    result = literalize_json(
        json_string=json.dumps(obj={"a": None, "b": None}),
        language=JAVA,
        line_prefix="",
        indent="    ",
        wrap=True,
        variable_name=None,
        new_variable=True,
        error_on_coercion=False,
    )
    assert result == "Map.ofEntries()"


def test_java_yaml_dict_null_values_with_comments() -> None:
    """Java YAML dict with null values and comments does not crash."""
    yaml_string = "# comment\nname: Alice\nscore: null\n"
    result = literalize_yaml(
        yaml_string=yaml_string,
        language=JAVA,
        line_prefix="",
        indent="    ",
        wrap=True,
        variable_name=None,
        new_variable=True,
        error_on_coercion=False,
    )
    expected = textwrap.dedent(
        text="""\
        Map.ofEntries(
            // comment
            Map.entry("name", "Alice")
        )"""
    )
    assert result == expected


def test_java_yaml_dict_null_value_inline_comment_preserved() -> None:
    """Inline comment on a null-valued dict entry is preserved as a before
    comment on the next non-null entry when skip_null_dict_values=True.
    """
    yaml_string = textwrap.dedent(
        text="""\
        host: localhost
        port: null  # not configured yet
        debug: true
        """,
    )
    result = literalize_yaml(
        yaml_string=yaml_string,
        language=JAVA,
        line_prefix="",
        indent="    ",
        wrap=True,
        variable_name=None,
        new_variable=True,
        error_on_coercion=False,
    )
    expected = textwrap.dedent(
        text="""\
        Map.ofEntries(
            Map.entry("host", "localhost"),
            // not configured yet
            Map.entry("debug", true)
        )"""
    )
    assert result == expected


def test_java_yaml_null_value_inline_comment_as_trailing() -> None:
    """Inline comment on a null-valued dict entry at the end becomes a
    trailing comment when skip_null_dict_values=True.
    """
    yaml_string = textwrap.dedent(
        text="""\
        host: localhost
        port: null  # not configured yet
        """,
    )
    result = literalize_yaml(
        yaml_string=yaml_string,
        language=JAVA,
        line_prefix="",
        indent="    ",
        wrap=True,
        variable_name=None,
        new_variable=True,
        error_on_coercion=False,
    )
    expected = textwrap.dedent(
        text="""\
        Map.ofEntries(
            Map.entry("host", "localhost")
            // not configured yet
        )"""
    )
    assert result == expected


def test_java_yaml_all_null_dict_with_trailing_comments() -> None:
    """All-null Java YAML dict with trailing comments does not duplicate
    delimiters.
    """
    yaml_string = "a: null\nb: null\n# trailing\n"
    result = literalize_yaml(
        yaml_string=yaml_string,
        language=JAVA,
        line_prefix="",
        indent="    ",
        wrap=True,
        variable_name=None,
        new_variable=True,
        error_on_coercion=False,
    )
    expected = "Map.ofEntries()\n    // trailing"
    assert result == expected


def test_java_yaml_ordered_map_skips_null_values() -> None:
    """Java YAML ordered map nested in a list filters null values."""
    yaml_string = textwrap.dedent(
        text="""\
        ---
        - !!omap
          - name: Alice
          - score: null
          - age: 30
        """,
    )
    result = literalize_yaml(
        yaml_string=yaml_string,
        language=JAVA,
        line_prefix="",
        indent="    ",
        wrap=True,
        variable_name=None,
        new_variable=True,
        error_on_coercion=False,
    )
    ordered_map_inline = (
        "new java.util.ArrayList<>(java.util.Arrays.asList("
        'Map.entry("name", "Alice"), Map.entry("age", 30)))'
    )
    expected = f"new Object[]{{\n    {ordered_map_inline}\n}}"
    assert result == expected


def test_java_sequence_wrap_uses_braces() -> None:
    """Java wrapped sequences use ``new Object[]{…}``."""
    result = literalize_json(
        json_string=json.dumps(obj=[1, "hello", True]),
        language=JAVA,
        line_prefix="",
        indent="    ",
        wrap=True,
        variable_name=None,
        new_variable=True,
        error_on_coercion=False,
    )
    expected = textwrap.dedent(
        text="""\
        new Object[]{
            1,
            "hello",
            true
        }"""
    )
    assert result == expected


@pytest.mark.parametrize(
    argnames=("json_input", "expected"),
    argvalues=[
        (
            [1, 2, 3],
            "new int[]{\n    1,\n    2,\n    3\n}",
        ),
        (
            ["hello", "world"],
            'new String[]{\n    "hello",\n    "world"\n}',
        ),
        (
            [1, "hello", True],
            'new Object[]{\n    1,\n    "hello",\n    true\n}',
        ),
    ],
    ids=["all_int", "all_string", "mixed"],
)
def test_java_typed_array_opener(
    *, json_input: list[object], expected: str
) -> None:
    """Java uses typed array openers inferred from element types."""
    result = literalize_json(
        json_string=json.dumps(obj=json_input),
        language=JAVA,
        line_prefix="",
        indent="    ",
        wrap=True,
        variable_name=None,
        new_variable=True,
        error_on_coercion=False,
    )
    assert result == expected


@pytest.mark.parametrize(
    argnames=("yaml_string", "expected"),
    argvalues=[
        ("hello\n", '"hello"'),
        ('"hello\\nworld"\n', '"hello" + char(10) + "world"'),
        ('"hello\\tworld"\n', '"hello" + char(9) + "world"'),
        ('"back\\\\slash"\n', '"back\\\\slash"'),
    ],
)
def test_matlab_string_escaping(*, yaml_string: str, expected: str) -> None:
    r"""MATLAB string values escape backslashes and use char() for control
    characters.

    Backslashes are doubled (``\\`` -> ``\\\\``) because MATLAB
    double-quoted strings interpret backslash escape sequences; control
    characters (newlines, tabs, etc.) are represented as ``char(N)``
    expressions joined with ``+``.
    """
    result = literalize_yaml(
        yaml_string=yaml_string,
        language=Matlab(
            date_format=Matlab.date_formats.ISO,
            datetime_format=Matlab.datetime_formats.ISO,
            bytes_format=Matlab.bytes_formats.HEX,
            sequence_format=Matlab.sequence_formats.CELL_ARRAY,
        ),
        line_prefix="",
        indent="    ",
        wrap=False,
        variable_name=None,
        new_variable=True,
        error_on_coercion=False,
    )
    assert result == expected


def test_matlab_dict_key_with_quote() -> None:
    """MATLAB struct keys containing double quotes are decoded correctly.

    The ``_decode_matlab_string_expr`` helper must handle ``""`` inside a
    double-quoted string, which represents a literal ``"`` character.
    """
    yaml_string = '{"hello \\"world\\"": 1}\n'
    result = literalize_yaml(
        yaml_string=yaml_string,
        language=Matlab(
            date_format=Matlab.date_formats.ISO,
            datetime_format=Matlab.datetime_formats.ISO,
            bytes_format=Matlab.bytes_formats.HEX,
            sequence_format=Matlab.sequence_formats.CELL_ARRAY,
        ),
        line_prefix="",
        indent="    ",
        wrap=False,
        variable_name=None,
        new_variable=True,
        error_on_coercion=False,
    )
    assert result == "'hello \"world\"', 1"


def test_toml_integer_dict_key() -> None:
    """TOML dict entry with an integer key passes through without
    modification.

    Integer keys are not quoted strings, so the bare-key optimisation is
    skipped and the raw formatted key is used directly.
    """
    result = literalize_yaml(
        yaml_string="1: value\n",
        language=TOML,
        line_prefix="",
        indent="    ",
        wrap=True,
        variable_name=None,
        new_variable=True,
        error_on_coercion=False,
    )
    expected = textwrap.dedent(
        text="""\
        {
            1 = "value"
        }"""
    )
    assert result == expected


def test_toml_non_quoted_dict_key() -> None:
    """TOML format_dict_entry with a key that is not a quoted string.

    When the key does not start with a double-quote character the
    bare-key optimization is skipped and the key is used verbatim.
    """
    result = TOML.dict_format_config.format_entry("plain_key", '"value"')
    assert result == 'plain_key = "value"'


def test_cobol_string_control_characters() -> None:
    """COBOL string literals replace control characters with spaces."""
    result = literalize_yaml(
        yaml_string='"line1\\nline2"\n',
        language=COBOL,
        line_prefix="",
        indent="    ",
        wrap=False,
        variable_name=None,
        new_variable=True,
        error_on_coercion=False,
    )
    assert result == '"line1 line2"'


def test_cobol_string_tab_characters() -> None:
    """COBOL string literals replace tab characters with spaces."""
    result = literalize_yaml(
        yaml_string='"col1\\tcol2"\n',
        language=COBOL,
        line_prefix="",
        indent="    ",
        wrap=False,
        variable_name=None,
        new_variable=True,
        error_on_coercion=False,
    )
    assert result == '"col1 col2"'


def test_cobol_level_number_cap() -> None:
    """COBOL level numbers are capped at 49 for deeply nested
    structures.
    """
    yaml_string = (
        "a:\n"
        "  b:\n"
        "    c:\n"
        "      d:\n"
        "        e:\n"
        "          f:\n"
        "            g:\n"
        "              h:\n"
        "                i:\n"
        "                  value: deep\n"
    )
    result = literalize_yaml(
        yaml_string=yaml_string,
        language=COBOL,
        line_prefix="    ",
        indent="    ",
        wrap=True,
        variable_name=None,
        new_variable=True,
        error_on_coercion=False,
    )
    expected = (
        "\n"
        "        05 F-A.\n"
        "10 F-B.\n"
        "15 F-C.\n"
        "20 F-D.\n"
        "25 F-E.\n"
        "30 F-F.\n"
        "35 F-G.\n"
        "40 F-H.\n"
        "45 F-I.\n"
        '49 F-VALUE PIC X(4) VALUE "deep".\n'
        "    "
    )
    assert result == expected


def test_cobol_key_name_trailing_hyphen_after_truncation() -> None:
    """COBOL data names must not end with a hyphen after truncation."""
    long_key = "a-b-c-d-e-f-g-h-i-j-k-l-m-n-o"
    yaml_string = f'"{long_key}": 1\n'
    result = literalize_yaml(
        yaml_string=yaml_string,
        language=COBOL,
        line_prefix="    ",
        indent="    ",
        wrap=True,
        variable_name=None,
        new_variable=True,
        error_on_coercion=False,
    )
    for line in result.splitlines():
        stripped = line.strip()
        if stripped.startswith("05 F-"):
            name = stripped.split()[1]
            assert not name.endswith("-")


def test_fortran_continuation_with_escaped_quote_and_comment() -> None:
    """Line continuation handles escaped quotes before inline comments."""
    yaml_string = "host: it's here  # a comment\nport: 80  # another\n"
    result = literalize_yaml(
        yaml_string=yaml_string,
        language=FORTRAN,
        variable_name="cfg",
        indent="    ",
        wrap=True,
        line_prefix="",
        new_variable=True,
        error_on_coercion=False,
    )
    assert "'it''s here'" in result
    assert "&  !" in result
