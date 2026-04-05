"""Tests for literalizer TOML conversion."""

import textwrap

import pytest

from literalizer import (
    InputFormat,
    Language,
    literalize,
)
from literalizer._comments import extract_toml_comments
from literalizer.exceptions import (
    HeterogeneousCoercionError,
    ParseError,
    TOMLParseError,
)
from literalizer.languages import (
    Go,
    Haskell,
    JavaScript,
    Mojo,
    Python,
    VisualBasic,
)

PYTHON = Python(
    date_format=Python.date_formats.PYTHON,
    datetime_format=Python.datetime_formats.PYTHON,
    bytes_format=Python.bytes_formats.HEX,
    sequence_format=Python.sequence_formats.TUPLE,
    set_format=Python.set_formats.SET,
    variable_type_hints=Python.variable_type_hints_formats.AUTO,
)
GO = Go(
    date_format=Go.date_formats.GO,
    datetime_format=Go.datetime_formats.GO,
    bytes_format=Go.bytes_formats.HEX,
    sequence_format=Go.sequence_formats.SLICE,
)
JAVASCRIPT = JavaScript(
    date_format=JavaScript.date_formats.JS,
    datetime_format=JavaScript.datetime_formats.JS,
    bytes_format=JavaScript.bytes_formats.HEX,
    sequence_format=JavaScript.sequence_formats.ARRAY,
)


def test_dict_python() -> None:
    """Python dict renders key-value pairs from TOML."""
    toml_string = 'user_1 = "team_alpha"\nuser_2 = "team_alpha"\n'
    result = literalize(
        source=toml_string,
        input_format=InputFormat.TOML,
        language=PYTHON,
        pre_indent_level=1,
        include_delimiters=False,
        variable_name=None,
        new_variable=True,
        error_on_coercion=False,
    )
    expected = '    "user_1": "team_alpha",\n    "user_2": "team_alpha",'
    assert result.code == expected


def test_dict_include_delimiters() -> None:
    """Wrapping a dict adds braces and indentation."""
    toml_string = "a = 1\nb = 2\n"
    result = literalize(
        source=toml_string,
        input_format=InputFormat.TOML,
        language=PYTHON,
        pre_indent_level=0,
        include_delimiters=True,
        variable_name=None,
        new_variable=True,
        error_on_coercion=False,
    )
    expected = textwrap.dedent(
        text="""\
        {
            "a": 1,
            "b": 2,
        }"""
    )
    assert result.code == expected


def test_empty_table() -> None:
    """An empty TOML string produces an empty dict."""
    result = literalize(
        source="",
        input_format=InputFormat.TOML,
        language=PYTHON,
        pre_indent_level=0,
        include_delimiters=True,
        variable_name=None,
        new_variable=True,
        error_on_coercion=False,
    )
    assert result.code == "{}"


def test_integers() -> None:
    """Integer values in a TOML array are rendered literally."""
    toml_string = "values = [42, 0, -7]\n"
    result = literalize(
        source=toml_string,
        input_format=InputFormat.TOML,
        language=PYTHON,
        pre_indent_level=0,
        include_delimiters=True,
        variable_name=None,
        new_variable=True,
        error_on_coercion=False,
    )
    expected = textwrap.dedent(
        text="""\
        {
            "values": (42, 0, -7),
        }"""
    )
    assert result.code == expected


def test_floats() -> None:
    """Float values are rendered literally."""
    toml_string = "values = [1000.0, 3.14]\n"
    result = literalize(
        source=toml_string,
        input_format=InputFormat.TOML,
        language=PYTHON,
        pre_indent_level=0,
        include_delimiters=True,
        variable_name=None,
        new_variable=True,
        error_on_coercion=False,
    )
    expected = textwrap.dedent(
        text="""\
        {
            "values": (1000.0, 3.14),
        }"""
    )
    assert result.code == expected


def test_booleans() -> None:
    """Boolean values are formatted per language."""
    toml_string = "enabled = true\nverbose = false\n"
    result = literalize(
        source=toml_string,
        input_format=InputFormat.TOML,
        language=PYTHON,
        pre_indent_level=0,
        include_delimiters=True,
        variable_name=None,
        new_variable=True,
        error_on_coercion=False,
    )
    expected = textwrap.dedent(
        text="""\
        {
            "enabled": True,
            "verbose": False,
        }"""
    )
    assert result.code == expected


def test_nested_table() -> None:
    """Nested TOML tables are rendered as nested dicts."""
    toml_string = '[server]\nname = "test"\nport = 8080\n'
    result = literalize(
        source=toml_string,
        input_format=InputFormat.TOML,
        language=PYTHON,
        pre_indent_level=0,
        include_delimiters=True,
        variable_name=None,
        new_variable=True,
        error_on_coercion=False,
    )
    expected = textwrap.dedent(
        text="""\
        {
            "server": {"name": "test", "port": 8080},
        }"""
    )
    assert result.code == expected


def test_array_of_tables() -> None:
    """TOML array-of-tables produces a list of dicts."""
    toml_string = '[[items]]\nname = "a"\n\n[[items]]\nname = "b"\n'
    result = literalize(
        source=toml_string,
        input_format=InputFormat.TOML,
        language=PYTHON,
        pre_indent_level=0,
        include_delimiters=True,
        variable_name=None,
        new_variable=True,
        error_on_coercion=False,
    )
    expected = textwrap.dedent(
        text="""\
        {
            "items": ({"name": "a"}, {"name": "b"}),
        }"""
    )
    assert result.code == expected


def test_date_python() -> None:
    """TOML date values are converted to Python date literals."""
    toml_string = "created = 2024-01-15\n"
    result = literalize(
        source=toml_string,
        input_format=InputFormat.TOML,
        language=PYTHON,
        pre_indent_level=0,
        include_delimiters=True,
        variable_name=None,
        new_variable=True,
        error_on_coercion=False,
    )
    expected = textwrap.dedent(
        text="""\
        {
            "created": datetime.date(year=2024, month=1, day=15),
        }"""
    )
    assert result.code == expected


def test_datetime_python() -> None:
    """TOML datetime values are converted to Python datetime literals."""
    toml_string = "updated = 2024-01-15T10:30:00\n"
    result = literalize(
        source=toml_string,
        input_format=InputFormat.TOML,
        language=PYTHON,
        pre_indent_level=0,
        include_delimiters=True,
        variable_name=None,
        new_variable=True,
        error_on_coercion=False,
    )
    assert '"updated": datetime.datetime(' in result.code
    assert "year=2024" in result.code
    assert "minute=30" in result.code


def test_time_coerced_to_string() -> None:
    """TOML time values are coerced to ISO-format strings."""
    toml_string = "start = 10:30:00\n"
    result = literalize(
        source=toml_string,
        input_format=InputFormat.TOML,
        language=PYTHON,
        pre_indent_level=0,
        include_delimiters=True,
        variable_name=None,
        new_variable=True,
        error_on_coercion=False,
    )
    expected = textwrap.dedent(
        text="""\
        {
            "start": "10:30:00",
        }"""
    )
    assert result.code == expected


def test_invalid_toml() -> None:
    """``literalize_toml`` raises on invalid TOML."""
    with pytest.raises(expected_exception=TOMLParseError):
        literalize(
            source="not = [valid toml",
            input_format=InputFormat.TOML,
            language=PYTHON,
            pre_indent_level=0,
            include_delimiters=False,
            variable_name=None,
            new_variable=True,
            error_on_coercion=False,
        )


def test_invalid_toml_is_parse_error() -> None:
    """``TOMLParseError`` is a subclass of ``ParseError``."""
    with pytest.raises(expected_exception=ParseError):
        literalize(
            source="not = [valid toml",
            input_format=InputFormat.TOML,
            language=PYTHON,
            pre_indent_level=0,
            include_delimiters=False,
            variable_name=None,
            new_variable=True,
            error_on_coercion=False,
        )


def test_variable_declaration() -> None:
    """Variable name wraps the output in a declaration."""
    toml_string = 'name = "alice"\n'
    result = literalize(
        source=toml_string,
        input_format=InputFormat.TOML,
        language=JAVASCRIPT,
        pre_indent_level=0,
        include_delimiters=True,
        variable_name="config",
        new_variable=True,
        error_on_coercion=False,
    )
    expected = textwrap.dedent(
        text="""\
        const config = {
            "name": "alice",
        };"""
    )
    assert result.code == expected


def test_variable_assignment() -> None:
    """``new_variable=False`` uses assignment syntax."""
    toml_string = 'name = "alice"\n'
    result = literalize(
        source=toml_string,
        input_format=InputFormat.TOML,
        language=PYTHON,
        pre_indent_level=0,
        include_delimiters=True,
        variable_name="config",
        new_variable=False,
        error_on_coercion=False,
    )
    expected = textwrap.dedent(
        text="""\
        config = {
            "name": "alice",
        }"""
    )
    assert result.code == expected


def test_go_output() -> None:
    """TOML input renders correctly for Go."""
    toml_string = 'name = "test"\ncount = 42\n'
    result = literalize(
        source=toml_string,
        input_format=InputFormat.TOML,
        language=GO,
        pre_indent_level=0,
        include_delimiters=True,
        variable_name=None,
        new_variable=True,
        error_on_coercion=False,
    )
    expected = 'map[string]any{\n\t"name": "test",\n\t"count": 42,\n}'
    assert result.code == expected


MOJO = Mojo(
    date_format=Mojo.date_formats.ISO,
    datetime_format=Mojo.datetime_formats.ISO,
    bytes_format=Mojo.bytes_formats.HEX,
    sequence_format=Mojo.sequence_formats.LIST,
)


def test_error_on_coercion_raises() -> None:
    """Error_on_coercion raises for heterogeneous TOML arrays."""
    toml_string = "values = [1, 2.5, 3]\n"
    with pytest.raises(expected_exception=HeterogeneousCoercionError):
        literalize(
            source=toml_string,
            input_format=InputFormat.TOML,
            language=MOJO,
            pre_indent_level=0,
            include_delimiters=True,
            variable_name=None,
            new_variable=True,
            error_on_coercion=True,
        )


def test_error_on_coercion_no_raise_homogeneous() -> None:
    """Error_on_coercion does not raise for homogeneous TOML arrays."""
    toml_string = "values = [1, 2, 3]\n"
    result = literalize(
        source=toml_string,
        input_format=InputFormat.TOML,
        language=PYTHON,
        pre_indent_level=0,
        include_delimiters=True,
        variable_name=None,
        new_variable=True,
        error_on_coercion=True,
    )
    expected = textwrap.dedent(
        text="""\
        {
            "values": (1, 2, 3),
        }"""
    )
    assert result.code == expected


@pytest.mark.parametrize(
    argnames=("toml_string", "language", "expected"),
    argvalues=[
        ("v = 42\n", PYTHON, '{\n    "v": 42,\n}'),
        ("v = 3.14\n", PYTHON, '{\n    "v": 3.14,\n}'),
        ('v = "hello"\n', PYTHON, '{\n    "v": "hello",\n}'),
        ("v = true\n", PYTHON, '{\n    "v": True,\n}'),
        ("v = false\n", PYTHON, '{\n    "v": False,\n}'),
    ],
)
def test_scalar_types(
    *, toml_string: str, language: Language, expected: str
) -> None:
    """Various TOML scalar types render correctly."""
    result = literalize(
        source=toml_string,
        input_format=InputFormat.TOML,
        language=language,
        pre_indent_level=0,
        include_delimiters=True,
        variable_name=None,
        new_variable=True,
        error_on_coercion=False,
    )
    assert result.code == expected


def test_body_preamble() -> None:
    """Languages with body preamble (e.g. Haskell) include it in code."""
    haskell = Haskell(
        date_format=Haskell.date_formats.ISO,
        datetime_format=Haskell.datetime_formats.ISO,
        bytes_format=Haskell.bytes_formats.HEX,
        sequence_format=Haskell.sequence_formats.LIST,
    )
    toml_string = 'name = "alice"\n'
    result = literalize(
        source=toml_string,
        input_format=InputFormat.TOML,
        language=haskell,
        pre_indent_level=0,
        include_delimiters=True,
        variable_name=None,
        new_variable=True,
        error_on_coercion=False,
    )
    assert result.body_preamble
    assert result.body_preamble[0] in result.code


def test_inline_comment_preserved() -> None:
    """Inline TOML comments appear in the output."""
    toml_string = 'host = "localhost"  # default host\nport = 8080\n'
    result = literalize(
        source=toml_string,
        input_format=InputFormat.TOML,
        language=PYTHON,
        pre_indent_level=0,
        include_delimiters=True,
        variable_name=None,
        new_variable=True,
        error_on_coercion=False,
    )
    expected = textwrap.dedent(
        text="""\
        {
            "host": "localhost",  # default host
            "port": 8080,
        }"""
    )
    assert result.code == expected


def test_before_comment_preserved() -> None:
    """Standalone comments before a key appear before that element."""
    toml_string = '# Server host\nhost = "localhost"\nport = 8080\n'
    result = literalize(
        source=toml_string,
        input_format=InputFormat.TOML,
        language=PYTHON,
        pre_indent_level=0,
        include_delimiters=True,
        variable_name=None,
        new_variable=True,
        error_on_coercion=False,
    )
    expected = textwrap.dedent(
        text="""\
        {
            # Server host
            "host": "localhost",
            "port": 8080,
        }"""
    )
    assert result.code == expected


def test_trailing_comment_preserved() -> None:
    """A comment after the last key appears as a trailing comment."""
    toml_string = 'host = "localhost"\n# end\n'
    result = literalize(
        source=toml_string,
        input_format=InputFormat.TOML,
        language=PYTHON,
        pre_indent_level=0,
        include_delimiters=True,
        variable_name=None,
        new_variable=True,
        error_on_coercion=False,
    )
    expected = textwrap.dedent(
        text="""\
        {
            "host": "localhost",
            # end
        }"""
    )
    assert result.code == expected


def test_mixed_comments_preserved() -> None:
    """Inline, before, and trailing comments all preserved together."""
    toml_string = (
        "# Server configuration\n"
        'host = "localhost"  # default host\n'
        "port = 8080\n"
    )
    result = literalize(
        source=toml_string,
        input_format=InputFormat.TOML,
        language=PYTHON,
        pre_indent_level=0,
        include_delimiters=True,
        variable_name=None,
        new_variable=True,
        error_on_coercion=False,
    )
    expected = textwrap.dedent(
        text="""\
        {
            # Server configuration
            "host": "localhost",  # default host
            "port": 8080,
        }"""
    )
    assert result.code == expected


def test_comments_go_output() -> None:
    """TOML comments render with Go comment syntax."""
    toml_string = '# Config\nhost = "localhost"  # default\nport = 8080\n'
    result = literalize(
        source=toml_string,
        input_format=InputFormat.TOML,
        language=GO,
        pre_indent_level=0,
        include_delimiters=True,
        variable_name=None,
        new_variable=True,
        error_on_coercion=False,
    )
    expected = (
        "map[string]any{\n"
        "\t// Config\n"
        '\t"host": "localhost",  // default\n'
        '\t"port": 8080,\n'
        "}"
    )
    assert result.code == expected


def test_no_comments_unchanged() -> None:
    """TOML without comments produces the same output as before."""
    toml_string = 'name = "test"\ncount = 42\n'
    result = literalize(
        source=toml_string,
        input_format=InputFormat.TOML,
        language=PYTHON,
        pre_indent_level=0,
        include_delimiters=True,
        variable_name=None,
        new_variable=True,
        error_on_coercion=False,
    )
    expected = textwrap.dedent(
        text="""\
        {
            "name": "test",
            "count": 42,
        }"""
    )
    assert result.code == expected


def test_comments_without_delimiters() -> None:
    """TOML comments work correctly without delimiters."""
    toml_string = '# header\nhost = "localhost"  # inline\nport = 8080\n'
    result = literalize(
        source=toml_string,
        input_format=InputFormat.TOML,
        language=PYTHON,
        pre_indent_level=0,
        include_delimiters=False,
        variable_name=None,
        new_variable=True,
        error_on_coercion=False,
    )
    expected = '# header\n"host": "localhost",  # inline\n"port": 8080,'
    assert result.code == expected


def test_comments_with_variable_declaration() -> None:
    """TOML comments work with variable wrapping."""
    toml_string = '# config\nhost = "localhost"  # default\n'
    result = literalize(
        source=toml_string,
        input_format=InputFormat.TOML,
        language=JAVASCRIPT,
        pre_indent_level=0,
        include_delimiters=True,
        variable_name="config",
        new_variable=True,
        error_on_coercion=False,
    )
    expected = textwrap.dedent(
        text="""\
        const config = {
            // config
            "host": "localhost",  // default
        };"""
    )
    assert result.code == expected


VISUAL_BASIC = VisualBasic(
    date_format=VisualBasic.date_formats.ISO,
    datetime_format=VisualBasic.datetime_formats.ISO,
    bytes_format=VisualBasic.bytes_formats.HEX,
    sequence_format=VisualBasic.sequence_formats.ARRAY,
)


def test_comments_language_without_collection_comments() -> None:
    """Comments are prepended for languages without collection support."""
    toml_string = '# header\nhost = "localhost"  # inline\n'
    result = literalize(
        source=toml_string,
        input_format=InputFormat.TOML,
        language=VISUAL_BASIC,
        pre_indent_level=0,
        include_delimiters=True,
        variable_name="config",
        new_variable=True,
        error_on_coercion=False,
    )
    assert "' header" in result.code
    assert "' inline" in result.code


def test_extract_toml_comments_non_document() -> None:
    """``extract_toml_comments`` returns empty for non-document input."""
    result = extract_toml_comments(toml_doc={"not": "a document"})
    assert result.elements == ()
    assert result.trailing == ()


def test_comments_with_blank_lines() -> None:
    """Blank lines between keys do not produce spurious comments."""
    toml_string = 'host = "localhost"\n\nport = 8080\n'
    result = literalize(
        source=toml_string,
        input_format=InputFormat.TOML,
        language=PYTHON,
        pre_indent_level=0,
        include_delimiters=True,
        variable_name=None,
        new_variable=True,
        error_on_coercion=False,
    )
    expected = textwrap.dedent(
        text="""\
        {
            "host": "localhost",
            "port": 8080,
        }"""
    )
    assert result.code == expected
