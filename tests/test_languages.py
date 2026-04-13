"""Language-specific tests for literalizer converter."""

import json
import re
import textwrap

import pytest
from pygments.lexers import find_lexer_class_by_name

import literalizer.languages
from literalizer import (
    CallStyleConfig,
    CallStyleKind,
    InputFormat,
    Language,
    literalize,
    literalize_call,
)
from literalizer._language import LanguageCls
from literalizer.exceptions import NullInCollectionError
from literalizer.languages import (
    Cobol,
    Cpp,
    CSharp,
    Fortran,
    Go,
    Haskell,
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
from literalizer.languages.cobol import (
    _bump_levels,  # pyright: ignore[reportPrivateUsage]
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
    variable_type_hints=Python.variable_type_hints_formats.AUTO,
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
    result = literalize(
        source=json.dumps(obj=[[True, None, "hi", [1, 2]]]),
        input_format=InputFormat.JSON,
        language=language,
        pre_indent_level=0,
        include_delimiters=False,
        variable_name=None,
        new_variable=True,
        error_on_coercion=False,
    )
    assert result.code == expected


def test_ruby_dict() -> None:
    """Ruby dicts use => syntax and nil."""
    result = literalize(
        source=json.dumps(obj=[{"key": None}]),
        input_format=InputFormat.JSON,
        language=RUBY,
        pre_indent_level=0,
        include_delimiters=False,
        variable_name=None,
        new_variable=True,
        error_on_coercion=False,
    )
    assert result.code == '{"key" => nil},'


def test_dict_ruby() -> None:
    """Ruby dict renders with => syntax."""
    result = literalize(
        source=json.dumps(obj={"user_1": "team_alpha"}),
        input_format=InputFormat.JSON,
        language=RUBY,
        pre_indent_level=1,
        include_delimiters=False,
        variable_name=None,
        new_variable=True,
        error_on_coercion=False,
    )
    assert result.code == '    "user_1" => "team_alpha",'


def test_java_dict_include_delimiters_no_multiline_trailing_comma() -> None:
    """Java Map.ofEntries() must not have a trailing comma before the
    closing paren.
    """
    result = literalize(
        source=json.dumps(obj={"name": "Alice", "age": 30}),
        input_format=InputFormat.JSON,
        language=JAVA,
        pre_indent_level=0,
        include_delimiters=True,
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
    assert result.code == expected


def test_java_dict_skips_null_values() -> None:
    """Java Map.ofEntries() omits entries with null values."""
    data = {"name": "Alice", "score": None, "age": 30}
    result = literalize(
        source=json.dumps(obj=data),
        input_format=InputFormat.JSON,
        language=JAVA,
        pre_indent_level=0,
        include_delimiters=True,
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
    assert result.code == expected


def test_java_dict_skips_null_values_no_include_delimiters() -> None:
    """Java dict omits null entries even without include_delimiters."""
    result = literalize(
        source=json.dumps(obj={"a": None, "b": 1}),
        input_format=InputFormat.JSON,
        language=JAVA,
        pre_indent_level=0,
        include_delimiters=False,
        variable_name=None,
        new_variable=True,
        error_on_coercion=False,
    )
    expected = 'Map.entry("b", 1)'
    assert result.code == expected


def test_java_dict_all_null_values_include_delimiters() -> None:
    """Java dict where all values are null produces empty
    Map.ofEntries().
    """
    result = literalize(
        source=json.dumps(obj={"a": None, "b": None}),
        input_format=InputFormat.JSON,
        language=JAVA,
        pre_indent_level=0,
        include_delimiters=True,
        variable_name=None,
        new_variable=True,
        error_on_coercion=False,
    )
    assert result.code == "Map.ofEntries()"


def test_java_dict_all_null_values_with_pre_indent_level() -> None:
    """Java all-null dict with pre_indent_level includes line_prefix."""
    result = literalize(
        source=json.dumps(obj={"a": None, "b": None}),
        input_format=InputFormat.JSON,
        language=JAVA,
        pre_indent_level=1,
        include_delimiters=True,
        variable_name=None,
        new_variable=True,
        error_on_coercion=False,
    )
    assert result.code == "    Map.ofEntries()"


def test_java_yaml_dict_null_values_with_comments() -> None:
    """Java YAML dict with null values and comments does not crash."""
    yaml_string = "# comment\nname: Alice\nscore: null\n"
    result = literalize(
        source=yaml_string,
        input_format=InputFormat.YAML,
        language=JAVA,
        pre_indent_level=0,
        include_delimiters=True,
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
    assert result.code == expected


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
    result = literalize(
        source=yaml_string,
        input_format=InputFormat.YAML,
        language=JAVA,
        pre_indent_level=0,
        include_delimiters=True,
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
    assert result.code == expected


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
    result = literalize(
        source=yaml_string,
        input_format=InputFormat.YAML,
        language=JAVA,
        pre_indent_level=0,
        include_delimiters=True,
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
    assert result.code == expected


def test_java_yaml_all_null_dict_with_trailing_comments() -> None:
    """All-null Java YAML dict with trailing comments does not duplicate
    delimiters.
    """
    yaml_string = "a: null\nb: null\n# trailing\n"
    result = literalize(
        source=yaml_string,
        input_format=InputFormat.YAML,
        language=JAVA,
        pre_indent_level=0,
        include_delimiters=True,
        variable_name=None,
        new_variable=True,
        error_on_coercion=False,
    )
    expected = "Map.ofEntries()\n    // trailing"
    assert result.code == expected


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
    result = literalize(
        source=yaml_string,
        input_format=InputFormat.YAML,
        language=JAVA,
        pre_indent_level=0,
        include_delimiters=True,
        variable_name=None,
        new_variable=True,
        error_on_coercion=False,
    )
    ordered_map_inline = (
        "new java.util.ArrayList<>(java.util.Arrays.asList("
        'Map.entry("name", "Alice"), Map.entry("age", 30)))'
    )
    expected = f"new Object[]{{\n    {ordered_map_inline}\n}}"
    assert result.code == expected


def test_java_sequence_include_delimiters_uses_braces() -> None:
    """Java wrapped sequences use ``new Object[]{…}``."""
    result = literalize(
        source=json.dumps(obj=[1, "hello", True]),
        input_format=InputFormat.JSON,
        language=JAVA,
        pre_indent_level=0,
        include_delimiters=True,
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
    assert result.code == expected


@pytest.mark.parametrize(
    argnames=("json_input", "expected"),
    argvalues=[
        (
            [1, 2, 3],
            textwrap.dedent(
                text="""\
                new int[]{
                    1,
                    2,
                    3
                }"""
            ),
        ),
        (
            ["hello", "world"],
            textwrap.dedent(
                text="""\
                new String[]{
                    "hello",
                    "world"
                }"""
            ),
        ),
        (
            [1, "hello", True],
            textwrap.dedent(
                text="""\
                new Object[]{
                    1,
                    "hello",
                    true
                }"""
            ),
        ),
    ],
    ids=["all_int", "all_string", "mixed"],
)
def test_java_typed_array_opener(
    *, json_input: list[object], expected: str
) -> None:
    """Java uses typed array openers inferred from element types."""
    result = literalize(
        source=json.dumps(obj=json_input),
        input_format=InputFormat.JSON,
        language=JAVA,
        pre_indent_level=0,
        include_delimiters=True,
        variable_name=None,
        new_variable=True,
        error_on_coercion=False,
    )
    assert result.code == expected


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
    result = literalize(
        source=yaml_string,
        input_format=InputFormat.YAML,
        language=Matlab(
            date_format=Matlab.date_formats.ISO,
            datetime_format=Matlab.datetime_formats.ISO,
            bytes_format=Matlab.bytes_formats.HEX,
            sequence_format=Matlab.sequence_formats.CELL_ARRAY,
        ),
        pre_indent_level=0,
        include_delimiters=False,
        variable_name=None,
        new_variable=True,
        error_on_coercion=False,
    )
    assert result.code == expected


def test_matlab_dict_key_with_quote() -> None:
    """MATLAB struct keys containing double quotes are decoded correctly.

    The ``_decode_matlab_string_expr`` helper must handle ``""`` inside a
    double-quoted string, which represents a literal ``"`` character.
    """
    yaml_string = '{"hello \\"world\\"": 1}\n'
    result = literalize(
        source=yaml_string,
        input_format=InputFormat.YAML,
        language=Matlab(
            date_format=Matlab.date_formats.ISO,
            datetime_format=Matlab.datetime_formats.ISO,
            bytes_format=Matlab.bytes_formats.HEX,
            sequence_format=Matlab.sequence_formats.CELL_ARRAY,
        ),
        pre_indent_level=0,
        include_delimiters=False,
        variable_name=None,
        new_variable=True,
        error_on_coercion=False,
    )
    assert result.code == "'hello \"world\"', 1"


def test_toml_integer_dict_key() -> None:
    """TOML dict entry with an integer key passes through without
    modification.

    Integer keys are not quoted strings, so the bare-key optimisation is
    skipped and the raw formatted key is used directly.
    """
    result = literalize(
        source="1: value\n",
        input_format=InputFormat.YAML,
        language=TOML,
        pre_indent_level=0,
        include_delimiters=True,
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
    assert result.code == expected


def test_toml_non_quoted_dict_key() -> None:
    """TOML format_dict_entry rejects a key that is not a quoted
    string.
    """
    with pytest.raises(
        expected_exception=ValueError,
        match="Expected a quoted",
    ):
        TOML.dict_format_config.format_entry("plain_key", "value", '"value"')


def test_cobol_string_control_characters() -> None:
    """COBOL string literals replace control characters with spaces."""
    result = literalize(
        source='"line1\\nline2"\n',
        input_format=InputFormat.YAML,
        language=COBOL,
        pre_indent_level=0,
        include_delimiters=False,
        variable_name=None,
        new_variable=True,
        error_on_coercion=False,
    )
    assert result.code == '"line1 line2"'


def test_cobol_string_tab_characters() -> None:
    """COBOL string literals replace tab characters with spaces."""
    result = literalize(
        source='"col1\\tcol2"\n',
        input_format=InputFormat.YAML,
        language=COBOL,
        pre_indent_level=0,
        include_delimiters=False,
        variable_name=None,
        new_variable=True,
        error_on_coercion=False,
    )
    assert result.code == '"col1 col2"'


def test_cobol_level_number_cap() -> None:
    """COBOL level numbers are capped at 49 for deeply nested
    structures.
    """
    yaml_string = textwrap.dedent(
        text="""\
        a:
          b:
            c:
              d:
                e:
                  f:
                    g:
                      h:
                        i:
                          value: deep
        """
    )
    result = literalize(
        source=yaml_string,
        input_format=InputFormat.YAML,
        language=COBOL,
        pre_indent_level=1,
        include_delimiters=True,
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
    assert result.code == expected


def test_cobol_key_name_trailing_hyphen_after_truncation() -> None:
    """COBOL data names must not end with a hyphen after truncation."""
    long_key = "a-b-c-d-e-f-g-h-i-j-k-l-m-n-o"
    yaml_string = f'"{long_key}": 1\n'
    result = literalize(
        source=yaml_string,
        input_format=InputFormat.YAML,
        language=COBOL,
        pre_indent_level=1,
        include_delimiters=True,
        variable_name=None,
        new_variable=True,
        error_on_coercion=False,
    )
    for line in result.code.splitlines():
        stripped = line.strip()
        if stripped.startswith("05 F-"):
            name = stripped.split()[1]
            assert not name.endswith("-")


def test_fortran_continuation_with_escaped_quote_and_comment() -> None:
    """Line continuation handles escaped quotes before inline comments."""
    yaml_string = "host: it's here  # a comment\nport: 80  # another\n"
    result = literalize(
        source=yaml_string,
        input_format=InputFormat.YAML,
        language=FORTRAN,
        pre_indent_level=0,
        variable_name="cfg",
        include_delimiters=True,
        new_variable=True,
        error_on_coercion=False,
    )
    assert "'it''s here'" in result.code
    assert "&  !" in result.code


def test_java_list_format() -> None:
    """Java LIST format uses ``List.of(...)`` for non-null sequences."""
    spec = Java(
        sequence_format=Java.sequence_formats.LIST,
    )
    result = literalize(
        source=json.dumps(obj=[1, "hello", True]),
        input_format=InputFormat.JSON,
        language=spec,
        pre_indent_level=0,
        include_delimiters=True,
        variable_name=None,
        new_variable=True,
        error_on_coercion=False,
    )
    expected = textwrap.dedent(
        text="""\
        List.of(
            1,
            "hello",
            true
        )"""
    )
    assert result.code == expected


def test_java_list_rejects_null_elements() -> None:
    """Java's ``List.of()`` does not accept null elements."""
    spec = Java(
        sequence_format=Java.sequence_formats.LIST,
    )
    expected_msg = re.escape(
        pattern="Java's List.of() does not accept null elements"
        " (got 3 items, including null). "
        "Use sequence_format=ARRAY instead."
    )
    with pytest.raises(
        expected_exception=NullInCollectionError,
        match=f"^{expected_msg}$",
    ):
        literalize(
            source=json.dumps(obj=[1, None, "hello"]),
            input_format=InputFormat.JSON,
            language=spec,
            pre_indent_level=0,
            include_delimiters=True,
            variable_name=None,
            new_variable=True,
            error_on_coercion=False,
        )


_SORTED_LANGUAGES: list[LanguageCls] = sorted(
    literalizer.languages.ALL_LANGUAGES,
    key=lambda c: c.__name__,
)


@pytest.mark.parametrize(
    argnames="language_cls",
    argvalues=_SORTED_LANGUAGES,
    ids=[c.__name__ for c in _SORTED_LANGUAGES],
)
def test_pygments_name_is_valid(
    *,
    language_cls: LanguageCls,
) -> None:
    """Every language's ``pygments_name`` is recognized by Pygments."""
    if language_cls.pygments_name is None:
        return
    # Raises ClassNotFound if the name is not a valid Pygments alias.
    find_lexer_class_by_name(_alias=language_cls.pygments_name)


@pytest.mark.parametrize(
    argnames="language_cls",
    argvalues=_SORTED_LANGUAGES,
    ids=[c.__name__ for c in _SORTED_LANGUAGES],
)
def test_wrap_in_file_methods_callable(
    *,
    language_cls: LanguageCls,
) -> None:
    """Every language's wrap_in_file and wrap_combined_in_file are
    callable.
    """
    wrapped = language_cls.wrap_in_file(
        content="x = 1",
        variable_name="x",
        body_preamble=(),
    )
    assert isinstance(wrapped, str)
    combined = language_cls.wrap_combined_in_file(
        declaration="x = 1",
        assignment="x = 2",
        variable_name="x",
        body_preamble=(),
    )
    assert isinstance(combined, str)


def test_python_no_any_import_when_all_defaults_overridden() -> None:
    """When all Python default collection types are non-Any, the
    ``from typing import Any`` import is not emitted.
    """
    spec = Python(
        default_set_element_type="str",
        default_sequence_element_type="str",
        default_dict_value_type="str",
        default_dict_key_type="str",
    )
    result = literalize(
        source="{}\n",
        input_format=InputFormat.YAML,
        language=spec,
        pre_indent_level=0,
        include_delimiters=True,
        variable_name="my_data",
        new_variable=True,
        error_on_coercion=False,
    )
    assert result.code == "my_data: dict[str, str] = {}"
    assert "Any" not in "".join(result.preamble)


def test_literalize_call_per_element_false() -> None:
    """Literalize_call with per_element=False passes the whole value."""
    result = literalize_call(
        source="[1, 2, 3]",
        input_format=InputFormat.JSON,
        language=Python(),
        call_function="process",
        call_params=["data"],
        per_element=False,
    )
    assert "process(" in result.code
    assert "1," in result.code


def test_literalize_call_missing_keyword_separator_raises() -> None:
    """Literalize_call raises ValueError for keyword style without
    separator.
    """

    class BadLang(Python):
        """Python variant with missing keyword_separator."""

    lang = BadLang()
    lang.call_style_config = CallStyleConfig(
        kind=CallStyleKind.KEYWORD,
    )
    with pytest.raises(
        expected_exception=ValueError,
        match="keyword_separator",
    ):
        literalize_call(
            source="- [1]",
            input_format=InputFormat.YAML,
            language=lang,
            call_function="f",
            call_params=["x"],
        )


def test_literalize_call_per_element_non_list_raises() -> None:
    """Literalize_call raises TypeError for non-list with per_element."""
    with pytest.raises(expected_exception=TypeError, match="top-level list"):
        literalize_call(
            source='"hello"',
            input_format=InputFormat.JSON,
            language=Python(),
            call_function="process",
            call_params=["value"],
            per_element=True,
        )


def test_literalize_call_positional_style() -> None:
    """Cover the POSITIONAL branch of _format_call_args."""
    result = literalize_call(
        source="- [1, 2]",
        input_format=InputFormat.YAML,
        language=Java(),
        call_function="process",
        call_params=["a", "b"],
    )
    assert result.code == "process(1, 2);"


def test_literalize_call_body_preamble() -> None:
    """Cover the computed.body branch in literalize_call."""
    result = literalize_call(
        source="- [hello, 1]",
        input_format=InputFormat.YAML,
        language=Haskell(),
        call_function="f",
        call_params=["a", "b"],
    )
    assert result.body_preamble
    assert "data" in "\n".join(result.body_preamble)


def test_js_call_stub_console() -> None:
    """Cover the console branch of _js_call_stub."""
    spec = JavaScript()
    assert not spec.format_call_stub("console.log", [])


def test_cobol_bump_levels_rejects_non_level_line() -> None:
    """_bump_levels raises ValueError for lines without a level number."""
    with pytest.raises(expected_exception=ValueError, match="Expected COBOL"):
        _bump_levels(content="not a level line")
