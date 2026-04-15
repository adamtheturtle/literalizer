"""Tests for literalizer JSON5 conversion."""

import textwrap

import pytest

from literalizer import (
    ExistingVariable,
    InputFormat,
    Language,
    NewVariable,
    literalize,
)
from literalizer.exceptions import (
    JSON5ParseError,
    ParseError,
)
from literalizer.languages import (
    Go,
    JavaScript,
    Python,
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
    """Python dict renders key-value pairs from JSON5."""
    source = '{user_1: "team_alpha", user_2: "team_alpha"}'
    result = literalize(
        source=source,
        input_format=InputFormat.JSON5,
        language=PYTHON,
        pre_indent_level=1,
        include_delimiters=False,
        variable_form=None,
        error_on_coercion=False,
    )
    expected = '    "user_1": "team_alpha",\n    "user_2": "team_alpha",'
    assert result.code == expected


def test_dict_include_delimiters() -> None:
    """Wrapping a dict adds braces and indentation."""
    source = "{a: 1, b: 2}"
    result = literalize(
        source=source,
        input_format=InputFormat.JSON5,
        language=PYTHON,
        pre_indent_level=0,
        include_delimiters=True,
        variable_form=None,
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


def test_array() -> None:
    """JSON5 array renders as a tuple in Python."""
    source = "[1, 2, 3,]"
    result = literalize(
        source=source,
        input_format=InputFormat.JSON5,
        language=PYTHON,
        pre_indent_level=0,
        include_delimiters=True,
        variable_form=None,
        error_on_coercion=False,
    )
    expected = textwrap.dedent(
        text="""\
        (
            1,
            2,
            3,
        )"""
    )
    assert result.code == expected


def test_unquoted_keys() -> None:
    """JSON5 unquoted keys are parsed correctly."""
    source = "{name: 'alice', age: 30}"
    result = literalize(
        source=source,
        input_format=InputFormat.JSON5,
        language=PYTHON,
        pre_indent_level=0,
        include_delimiters=True,
        variable_form=None,
        error_on_coercion=False,
    )
    expected = textwrap.dedent(
        text="""\
        {
            "name": "alice",
            "age": 30,
        }"""
    )
    assert result.code == expected


def test_single_quoted_strings() -> None:
    """JSON5 single-quoted strings are parsed correctly."""
    source = "{'key': 'value'}"
    result = literalize(
        source=source,
        input_format=InputFormat.JSON5,
        language=PYTHON,
        pre_indent_level=0,
        include_delimiters=True,
        variable_form=None,
        error_on_coercion=False,
    )
    expected = textwrap.dedent(
        text="""\
        {
            "key": "value",
        }"""
    )
    assert result.code == expected


def test_trailing_commas() -> None:
    """JSON5 trailing commas in objects are handled."""
    source = '{"a": 1, "b": 2,}'
    result = literalize(
        source=source,
        input_format=InputFormat.JSON5,
        language=PYTHON,
        pre_indent_level=0,
        include_delimiters=True,
        variable_form=None,
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


def test_comments_stripped() -> None:
    """JSON5 comments are stripped during parsing."""
    source = """\
{
    // This is a comment
    name: "alice",
    /* block comment */
    age: 30,
}"""
    result = literalize(
        source=source,
        input_format=InputFormat.JSON5,
        language=PYTHON,
        pre_indent_level=0,
        include_delimiters=True,
        variable_form=None,
        error_on_coercion=False,
    )
    expected = textwrap.dedent(
        text="""\
        {
            "name": "alice",
            "age": 30,
        }"""
    )
    assert result.code == expected


def test_null() -> None:
    """JSON5 null is parsed as None."""
    source = '{"key": null}'
    result = literalize(
        source=source,
        input_format=InputFormat.JSON5,
        language=PYTHON,
        pre_indent_level=0,
        include_delimiters=True,
        variable_form=None,
        error_on_coercion=False,
    )
    expected = textwrap.dedent(
        text="""\
        {
            "key": None,
        }"""
    )
    assert result.code == expected


def test_booleans() -> None:
    """JSON5 booleans are parsed correctly."""
    source = '{"enabled": true, "verbose": false}'
    result = literalize(
        source=source,
        input_format=InputFormat.JSON5,
        language=PYTHON,
        pre_indent_level=0,
        include_delimiters=True,
        variable_form=None,
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


def test_nested_objects() -> None:
    """JSON5 nested objects are parsed correctly."""
    source = '{server: {name: "test", port: 8080}}'
    result = literalize(
        source=source,
        input_format=InputFormat.JSON5,
        language=PYTHON,
        pre_indent_level=0,
        include_delimiters=True,
        variable_form=None,
        error_on_coercion=False,
    )
    expected = textwrap.dedent(
        text="""\
        {
            "server": {"name": "test", "port": 8080},
        }"""
    )
    assert result.code == expected


def test_invalid_json5() -> None:
    """Invalid JSON5 raises ``JSON5ParseError``."""
    with pytest.raises(expected_exception=JSON5ParseError):
        literalize(
            source="{invalid",
            input_format=InputFormat.JSON5,
            language=PYTHON,
            pre_indent_level=0,
            include_delimiters=False,
            variable_form=None,
            error_on_coercion=False,
        )


def test_invalid_json5_is_parse_error() -> None:
    """``JSON5ParseError`` is a subclass of ``ParseError``."""
    with pytest.raises(expected_exception=ParseError):
        literalize(
            source="{invalid",
            input_format=InputFormat.JSON5,
            language=PYTHON,
            pre_indent_level=0,
            include_delimiters=False,
            variable_form=None,
            error_on_coercion=False,
        )


def test_variable_declaration() -> None:
    """Variable name wraps the output in a declaration."""
    source = '{name: "alice"}'
    result = literalize(
        source=source,
        input_format=InputFormat.JSON5,
        language=JAVASCRIPT,
        pre_indent_level=0,
        include_delimiters=True,
        variable_form=NewVariable(name="config"),
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
    source = '{name: "alice"}'
    result = literalize(
        source=source,
        input_format=InputFormat.JSON5,
        language=PYTHON,
        pre_indent_level=0,
        include_delimiters=True,
        variable_form=ExistingVariable(name="config"),
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
    """JSON5 input renders correctly for Go."""
    source = '{name: "test", count: 42}'
    result = literalize(
        source=source,
        input_format=InputFormat.JSON5,
        language=GO,
        pre_indent_level=0,
        include_delimiters=True,
        variable_form=None,
        error_on_coercion=False,
    )
    expected = 'map[string]any{\n\t"name": "test",\n\t"count": 42,\n}'
    assert result.code == expected


@pytest.mark.parametrize(
    argnames=("source", "language", "expected"),
    argvalues=[
        ('{"v": 42}', PYTHON, '{\n    "v": 42,\n}'),
        ('{"v": 3.14}', PYTHON, '{\n    "v": 3.14,\n}'),
        ('{"v": "hello"}', PYTHON, '{\n    "v": "hello",\n}'),
        ('{"v": true}', PYTHON, '{\n    "v": True,\n}'),
        ('{"v": false}', PYTHON, '{\n    "v": False,\n}'),
        ('{"v": null}', PYTHON, '{\n    "v": None,\n}'),
    ],
)
def test_scalar_types(
    *, source: str, language: Language, expected: str
) -> None:
    """Various JSON5 scalar types render correctly."""
    result = literalize(
        source=source,
        input_format=InputFormat.JSON5,
        language=language,
        pre_indent_level=0,
        include_delimiters=True,
        variable_form=None,
        error_on_coercion=False,
    )
    assert result.code == expected


def test_scalar_string() -> None:
    """A bare JSON5 string renders as a scalar."""
    source = '"hello"'
    result = literalize(
        source=source,
        input_format=InputFormat.JSON5,
        language=PYTHON,
        pre_indent_level=0,
        include_delimiters=True,
        variable_form=None,
        error_on_coercion=False,
    )
    assert result.code == '"hello"'


def test_scalar_number() -> None:
    """A bare JSON5 number renders as a scalar."""
    source = "42"
    result = literalize(
        source=source,
        input_format=InputFormat.JSON5,
        language=PYTHON,
        pre_indent_level=0,
        include_delimiters=True,
        variable_form=None,
        error_on_coercion=False,
    )
    assert result.code == "42"
