"""Tests for literalizer JSON conversion."""

import json
import textwrap

import pytest

from literalizer import (
    Language,
    literalize_json,
)
from literalizer.exceptions import (
    HeterogeneousCoercionError,
    JSONParseError,
    ParseError,
)
from literalizer.languages import (
    Cpp,
    CSharp,
    Go,
    JavaScript,
    Mojo,
    Python,
    Ruby,
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
GO = Go(
    date_format=Go.DateFormat.ISO,
    datetime_format=Go.DatetimeFormat.ISO,
    sequence_format=Go.SequenceFormat.SLICE,
)
JAVASCRIPT = JavaScript(
    date_format=JavaScript.DateFormat.ISO,
    datetime_format=JavaScript.DatetimeFormat.ISO,
    sequence_format=JavaScript.SequenceFormat.ARRAY,
)
PYTHON = Python(
    date_format=Python.DateFormat.ISO,
    datetime_format=Python.DatetimeFormat.ISO,
    bytes_format=Python.BytesFormat.HEX,
    sequence_format=Python.SequenceFormat.TUPLE,
    set_format=Python.SetFormat.SET,
    variable_type_hints=Python.VariableTypeHints.NONE,
)
RUBY = Ruby(
    date_format=Ruby.DateFormat.ISO,
    datetime_format=Ruby.DatetimeFormat.ISO,
    sequence_format=Ruby.SequenceFormat.ARRAY,
)


def test_dict_python() -> None:
    """Python dict renders key-value pairs with a prefix."""
    data = {"user_1": "team_alpha", "user_2": "team_alpha"}
    result = literalize_json(
        json_string=json.dumps(obj=data),
        language=PYTHON,
        line_prefix="    ",
        indent="    ",
        wrap=False,
        variable_name=None,
        new_variable=True,
        error_on_coercion=False,
    )
    assert result == '    "user_1": "team_alpha",\n    "user_2": "team_alpha",'


def test_dict_wrap() -> None:
    """Wrapping a dict adds braces and indentation."""
    result = literalize_json(
        json_string=json.dumps(obj={"a": 1, "b": 2}),
        language=PYTHON,
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
            "a": 1,
            "b": 2,
        }"""
    )
    assert result == expected


@pytest.mark.parametrize(argnames="wrap", argvalues=[False, True])
def test_dict_empty(*, wrap: bool) -> None:
    """An empty dict produces an empty string regardless of wrap."""
    result = literalize_json(
        json_string=json.dumps(obj={}),
        language=PYTHON,
        line_prefix="",
        indent="    ",
        wrap=wrap,
        variable_name=None,
        new_variable=True,
        error_on_coercion=False,
    )
    assert result == ""


def test_integers() -> None:
    """Integer values are rendered literally."""
    result = literalize_json(
        json_string=json.dumps(obj=[42, 0, -7]),
        language=PYTHON,
        line_prefix="",
        indent="    ",
        wrap=False,
        variable_name=None,
        new_variable=True,
        error_on_coercion=False,
    )
    expected = textwrap.dedent(
        text="""\
        42,
        0,
        -7,"""
    )
    assert result == expected


def test_floats() -> None:
    """Float values are rendered literally."""
    result = literalize_json(
        json_string=json.dumps(obj=[1000.0, 3.14]),
        language=PYTHON,
        line_prefix="",
        indent="    ",
        wrap=False,
        variable_name=None,
        new_variable=True,
        error_on_coercion=False,
    )
    expected = textwrap.dedent(
        text="""\
        1000.0,
        3.14,"""
    )
    assert result == expected


def test_string_escaping() -> None:
    """Special characters in strings are properly escaped."""
    result = literalize_json(
        json_string=json.dumps(obj=['say "hi"', "a\\b", "line1\nline2"]),
        language=PYTHON,
        line_prefix="",
        indent="    ",
        wrap=False,
        variable_name=None,
        new_variable=True,
        error_on_coercion=False,
    )
    lines = result.split(sep="\n")
    assert lines[0] == '"say \\"hi\\"",'
    assert lines[1] == '"a\\\\b",'
    assert lines[2] == '"line1\\nline2",'


def test_nested_arrays() -> None:
    """Nested arrays are rendered recursively."""
    result = literalize_json(
        json_string=json.dumps(obj=[[[1, 2], [3, 4]]]),
        language=PYTHON,
        line_prefix="",
        indent="    ",
        wrap=False,
        variable_name=None,
        new_variable=True,
        error_on_coercion=False,
    )
    assert result == "((1, 2), (3, 4)),"


def test_dicts() -> None:
    """Dicts inside a list are rendered inline."""
    result = literalize_json(
        json_string=json.dumps(obj=[{"name": "alice", "age": 30}]),
        language=PYTHON,
        line_prefix="",
        indent="    ",
        wrap=False,
        variable_name=None,
        new_variable=True,
        error_on_coercion=False,
    )
    assert result == '{"name": "alice", "age": 30},'


def test_nested_dict_in_sequence() -> None:
    """A dict nested inside a sequence is rendered inline."""
    result = literalize_json(
        json_string=json.dumps(obj=[["a", {"x": 1}]]),
        language=PYTHON,
        line_prefix="",
        indent="    ",
        wrap=False,
        variable_name=None,
        new_variable=True,
        error_on_coercion=False,
    )
    assert result == '("a", {"x": 1}),'


def test_nested_sequence_in_dict() -> None:
    """A sequence nested inside a dict is rendered inline."""
    result = literalize_json(
        json_string=json.dumps(obj=[{"items": [1, 2]}]),
        language=PYTHON,
        line_prefix="",
        indent="    ",
        wrap=False,
        variable_name=None,
        new_variable=True,
        error_on_coercion=False,
    )
    assert result == '{"items": (1, 2)},'


def test_indent_spaces() -> None:
    """Space-based prefix is prepended to each line."""
    result = literalize_json(
        json_string=json.dumps(obj=[True, False]),
        language=PYTHON,
        line_prefix="        ",
        indent="    ",
        wrap=False,
        variable_name=None,
        new_variable=True,
        error_on_coercion=False,
    )
    assert result == "        True,\n        False,"


def test_indent_tabs() -> None:
    """Tab-based prefix is prepended to each line."""
    result = literalize_json(
        json_string=json.dumps(obj=[True, False]),
        language=GO,
        line_prefix="\t\t",
        indent="    ",
        wrap=False,
        variable_name=None,
        new_variable=True,
        error_on_coercion=False,
    )
    assert result == "\t\ttrue,\n\t\tfalse,"


def test_wrap() -> None:
    """Wrapping adds brackets and indentation."""
    result = literalize_json(
        json_string=json.dumps(obj=[True, False]),
        language=PYTHON,
        line_prefix="",
        indent="    ",
        wrap=True,
        variable_name=None,
        new_variable=True,
        error_on_coercion=False,
    )
    expected = textwrap.dedent(
        text="""\
        (
            True,
            False,
        )"""
    )
    assert result == expected


def test_wrap_with_line_prefix() -> None:
    """Wrapping respects the given line_prefix."""
    result = literalize_json(
        json_string=json.dumps(obj=[["a", 1.0]]),
        language=PYTHON,
        line_prefix="    ",
        indent="    ",
        wrap=True,
        variable_name=None,
        new_variable=True,
        error_on_coercion=False,
    )
    expected = '    (\n        ("a", 1.0),\n    )'
    assert result == expected


@pytest.mark.parametrize(argnames="wrap", argvalues=[False, True])
def test_empty_data(*, wrap: bool) -> None:
    """An empty list produces an empty string regardless of wrap."""
    result = literalize_json(
        json_string=json.dumps(obj=[]),
        language=PYTHON,
        line_prefix="",
        indent="    ",
        wrap=wrap,
        variable_name=None,
        new_variable=True,
        error_on_coercion=False,
    )
    assert result == ""


@pytest.mark.parametrize(
    argnames=("json_string", "language", "expected"),
    argvalues=[
        ("42", PYTHON, "42"),
        ("3.14", PYTHON, "3.14"),
        ('"hello"', PYTHON, '"hello"'),
        ("true", PYTHON, "True"),
        ("false", PYTHON, "False"),
        ("null", PYTHON, "None"),
        ("true", JAVASCRIPT, "true"),
        ("null", CSHARP, "(object?)null"),
        ("null", GO, "nil"),
        ("null", RUBY, "nil"),
        ("null", CPP, "nullptr"),
    ],
)
def test_scalar(
    *, json_string: str, language: Language, expected: str
) -> None:
    """Scalar values are formatted as native literals."""
    result = literalize_json(
        json_string=json_string,
        language=language,
        line_prefix="",
        indent="    ",
        wrap=False,
        variable_name=None,
        new_variable=True,
        error_on_coercion=False,
    )
    assert result == expected


def test_scalar_with_indent() -> None:
    """Scalar values respect the prefix parameter."""
    result = literalize_json(
        json_string="42",
        language=PYTHON,
        line_prefix="    ",
        indent="    ",
        wrap=False,
        variable_name=None,
        new_variable=True,
        error_on_coercion=False,
    )
    assert result == "    42"


def test_scalar_wrap_ignored() -> None:
    """Wrap is ignored for scalar values."""
    result = literalize_json(
        json_string="42",
        language=PYTHON,
        line_prefix="",
        indent="    ",
        wrap=True,
        variable_name=None,
        new_variable=True,
        error_on_coercion=False,
    )
    assert result == "42"


def test_literalize_json_array() -> None:
    """``literalize_json`` parses a JSON array string."""
    json_string = '[["user_1", 1000.0], ["user_2", 2000.0]]'
    result = literalize_json(
        json_string=json_string,
        language=PYTHON,
        line_prefix="    ",
        indent="    ",
        wrap=False,
        variable_name=None,
        new_variable=True,
        error_on_coercion=False,
    )
    expected = '    ("user_1", 1000.0),\n    ("user_2", 2000.0),'
    assert result == expected


def test_literalize_json_object() -> None:
    """``literalize_json`` parses a JSON object string."""
    json_string = '{"a": 1, "b": true}'
    result = literalize_json(
        json_string=json_string,
        language=PYTHON,
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
            "a": 1,
            "b": True,
        }"""
    )
    assert result == expected


def test_literalize_json_invalid() -> None:
    """``literalize_json`` raises on invalid JSON."""
    with pytest.raises(expected_exception=JSONParseError):
        literalize_json(
            json_string="not json",
            language=PYTHON,
            line_prefix="",
            indent="    ",
            wrap=False,
            variable_name=None,
            new_variable=True,
            error_on_coercion=False,
        )


def test_part1_sample_python() -> None:
    """Realistic test matching part1_sample_input.json structure."""
    data = [
        ["user_1", 1000.0],
        ["user_1", 1001.0],
        ["user_1", 1002.0],
        ["user_1", 1003.0],
    ]
    result = literalize_json(
        json_string=json.dumps(obj=data),
        language=PYTHON,
        line_prefix="        ",
        indent="    ",
        wrap=False,
        variable_name=None,
        new_variable=True,
        error_on_coercion=False,
    )
    expected_lines = [
        '        ("user_1", 1000.0),',
        '        ("user_1", 1001.0),',
        '        ("user_1", 1002.0),',
        '        ("user_1", 1003.0),',
    ]
    assert result.split(sep="\n") == expected_lines


def test_part2_sample_go() -> None:
    """Realistic test matching part2_sample_input.json structure."""
    data = [["user_1", 49, 1000.0], ["user_9", 10, 1003.0]]
    result = literalize_json(
        json_string=json.dumps(obj=data),
        language=GO,
        line_prefix="        ",
        indent="    ",
        wrap=False,
        variable_name=None,
        new_variable=True,
        error_on_coercion=False,
    )
    lines = result.split(sep="\n")
    assert lines[0] == '        []any{"user_1", 49, 1000.0},'
    assert lines[1] == '        []any{"user_9", 10, 1003.0},'


def test_literalize_json_invalid_is_parse_error() -> None:
    """``JSONParseError`` is a subclass of ``ParseError``."""
    with pytest.raises(expected_exception=ParseError):
        literalize_json(
            json_string="not json",
            language=PYTHON,
            line_prefix="",
            indent="    ",
            wrap=False,
            variable_name=None,
            new_variable=True,
            error_on_coercion=False,
        )


MOJO = Mojo(
    sequence_format=Mojo.SequenceFormat.LIST,
)


def test_error_on_coercion_json_raises() -> None:
    """Error_on_coercion raises for heterogeneous JSON arrays."""
    with pytest.raises(expected_exception=HeterogeneousCoercionError):
        literalize_json(
            json_string="[1, 2.5, 3]",
            language=MOJO,
            line_prefix="",
            indent="    ",
            wrap=True,
            variable_name=None,
            new_variable=True,
            error_on_coercion=True,
        )


def test_error_on_coercion_json_no_raise_homogeneous() -> None:
    """Error_on_coercion does not raise for homogeneous JSON arrays."""
    result = literalize_json(
        json_string="[1, 2, 3]",
        language=MOJO,
        line_prefix="",
        indent="    ",
        wrap=True,
        variable_name=None,
        new_variable=True,
        error_on_coercion=True,
    )
    expected = textwrap.dedent(
        text="""\
        [
            1,
            2,
            3,
        ]"""
    )
    assert result == expected
