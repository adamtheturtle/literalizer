"""Language-specific tests for literalizer converter."""

import json
import textwrap

import pytest

from literalizer import (
    Language,
    LanguageSpec,
    literalize_json,
    literalize_yaml,
)
from literalizer._formatters import (
    dict_entry_with_separator,
    fixed_dict_open,
    fixed_sequence_open,
    format_bytes_hex,
    format_date_iso,
    format_datetime_iso,
    format_string_backslash,
    passthrough_sequence_entry,
    passthrough_set_entry,
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
    sequence_format=Cobol.SequenceFormat.SEQUENCE,
)
CPP = Cpp(
    date_format=Cpp.DateFormat.ISO,
    datetime_format=Cpp.DatetimeFormat.ISO,
    sequence_format=Cpp.SequenceFormat.INITIALIZER_LIST,
)
FORTRAN = Fortran(
    sequence_format=Fortran.SequenceFormat.LIST,
)
CSHARP = CSharp(
    date_format=CSharp.DateFormat.ISO,
    datetime_format=CSharp.DatetimeFormat.ISO,
    sequence_format=CSharp.SequenceFormat.ARRAY,
)
GO = Go(
    date_format=Go.DateFormat.ISO,
    datetime_format=Go.DatetimeFormat.ISO,
    sequence_format=Go.SequenceFormat.SLICE,
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
TOML = Toml(
    sequence_format=Toml.SequenceFormat.ARRAY,
)
TYPESCRIPT = TypeScript(
    date_format=TypeScript.DateFormat.ISO,
    datetime_format=TypeScript.DatetimeFormat.ISO,
    sequence_format=TypeScript.SequenceFormat.ARRAY,
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
        (RUST, 'vec![true, None, "hi", vec![1, 2]],'),
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
    )
    expected = "Map.ofEntries()\n    // trailing"
    assert result == expected


def test_java_yaml_omap_skips_null_values() -> None:
    """Java YAML omap nested in a list filters null values."""
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
    )
    omap_inline = (
        "new java.util.ArrayList<>(java.util.Arrays.asList("
        'Map.entry("name", "Alice"), Map.entry("age", 30)))'
    )
    expected = f"new Object[]{{\n    {omap_inline}\n}}"
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
    argnames=("json_input", "expected_open"),
    argvalues=[
        ([1, 2, 3], "new int[]{"),
        (["hello", "world"], "new String[]{"),
        ([1, "hello", True], "new Object[]{"),
    ],
    ids=["all_int", "all_string", "mixed"],
)
def test_java_typed_array_opener(
    *, json_input: list[object], expected_open: str
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
    )
    assert result.startswith(expected_open)


def test_custom_language() -> None:
    """A custom Language works as a language."""
    custom = LanguageSpec(
        null_literal="NIL",
        true_literal="YES",
        false_literal="NO",
        sequence_open=fixed_sequence_open(open_str="<"),
        sequence_close=">",
        dict_open=fixed_dict_open(open_str="{"),
        dict_close="}",
        format_dict_entry=dict_entry_with_separator(separator=" -> "),
        multiline_trailing_comma=True,
        single_element_trailing_comma=False,
        format_string=format_string_backslash,
        format_bytes=format_bytes_hex,
        format_date=format_date_iso,
        format_datetime=format_datetime_iso,
        empty_sequence=None,
        empty_dict=None,
        set_open="<",
        set_close=">",
        empty_set=None,
        format_sequence_entry=passthrough_sequence_entry,
        format_set_entry=passthrough_set_entry,
        comment_prefix="//",
        comment_suffix="",
        omap_open="{",
        omap_close="}",
        format_omap_entry=lambda key, value: f"{key}: {value}",
        multiline_close_indent="",
        element_separator=", ",
        skip_null_dict_values=False,
        coerce_heterogeneous_to_strings=False,
        supports_collection_comments=True,
        format_variable_declaration=PYTHON.format_variable_declaration,
        format_variable_assignment=PYTHON.format_variable_assignment,
        sequence_format=Python.SequenceFormat.TUPLE,
    )
    result = literalize_json(
        json_string=json.dumps(obj=[True, None, "hi"]),
        language=custom,
        line_prefix="",
        indent="    ",
        wrap=False,
        variable_name=None,
        new_variable=True,
    )
    assert result == 'YES,\nNIL,\n"hi",'


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
        language=Matlab(sequence_format=Matlab.SequenceFormat.CELL_ARRAY),
        line_prefix="",
        indent="    ",
        wrap=False,
        variable_name=None,
        new_variable=True,
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
        language=Matlab(sequence_format=Matlab.SequenceFormat.CELL_ARRAY),
        line_prefix="",
        indent="    ",
        wrap=False,
        variable_name=None,
        new_variable=True,
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
    )
    expected = '{\n    1 = "value"\n}'
    assert result == expected


def test_toml_non_quoted_dict_key() -> None:
    """TOML format_dict_entry with a key that is not a quoted string.

    When the key does not start with a double-quote character the
    bare-key optimization is skipped and the key is used verbatim.
    """
    result = TOML.format_dict_entry("plain_key", '"value"')
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
    )
    assert "'it''s here'" in result
    assert "&  !" in result
