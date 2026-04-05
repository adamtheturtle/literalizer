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
    InvalidDictKeyError,
    JSONParseError,
    ParseError,
)
from literalizer.languages import (
    Cpp,
    CSharp,
    Dhall,
    Go,
    JavaScript,
    Mojo,
    Python,
    R,
    Ruby,
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


def test_dict_python() -> None:
    """Python dict renders key-value pairs with a pre-indent level."""
    data = {"user_1": "team_alpha", "user_2": "team_alpha"}
    result = literalize_json(
        json_string=json.dumps(obj=data),
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
    result = literalize_json(
        json_string=json.dumps(obj={"a": 1, "b": 2}),
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


@pytest.mark.parametrize(
    argnames="include_delimiters",
    argvalues=[False, True],
)
def test_dict_empty(*, include_delimiters: bool) -> None:
    """An empty dict produces the language's empty-dict literal when
    delimiters are included, or an empty string without delimiters.
    """
    result = literalize_json(
        json_string=json.dumps(obj={}),
        language=PYTHON,
        pre_indent_level=0,
        include_delimiters=include_delimiters,
        variable_name=None,
        new_variable=True,
        error_on_coercion=False,
    )
    expected = "{}" if include_delimiters else ""
    assert result.code == expected


def test_integers() -> None:
    """Integer values are rendered literally."""
    result = literalize_json(
        json_string=json.dumps(obj=[42, 0, -7]),
        language=PYTHON,
        pre_indent_level=0,
        include_delimiters=False,
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
    assert result.code == expected


def test_floats() -> None:
    """Float values are rendered literally."""
    result = literalize_json(
        json_string=json.dumps(obj=[1000.0, 3.14]),
        language=PYTHON,
        pre_indent_level=0,
        include_delimiters=False,
        variable_name=None,
        new_variable=True,
        error_on_coercion=False,
    )
    expected = textwrap.dedent(
        text="""\
        1000.0,
        3.14,"""
    )
    assert result.code == expected


def test_string_escaping() -> None:
    """Special characters in strings are properly escaped."""
    result = literalize_json(
        json_string=json.dumps(obj=['say "hi"', "a\\b", "line1\nline2"]),
        language=PYTHON,
        pre_indent_level=0,
        include_delimiters=False,
        variable_name=None,
        new_variable=True,
        error_on_coercion=False,
    )
    lines = result.code.split(sep="\n")
    assert lines[0] == '"say \\"hi\\"",'
    assert lines[1] == '"a\\\\b",'
    assert lines[2] == '"line1\\nline2",'


def test_nested_arrays() -> None:
    """Nested arrays are rendered recursively."""
    result = literalize_json(
        json_string=json.dumps(obj=[[[1, 2], [3, 4]]]),
        language=PYTHON,
        pre_indent_level=0,
        include_delimiters=False,
        variable_name=None,
        new_variable=True,
        error_on_coercion=False,
    )
    assert result.code == "((1, 2), (3, 4)),"


def test_dicts() -> None:
    """Dicts inside a list are rendered inline."""
    result = literalize_json(
        json_string=json.dumps(obj=[{"name": "alice", "age": 30}]),
        language=PYTHON,
        pre_indent_level=0,
        include_delimiters=False,
        variable_name=None,
        new_variable=True,
        error_on_coercion=False,
    )
    assert result.code == '{"name": "alice", "age": 30},'


def test_nested_dict_in_sequence() -> None:
    """A dict nested inside a sequence is rendered inline."""
    result = literalize_json(
        json_string=json.dumps(obj=[["a", {"x": 1}]]),
        language=PYTHON,
        pre_indent_level=0,
        include_delimiters=False,
        variable_name=None,
        new_variable=True,
        error_on_coercion=False,
    )
    assert result.code == '("a", {"x": 1}),'


def test_nested_sequence_in_dict() -> None:
    """A sequence nested inside a dict is rendered inline."""
    result = literalize_json(
        json_string=json.dumps(obj=[{"items": [1, 2]}]),
        language=PYTHON,
        pre_indent_level=0,
        include_delimiters=False,
        variable_name=None,
        new_variable=True,
        error_on_coercion=False,
    )
    assert result.code == '{"items": (1, 2)},'


def test_indent_spaces() -> None:
    """Space-based prefix is prepended to each line."""
    result = literalize_json(
        json_string=json.dumps(obj=[True, False]),
        language=PYTHON,
        pre_indent_level=2,
        include_delimiters=False,
        variable_name=None,
        new_variable=True,
        error_on_coercion=False,
    )
    assert result.code == "        True,\n        False,"


def test_indent_tabs() -> None:
    """Pre-indent level is applied using the Go language indent."""
    result = literalize_json(
        json_string=json.dumps(obj=[True, False]),
        language=GO,
        pre_indent_level=2,
        include_delimiters=False,
        variable_name=None,
        new_variable=True,
        error_on_coercion=False,
    )
    assert result.code == "\t\ttrue,\n\t\tfalse,"


def test_include_delimiters() -> None:
    """Wrapping adds brackets and indentation."""
    result = literalize_json(
        json_string=json.dumps(obj=[True, False]),
        language=PYTHON,
        pre_indent_level=0,
        include_delimiters=True,
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
    assert result.code == expected


def test_include_delimiters_with_pre_indent_level() -> None:
    """Wrapping respects the given pre_indent_level."""
    result = literalize_json(
        json_string=json.dumps(obj=[["a", 1.0]]),
        language=PYTHON,
        pre_indent_level=1,
        include_delimiters=True,
        variable_name=None,
        new_variable=True,
        error_on_coercion=False,
    )
    expected = '    (\n        ("a", 1.0),\n    )'
    assert result.code == expected


def test_indent_override() -> None:
    """User-provided indent overrides the language default."""
    language = Python(
        date_format=Python.date_formats.PYTHON,
        datetime_format=Python.datetime_formats.PYTHON,
        bytes_format=Python.bytes_formats.HEX,
        sequence_format=Python.sequence_formats.TUPLE,
        set_format=Python.set_formats.SET,
        indent="\t",
    )
    result = literalize_json(
        json_string=json.dumps(obj=[True, False]),
        language=language,
        pre_indent_level=0,
        include_delimiters=True,
        variable_name=None,
        new_variable=True,
        error_on_coercion=False,
    )
    expected = "(\n\tTrue,\n\tFalse,\n)"
    assert result.code == expected


@pytest.mark.parametrize(
    argnames="include_delimiters",
    argvalues=[False, True],
)
def test_empty_data(*, include_delimiters: bool) -> None:
    """An empty list produces the language's empty-sequence literal when
    delimiters are included, or an empty string without delimiters.
    """
    result = literalize_json(
        json_string=json.dumps(obj=[]),
        language=PYTHON,
        pre_indent_level=0,
        include_delimiters=include_delimiters,
        variable_name=None,
        new_variable=True,
        error_on_coercion=False,
    )
    expected = "()" if include_delimiters else ""
    assert result.code == expected


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
        pre_indent_level=0,
        include_delimiters=False,
        variable_name=None,
        new_variable=True,
        error_on_coercion=False,
    )
    assert result.code == expected


def test_scalar_with_indent() -> None:
    """Scalar values respect the pre_indent_level parameter."""
    result = literalize_json(
        json_string="42",
        language=PYTHON,
        pre_indent_level=1,
        include_delimiters=False,
        variable_name=None,
        new_variable=True,
        error_on_coercion=False,
    )
    assert result.code == "    42"


def test_scalar_include_delimiters_ignored() -> None:
    """Wrap is ignored for scalar values."""
    result = literalize_json(
        json_string="42",
        language=PYTHON,
        pre_indent_level=0,
        include_delimiters=True,
        variable_name=None,
        new_variable=True,
        error_on_coercion=False,
    )
    assert result.code == "42"


def test_literalize_json_array() -> None:
    """``literalize_json`` parses a JSON array string."""
    json_string = '[["user_1", 1000.0], ["user_2", 2000.0]]'
    result = literalize_json(
        json_string=json_string,
        language=PYTHON,
        pre_indent_level=1,
        include_delimiters=False,
        variable_name=None,
        new_variable=True,
        error_on_coercion=False,
    )
    expected = '    ("user_1", 1000.0),\n    ("user_2", 2000.0),'
    assert result.code == expected


def test_literalize_json_object() -> None:
    """``literalize_json`` parses a JSON object string."""
    json_string = '{"a": 1, "b": true}'
    result = literalize_json(
        json_string=json_string,
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
            "b": True,
        }"""
    )
    assert result.code == expected


def test_literalize_json_invalid() -> None:
    """``literalize_json`` raises on invalid JSON."""
    with pytest.raises(expected_exception=JSONParseError):
        literalize_json(
            json_string="not json",
            language=PYTHON,
            pre_indent_level=0,
            include_delimiters=False,
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
        pre_indent_level=2,
        include_delimiters=False,
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
    assert result.code.split(sep="\n") == expected_lines


def test_part2_sample_go() -> None:
    """Realistic test matching part2_sample_input.json structure."""
    data = [["user_1", 49, 1000.0], ["user_9", 10, 1003.0]]
    result = literalize_json(
        json_string=json.dumps(obj=data),
        language=GO,
        pre_indent_level=2,
        include_delimiters=False,
        variable_name=None,
        new_variable=True,
        error_on_coercion=False,
    )
    lines = result.code.split(sep="\n")
    assert lines[0] == '\t\t[]any{"user_1", 49, 1000.0},'
    assert lines[1] == '\t\t[]any{"user_9", 10, 1003.0},'


def test_literalize_json_invalid_is_parse_error() -> None:
    """``JSONParseError`` is a subclass of ``ParseError``."""
    with pytest.raises(expected_exception=ParseError):
        literalize_json(
            json_string="not json",
            language=PYTHON,
            pre_indent_level=0,
            include_delimiters=False,
            variable_name=None,
            new_variable=True,
            error_on_coercion=False,
        )


MOJO = Mojo(
    date_format=Mojo.date_formats.ISO,
    datetime_format=Mojo.datetime_formats.ISO,
    bytes_format=Mojo.bytes_formats.HEX,
    sequence_format=Mojo.sequence_formats.LIST,
)


def test_error_on_coercion_json_raises() -> None:
    """Error_on_coercion raises for heterogeneous JSON arrays."""
    with pytest.raises(expected_exception=HeterogeneousCoercionError):
        literalize_json(
            json_string="[1, 2.5, 3]",
            language=MOJO,
            pre_indent_level=0,
            include_delimiters=True,
            variable_name=None,
            new_variable=True,
            error_on_coercion=True,
        )


def test_error_on_coercion_json_no_raise_homogeneous() -> None:
    """Error_on_coercion does not raise for homogeneous JSON arrays."""
    result = literalize_json(
        json_string="[1, 2, 3]",
        language=MOJO,
        pre_indent_level=0,
        include_delimiters=True,
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
    assert result.code == expected


def test_error_on_coercion_json_raises_sibling_lists() -> None:
    """Error_on_coercion raises for heterogeneous sibling sub-lists."""
    with pytest.raises(expected_exception=HeterogeneousCoercionError):
        literalize_json(
            json_string='[[1, 2], ["a", "b"]]',
            language=MOJO,
            pre_indent_level=0,
            include_delimiters=True,
            variable_name=None,
            new_variable=True,
            error_on_coercion=True,
        )


def test_error_on_coercion_json_raises_nested_sibling_lists() -> None:
    """Error_on_coercion raises for nested heterogeneous sibling
    sub-lists.
    """
    with pytest.raises(expected_exception=HeterogeneousCoercionError):
        literalize_json(
            json_string='[[[1, 2], ["a", "b"]]]',
            language=MOJO,
            pre_indent_level=0,
            include_delimiters=True,
            variable_name=None,
            new_variable=True,
            error_on_coercion=True,
        )


def test_cpp_array_null_list_fallback_json() -> None:
    """C++ ARRAY format falls back when schema type is not directly
    convertible (e.g. all-null list).
    """
    cpp_array = Cpp(sequence_format=Cpp.sequence_formats.ARRAY)
    result = literalize_json(
        json_string=json.dumps(obj=[None, None]),
        language=cpp_array,
        pre_indent_level=0,
        include_delimiters=True,
        variable_name=None,
        new_variable=True,
        error_on_coercion=False,
    )
    assert "nullptr" in result.code
    assert result.code.startswith("{")


def test_coerce_mixed_dict_values_none_with_list_json() -> None:
    """Dicts with None alongside a list are coerced to strings."""
    result = literalize_json(
        json_string=json.dumps(obj={"tags": ["admin"], "extra": None}),
        language=MOJO,
        pre_indent_level=0,
        include_delimiters=True,
        variable_name=None,
        new_variable=True,
        error_on_coercion=False,
    )
    expected = textwrap.dedent(
        text="""\
        {
            "tags": "[\\"admin\\"]",
            "extra": "None",
        }"""
    )
    assert result.code == expected


def test_coerce_mixed_dict_values_with_list_json() -> None:
    """Dicts with string and list values are coerced to all strings."""
    result = literalize_json(
        json_string=json.dumps(
            obj={"name": "Bob", "tags": ["admin", "user"]},
        ),
        language=MOJO,
        pre_indent_level=0,
        include_delimiters=True,
        variable_name=None,
        new_variable=True,
        error_on_coercion=False,
    )
    expected = textwrap.dedent(
        text="""\
        {
            "name": "Bob",
            "tags": "[\\"admin\\", \\"user\\"]",
        }"""
    )
    assert result.code == expected


def test_r_empty_dict_key_positional_json() -> None:
    """R with POSITIONAL empty_dict_key emits unnamed list elements."""
    spec = R(
        date_format=R.date_formats.R,
        datetime_format=R.datetime_formats.R,
        empty_dict_key=R.empty_dict_keys.POSITIONAL,
        bytes_format=R.bytes_formats.HEX,
        sequence_format=R.sequence_formats.LIST,
    )
    result = literalize_json(
        json_string=json.dumps(obj={"": "value"}),
        language=spec,
        pre_indent_level=0,
        include_delimiters=True,
        variable_name=None,
        new_variable=True,
        error_on_coercion=False,
    )
    expected = textwrap.dedent(
        text="""\
        list(
            "value"
        )"""
    )
    assert result.code == expected


def test_r_empty_dict_key_error_json() -> None:
    """R with ERROR empty_dict_key raises InvalidDictKeyError."""
    spec = R(
        date_format=R.date_formats.R,
        datetime_format=R.datetime_formats.R,
        empty_dict_key=R.empty_dict_keys.ERROR,
        bytes_format=R.bytes_formats.HEX,
        sequence_format=R.sequence_formats.LIST,
    )
    with pytest.raises(expected_exception=InvalidDictKeyError):
        literalize_json(
            json_string=json.dumps(obj={"": "value"}),
            language=spec,
            pre_indent_level=0,
            include_delimiters=True,
            variable_name=None,
            new_variable=True,
            error_on_coercion=False,
        )


def test_r_empty_dict_key_error_non_empty_key_ok_json() -> None:
    """R with ERROR empty_dict_key does not raise for non-empty keys."""
    spec = R(
        date_format=R.date_formats.R,
        datetime_format=R.datetime_formats.R,
        empty_dict_key=R.empty_dict_keys.ERROR,
        bytes_format=R.bytes_formats.HEX,
        sequence_format=R.sequence_formats.LIST,
    )
    result = literalize_json(
        json_string=json.dumps(obj={"key": "value"}),
        language=spec,
        pre_indent_level=0,
        include_delimiters=True,
        variable_name=None,
        new_variable=True,
        error_on_coercion=False,
    )
    expected = textwrap.dedent(
        text="""\
        list(
            "key" = "value"
        )"""
    )
    assert result.code == expected


def test_error_on_coercion_json_raises_for_heterogeneous_dict() -> None:
    """Error_on_coercion raises when dict values have mixed scalar
    types.
    """
    with pytest.raises(expected_exception=HeterogeneousCoercionError):
        literalize_json(
            json_string=json.dumps(obj={"a": 1, "b": 2.5}),
            language=MOJO,
            pre_indent_level=0,
            include_delimiters=True,
            variable_name=None,
            new_variable=True,
            error_on_coercion=True,
        )


def test_error_on_coercion_json_no_effect_without_coerce_flag() -> None:
    """Error_on_coercion has no effect when language doesn't coerce."""
    result = literalize_json(
        json_string=json.dumps(obj=[1, 2.5, 3]),
        language=PYTHON,
        pre_indent_level=0,
        include_delimiters=True,
        variable_name=None,
        new_variable=True,
        error_on_coercion=True,
    )
    expected = textwrap.dedent(
        text="""\
        (
            1,
            2.5,
            3,
        )"""
    )
    assert result.code == expected


def test_error_on_coercion_json_raises_for_nested_heterogeneous() -> None:
    """Error_on_coercion raises for heterogeneous data nested in a
    list.
    """
    with pytest.raises(expected_exception=HeterogeneousCoercionError):
        literalize_json(
            json_string=json.dumps(obj=[[1, "hello"]]),
            language=MOJO,
            pre_indent_level=0,
            include_delimiters=True,
            variable_name=None,
            new_variable=True,
            error_on_coercion=True,
        )


def test_error_on_coercion_json_no_raise_for_homogeneous_dict() -> None:
    """Error_on_coercion does not raise for homogeneous dict values."""
    result = literalize_json(
        json_string=json.dumps(obj={"a": 1, "b": 2}),
        language=MOJO,
        pre_indent_level=0,
        include_delimiters=True,
        variable_name=None,
        new_variable=True,
        error_on_coercion=True,
    )
    expected = textwrap.dedent(
        text="""\
        {
            "a": 1,
            "b": 2,
        }"""
    )
    assert result.code == expected


def test_error_on_coercion_json_raises_for_mixed_dict_values() -> None:
    """Error_on_coercion raises when a dict has values of mixed types."""
    with pytest.raises(expected_exception=HeterogeneousCoercionError):
        literalize_json(
            json_string=json.dumps(
                obj={"name": "Bob", "tags": ["admin", "user"]},
            ),
            language=MOJO,
            pre_indent_level=0,
            include_delimiters=True,
            variable_name=None,
            new_variable=True,
            error_on_coercion=True,
        )


def test_error_on_coercion_json_raises_for_mixed_list_values() -> None:
    """Error_on_coercion raises when a list has mixed element types."""
    with pytest.raises(expected_exception=HeterogeneousCoercionError):
        literalize_json(
            json_string=json.dumps(obj=["hello", ["nested"]]),
            language=MOJO,
            pre_indent_level=0,
            include_delimiters=True,
            variable_name=None,
            new_variable=True,
            error_on_coercion=True,
        )


def test_error_on_coercion_json_raises_for_mixed_dict_shapes() -> None:
    """Error_on_coercion raises when a list has dicts with different
    keys, including when the list is nested inside a dict.
    """
    data = {
        "items": [
            {"type": "create", "draft": True},
            {"type": "update"},
        ],
    }
    with pytest.raises(expected_exception=HeterogeneousCoercionError):
        literalize_json(
            json_string=json.dumps(obj=data),
            language=Dhall(),
            pre_indent_level=0,
            include_delimiters=True,
            variable_name=None,
            new_variable=True,
            error_on_coercion=True,
        )


def test_error_on_coercion_json_no_raise_for_uniform_dict_shapes() -> None:
    """Error_on_coercion does not raise when all dicts in a list have
    the same keys.
    """
    data = [
        {"type": "create", "name": "a"},
        {"type": "update", "name": "b"},
    ]
    literalize_json(
        json_string=json.dumps(obj=data),
        language=Dhall(),
        pre_indent_level=0,
        include_delimiters=True,
        variable_name=None,
        new_variable=True,
        error_on_coercion=True,
    )


def test_error_on_coercion_json_raises_for_mixed_dict_none_list() -> None:
    """Error_on_coercion raises when a dict has None alongside a list."""
    with pytest.raises(expected_exception=HeterogeneousCoercionError):
        literalize_json(
            json_string=json.dumps(
                obj={"tags": ["admin"], "extra": None},
            ),
            language=MOJO,
            pre_indent_level=0,
            include_delimiters=True,
            variable_name=None,
            new_variable=True,
            error_on_coercion=True,
        )


def test_dhall_empty_dict_key_error_json() -> None:
    """Dhall raises InvalidDictKeyError for empty-string dict keys."""
    with pytest.raises(expected_exception=InvalidDictKeyError):
        literalize_json(
            json_string=json.dumps(obj={"": "value"}),
            language=Dhall(),
            pre_indent_level=0,
            include_delimiters=True,
            variable_name=None,
            new_variable=True,
            error_on_coercion=False,
        )


def test_dhall_control_char_in_string_json() -> None:
    """Dhall escapes control characters using braced unicode escapes."""
    result = literalize_json(
        json_string=json.dumps(obj="\x01"),
        language=Dhall(),
        pre_indent_level=0,
        include_delimiters=True,
        variable_name="my_data",
        new_variable=True,
        error_on_coercion=False,
    )
    expected = 'let my_data = "\\u{0001}" in my_data'
    assert result.code == expected


def test_dhall_control_char_key_error_json() -> None:
    """Dhall rejects control characters in dict keys."""
    with pytest.raises(expected_exception=InvalidDictKeyError):
        literalize_json(
            json_string=json.dumps(obj={"\x01": "value"}),
            language=Dhall(),
            pre_indent_level=0,
            include_delimiters=True,
            variable_name=None,
            new_variable=True,
            error_on_coercion=False,
        )


def test_dhall_backtick_label_unescaping_json() -> None:
    """Dhall backtick labels contain raw content, not escape sequences."""
    result = literalize_json(
        json_string=json.dumps(obj={"$ref": "value"}),
        language=Dhall(),
        pre_indent_level=0,
        include_delimiters=True,
        variable_name="my_data",
        new_variable=True,
        error_on_coercion=False,
    )
    expected = textwrap.dedent(
        text="""\
        let my_data = {
          `$ref` = "value",
        } in my_data"""
    )
    assert result.code == expected
