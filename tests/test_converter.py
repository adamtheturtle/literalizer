"""Tests for literalizer converter."""

from __future__ import annotations

import ast
import datetime
import json
import textwrap
from collections.abc import Callable  # noqa: TC003
from typing import Any

import pytest
from hypothesis import given
from hypothesis import strategies as st

from literalizer import (
    CPP,
    CSHARP,
    GO,
    JAVA,
    JAVASCRIPT,
    KOTLIN,
    PYTHON,
    RUBY,
    TYPESCRIPT,
    Language,
    LanguageSpec,
    format_date_cpp,
    format_date_csharp,
    format_date_go,
    format_date_iso,
    format_date_java,
    format_date_js,
    format_date_kotlin,
    format_date_php,
    format_date_python,
    format_date_ruby,
    format_datetime_cpp,
    format_datetime_csharp,
    format_datetime_epoch,
    format_datetime_go,
    format_datetime_iso,
    format_datetime_java_instant,
    format_datetime_java_zoned,
    format_datetime_js,
    format_datetime_kotlin,
    format_datetime_php,
    format_datetime_python,
    format_datetime_ruby,
    literalize_json,
    literalize_yaml,
)
from literalizer.exceptions import JSONParseError, ParseError, YAMLParseError


@pytest.mark.parametrize(
    argnames=("language", "expected"),
    argvalues=[
        (PYTHON, '(True, None, "hi", (1, 2)),'),
        (JAVASCRIPT, '[true, null, "hi", [1, 2]],'),
        (TYPESCRIPT, '[true, null, "hi", [1, 2]],'),
        (GO, '[]any{true, nil, "hi", []any{1, 2}},'),
        (CPP, '{true, nullptr, "hi", {1, 2}},'),
        (JAVA, 'new Object[]{true, null, "hi", new Object[]{1, 2}}'),
        (CSHARP, '(true, (object?)null, "hi", (1, 2))'),
        (RUBY, '[true, nil, "hi", [1, 2]],'),
        (KOTLIN, 'listOf<Any?>(true, null, "hi", listOf<Any?>(1, 2)),'),
    ],
)
def test_language_list(*, language: Language, expected: str) -> None:
    """Each language produces the correct list literal."""
    result = literalize_json(
        json_string=json.dumps(obj=[[True, None, "hi", [1, 2]]]),
        language=language,
        prefix="",
        wrap=False,
    )
    assert result == expected


def test_ruby_dict() -> None:
    """Ruby dicts use => syntax and nil."""
    result = literalize_json(
        json_string=json.dumps(obj=[{"key": None}]),
        language=RUBY,
        prefix="",
        wrap=False,
    )
    assert result == '{"key" => nil},'


def test_dict_python() -> None:
    """Python dict renders key-value pairs with a prefix."""
    data = {"user_1": "team_alpha", "user_2": "team_alpha"}
    result = literalize_json(
        json_string=json.dumps(obj=data),
        language=PYTHON,
        prefix="    ",
        wrap=False,
    )
    assert result == '    "user_1": "team_alpha",\n    "user_2": "team_alpha",'


def test_dict_ruby() -> None:
    """Ruby dict renders with => syntax."""
    result = literalize_json(
        json_string=json.dumps(obj={"user_1": "team_alpha"}),
        language=RUBY,
        prefix="  ",
        wrap=False,
    )
    assert result == '  "user_1" => "team_alpha",'


def test_dict_wrap() -> None:
    """Wrapping a dict adds braces and indentation."""
    result = literalize_json(
        json_string=json.dumps(obj={"a": 1, "b": 2}),
        language=PYTHON,
        prefix="",
        wrap=True,
    )
    expected = textwrap.dedent(
        text="""\
        {
            "a": 1,
            "b": 2,
        }"""
    )
    assert result == expected


def test_java_dict_wrap_no_trailing_comma() -> None:
    """Java Map.ofEntries() must not have a trailing comma before the
    closing paren.
    """
    result = literalize_json(
        json_string=json.dumps(obj={"name": "Alice", "age": 30}),
        language=JAVA,
        prefix="",
        wrap=True,
    )
    expected = textwrap.dedent(
        text="""\
        Map.ofEntries(
            Map.entry("name", "Alice"),
            Map.entry("age", 30)
        )"""
    )
    assert result == expected


def test_java_list_wrap_uses_braces() -> None:
    """Java wrapped lists use ``new Object[]{…}``."""
    result = literalize_json(
        json_string=json.dumps(obj=[1, "hello", True]),
        language=JAVA,
        prefix="",
        wrap=True,
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


@pytest.mark.parametrize(argnames="wrap", argvalues=[False, True])
def test_dict_empty(wrap: bool) -> None:  # noqa: FBT001
    """An empty dict produces an empty string regardless of wrap."""
    result = literalize_json(
        json_string=json.dumps(obj={}), language=PYTHON, prefix="", wrap=wrap
    )
    assert result == ""


def test_integers() -> None:
    """Integer values are rendered literally."""
    result = literalize_json(
        json_string=json.dumps(obj=[42, 0, -7]),
        language=PYTHON,
        prefix="",
        wrap=False,
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
        prefix="",
        wrap=False,
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
        prefix="",
        wrap=False,
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
        prefix="",
        wrap=False,
    )
    assert result == "((1, 2), (3, 4)),"


def test_dicts() -> None:
    """Dicts inside a list are rendered inline."""
    result = literalize_json(
        json_string=json.dumps(obj=[{"name": "alice", "age": 30}]),
        language=PYTHON,
        prefix="",
        wrap=False,
    )
    assert result == '{"name": "alice", "age": 30},'


def test_nested_dict_in_list() -> None:
    """A dict nested inside a list is rendered inline."""
    result = literalize_json(
        json_string=json.dumps(obj=[["a", {"x": 1}]]),
        language=PYTHON,
        prefix="",
        wrap=False,
    )
    assert result == '("a", {"x": 1}),'


def test_nested_list_in_dict() -> None:
    """A list nested inside a dict is rendered inline."""
    result = literalize_json(
        json_string=json.dumps(obj=[{"items": [1, 2]}]),
        language=PYTHON,
        prefix="",
        wrap=False,
    )
    assert result == '{"items": (1, 2)},'


def test_prefix_spaces() -> None:
    """Space-based prefix is prepended to each line."""
    result = literalize_json(
        json_string=json.dumps(obj=[True, False]),
        language=PYTHON,
        prefix="        ",
        wrap=False,
    )
    assert result == "        True,\n        False,"


def test_prefix_tabs() -> None:
    """Tab-based prefix is prepended to each line."""
    result = literalize_json(
        json_string=json.dumps(obj=[True, False]),
        language=GO,
        prefix="\t\t",
        wrap=False,
    )
    assert result == "\t\ttrue,\n\t\tfalse,"


def test_wrap() -> None:
    """Wrapping adds brackets and indentation."""
    result = literalize_json(
        json_string=json.dumps(obj=[True, False]),
        language=PYTHON,
        prefix="",
        wrap=True,
    )
    expected = textwrap.dedent(
        text="""\
        (
            True,
            False,
        )"""
    )
    assert result == expected


def test_wrap_with_prefix() -> None:
    """Wrapping respects the given prefix."""
    result = literalize_json(
        json_string=json.dumps(obj=[["a", 1.0]]),
        language=PYTHON,
        prefix="    ",
        wrap=True,
    )
    expected = textwrap.dedent(
        text="""\
        (
            ("a", 1.0),
        )"""
    )
    assert result == expected


@pytest.mark.parametrize(argnames="wrap", argvalues=[False, True])
def test_empty_data(wrap: bool) -> None:  # noqa: FBT001
    """An empty list produces an empty string regardless of wrap."""
    result = literalize_json(
        json_string=json.dumps(obj=[]), language=PYTHON, prefix="", wrap=wrap
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
        json_string=json_string, language=language, prefix="", wrap=False
    )
    assert result == expected


def test_scalar_with_prefix() -> None:
    """Scalar values respect the prefix parameter."""
    result = literalize_json(
        json_string="42", language=PYTHON, prefix="    ", wrap=False
    )
    assert result == "    42"


def test_scalar_wrap_ignored() -> None:
    """Wrap is ignored for scalar values."""
    result = literalize_json(
        json_string="42", language=PYTHON, prefix="", wrap=True
    )
    assert result == "42"


def test_custom_language() -> None:
    """A custom LanguageSpec works as a language."""
    custom = LanguageSpec(
        null_literal="NIL",
        true_literal="YES",
        false_literal="NO",
        collection_open="<",
        collection_close=">",
        dict_separator=" -> ",
        dict_open="{",
        dict_close="}",
        format_dict_entry=None,
        trailing_comma=True,
        single_element_trailing_comma=False,
        format_date=format_date_iso,
        format_datetime=format_datetime_iso,
        empty_collection=None,
        set_open="<",
        set_close=">",
        empty_set=None,
        format_set_entry=None,
        comment_prefix="//",
    )
    result = literalize_json(
        json_string=json.dumps(obj=[True, None, "hi"]),
        language=custom,
        prefix="",
        wrap=False,
    )
    assert result == 'YES,\nNIL,\n"hi",'


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
        prefix="        ",
        wrap=False,
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
        prefix="        ",
        wrap=False,
    )
    lines = result.split(sep="\n")
    assert lines[0] == '        []any{"user_1", 49, 1000.0},'
    assert lines[1] == '        []any{"user_9", 10, 1003.0},'


type _JSONScalar = str | int | float | bool | None

type _JSONValue = _JSONScalar | list[_JSONValue] | dict[str, _JSONValue]


def _lists_to_tuples(*, value: _JSONValue) -> object:
    """Recursively convert lists to tuples to match Python converter
    output.
    """
    if isinstance(value, list):
        return tuple(_lists_to_tuples(value=v) for v in value)
    if isinstance(value, dict):
        return {k: _lists_to_tuples(value=v) for k, v in value.items()}
    return value


json_text = st.text(
    alphabet=st.characters(
        categories=("L", "M", "N", "P", "S", "Z"), exclude_characters="\x00"
    )
)
json_scalars = (
    st.none()
    | st.booleans()
    | st.integers()
    | st.floats(allow_nan=False, allow_infinity=False)
    | json_text
)
json_values: st.SearchStrategy[Any] = st.recursive(
    base=json_scalars,
    extend=lambda children: (
        st.lists(elements=children)
        | st.dictionaries(keys=json_text, values=children)
    ),
)
json_arrays = st.lists(elements=json_values, max_size=10)
json_objects = st.dictionaries(keys=json_text, values=json_values, max_size=10)


def test_literalize_json_array() -> None:
    """``literalize_json`` parses a JSON array string."""
    json_string = '[["user_1", 1000.0], ["user_2", 2000.0]]'
    result = literalize_json(
        json_string=json_string,
        language=PYTHON,
        prefix="    ",
        wrap=False,
    )
    expected = '    ("user_1", 1000.0),\n    ("user_2", 2000.0),'
    assert result == expected


def test_literalize_json_object() -> None:
    """``literalize_json`` parses a JSON object string."""
    json_string = '{"a": 1, "b": true}'
    result = literalize_json(
        json_string=json_string,
        language=PYTHON,
        prefix="",
        wrap=True,
    )
    expected = '{\n    "a": 1,\n    "b": True,\n}'
    assert result == expected


def test_literalize_json_invalid() -> None:
    """``literalize_json`` raises on invalid JSON."""
    with pytest.raises(expected_exception=JSONParseError):
        literalize_json(
            json_string="not json",
            language=PYTHON,
            prefix="",
            wrap=False,
        )


def test_literalize_json_invalid_is_parse_error() -> None:
    """``JSONParseError`` is a subclass of ``ParseError``."""
    with pytest.raises(expected_exception=ParseError):
        literalize_json(
            json_string="not json",
            language=PYTHON,
            prefix="",
            wrap=False,
        )


@given(data=json_arrays)
def test_roundtrip_array(data: list[Any]) -> None:
    """JSON array -> Python literal -> ast.literal_eval round-trips."""
    result = literalize_json(
        json_string=json.dumps(obj=data),
        language=PYTHON,
        prefix="",
        wrap=True,
    )
    if not data:
        assert result == ""
        return
    parsed = ast.literal_eval(node_or_string=result)
    assert parsed == tuple(_lists_to_tuples(value=v) for v in data)


@given(data=json_scalars)
def test_roundtrip_scalar(data: _JSONScalar) -> None:
    """Scalar -> Python literal -> ast.literal_eval round-trips."""
    result = literalize_json(
        json_string=json.dumps(obj=data),
        language=PYTHON,
        prefix="",
        wrap=False,
    )
    parsed = ast.literal_eval(node_or_string=result)
    assert parsed == data


@given(data=json_objects)
def test_roundtrip_dict(data: dict[str, Any]) -> None:
    """JSON object -> Python literal -> ast.literal_eval round-trips."""
    result = literalize_json(
        json_string=json.dumps(obj=data),
        language=PYTHON,
        prefix="",
        wrap=True,
    )
    if not data:
        assert result == ""
        return
    parsed = ast.literal_eval(node_or_string=result)
    assert parsed == _lists_to_tuples(value=data)


def test_literalize_yaml_empty_sequence() -> None:
    """An empty YAML sequence produces an empty string."""
    result = literalize_yaml(
        yaml_string="[]\n",
        language=PYTHON,
        prefix="",
        wrap=True,
    )
    assert result == ""


def test_literalize_yaml_sequence() -> None:
    """``literalize_yaml`` parses a YAML sequence string."""
    yaml_string = "- [user_1, 1000.0]\n- [user_2, 2000.0]\n"
    result = literalize_yaml(
        yaml_string=yaml_string,
        language=PYTHON,
        prefix="    ",
        wrap=False,
    )
    expected = '    ("user_1", 1000.0),\n    ("user_2", 2000.0),'
    assert result == expected


def test_literalize_yaml_mapping() -> None:
    """``literalize_yaml`` parses a YAML mapping string."""
    yaml_string = "a: 1\nb: true\n"
    result = literalize_yaml(
        yaml_string=yaml_string,
        language=PYTHON,
        prefix="",
        wrap=True,
    )
    expected = '{\n    "a": 1,\n    "b": True,\n}'
    assert result == expected


def test_literalize_yaml_invalid() -> None:
    """``literalize_yaml`` raises on invalid YAML."""
    with pytest.raises(expected_exception=YAMLParseError):
        literalize_yaml(
            yaml_string=":\n  :\n    - ][",
            language=PYTHON,
            prefix="",
            wrap=False,
        )


def test_literalize_yaml_invalid_is_parse_error() -> None:
    """``YAMLParseError`` is a subclass of ``ParseError``."""
    with pytest.raises(expected_exception=ParseError):
        literalize_yaml(
            yaml_string=":\n  :\n    - ][",
            language=PYTHON,
            prefix="",
            wrap=False,
        )


@pytest.mark.parametrize(
    argnames=("yaml_string", "language", "expected"),
    argvalues=[
        ("42", PYTHON, "42"),
        ("3.14", PYTHON, "3.14"),
        ("hello", PYTHON, '"hello"'),
        ("true", PYTHON, "True"),
        ("false", PYTHON, "False"),
        ("null", PYTHON, "None"),
        ("true", JAVASCRIPT, "true"),
        ("null", GO, "nil"),
    ],
)
def test_literalize_yaml_scalar(
    *,
    yaml_string: str,
    language: Language,
    expected: str,
) -> None:
    """``literalize_yaml`` handles scalar YAML values."""
    result = literalize_yaml(
        yaml_string=yaml_string,
        language=language,
        prefix="",
        wrap=False,
    )
    assert result == expected


def test_literalize_yaml_date() -> None:
    """``literalize_yaml`` formats date values as ISO string literals."""
    yaml_string = "- 2024-01-15\n"
    result = literalize_yaml(
        yaml_string=yaml_string,
        language=PYTHON,
        prefix="",
        wrap=False,
    )
    assert result == '"2024-01-15",'


def test_literalize_yaml_datetime() -> None:
    """``literalize_yaml`` formats datetime values as ISO string
    literals.
    """
    yaml_string = "- 2024-01-15T12:30:00\n"
    result = literalize_yaml(
        yaml_string=yaml_string,
        language=PYTHON,
        prefix="",
        wrap=False,
    )
    assert result == '"2024-01-15T12:30:00",'


_SAMPLE_DATE = datetime.date(year=2024, month=1, day=15)
_SAMPLE_DATETIME = datetime.datetime.fromisoformat("2024-01-15T12:30:00")
_SAMPLE_DATETIME_MICRO = datetime.datetime.fromisoformat(
    "2024-01-15T12:30:00.123456"
)


@pytest.mark.parametrize(
    argnames=("func", "value", "expected"),
    argvalues=[
        pytest.param(
            format_date_iso,
            _SAMPLE_DATE,
            '"2024-01-15"',
            id="format_date_iso",
        ),
        pytest.param(
            format_datetime_iso,
            _SAMPLE_DATETIME,
            '"2024-01-15T12:30:00"',
            id="format_datetime_iso",
        ),
        pytest.param(
            format_date_python,
            _SAMPLE_DATE,
            "datetime.date(2024, 1, 15)",
            id="format_date_python",
        ),
        pytest.param(
            format_datetime_python,
            _SAMPLE_DATETIME,
            "datetime.datetime(2024, 1, 15, 12, 30, 0)",
            id="format_datetime_python",
        ),
        pytest.param(
            format_datetime_python,
            _SAMPLE_DATETIME_MICRO,
            "datetime.datetime(2024, 1, 15, 12, 30, 0, 123456)",
            id="format_datetime_python_microsecond",
        ),
        pytest.param(
            format_date_java,
            _SAMPLE_DATE,
            "LocalDate.of(2024, 1, 15)",
            id="format_date_java",
        ),
        pytest.param(
            format_datetime_java_instant,
            _SAMPLE_DATETIME,
            'Instant.parse("2024-01-15T12:30:00")',
            id="format_datetime_java_instant",
        ),
        pytest.param(
            format_datetime_java_zoned,
            _SAMPLE_DATETIME,
            'ZonedDateTime.of(2024, 1, 15, 12, 30, 0, 0, ZoneId.of("UTC"))',
            id="format_datetime_java_zoned",
        ),
        pytest.param(
            format_date_ruby,
            _SAMPLE_DATE,
            "Date.new(2024, 1, 15)",
            id="format_date_ruby",
        ),
        pytest.param(
            format_datetime_ruby,
            _SAMPLE_DATETIME,
            "Time.new(2024, 1, 15, 12, 30, 0)",
            id="format_datetime_ruby",
        ),
        pytest.param(
            format_date_js,
            _SAMPLE_DATE,
            'new Date("2024-01-15")',
            id="format_date_js",
        ),
        pytest.param(
            format_datetime_js,
            _SAMPLE_DATETIME,
            'new Date("2024-01-15T12:30:00")',
            id="format_datetime_js",
        ),
        pytest.param(
            format_date_csharp,
            _SAMPLE_DATE,
            "new DateOnly(2024, 1, 15)",
            id="format_date_csharp",
        ),
        pytest.param(
            format_datetime_csharp,
            _SAMPLE_DATETIME,
            "new DateTime(2024, 1, 15, 12, 30, 0)",
            id="format_datetime_csharp",
        ),
        pytest.param(
            format_date_go,
            _SAMPLE_DATE,
            "time.Date(2024, time.January, 15, 0, 0, 0, 0, time.UTC)",
            id="format_date_go",
        ),
        pytest.param(
            format_datetime_go,
            _SAMPLE_DATETIME,
            "time.Date(2024, time.January, 15, 12, 30, 0, 0, time.UTC)",
            id="format_datetime_go",
        ),
        pytest.param(
            format_date_kotlin,
            _SAMPLE_DATE,
            "LocalDate.of(2024, 1, 15)",
            id="format_date_kotlin",
        ),
        pytest.param(
            format_datetime_kotlin,
            _SAMPLE_DATETIME,
            "LocalDateTime.of(2024, 1, 15, 12, 30, 0)",
            id="format_datetime_kotlin",
        ),
        pytest.param(
            format_date_php,
            _SAMPLE_DATE,
            'new DateTime("2024-01-15")',
            id="format_date_php",
        ),
        pytest.param(
            format_datetime_php,
            _SAMPLE_DATETIME,
            'new DateTime("2024-01-15T12:30:00")',
            id="format_datetime_php",
        ),
    ],
)
def test_format_date_datetime(
    func: Callable[..., str],
    value: datetime.date | datetime.datetime,
    expected: str,
) -> None:
    """Each format function returns the expected string."""
    assert func(value=value) == expected


def test_format_datetime_epoch() -> None:
    """``format_datetime_epoch`` returns a numeric timestamp."""
    result = format_datetime_epoch(value=_SAMPLE_DATETIME)
    # The exact value depends on local timezone for naive datetimes,
    # so just check it parses as a float.
    float(result)


def test_format_date_cpp() -> None:
    """``format_date_cpp`` returns a year_month_day literal."""
    result = format_date_cpp(value=_SAMPLE_DATE)
    assert "std::chrono::year{2024}" in result
    assert "std::chrono::month{1}" in result
    assert "std::chrono::day{15}" in result


def test_format_datetime_cpp() -> None:
    """``format_datetime_cpp`` returns a sys_days expression."""
    result = format_datetime_cpp(value=_SAMPLE_DATETIME)
    assert "std::chrono::sys_days" in result
    assert "std::chrono::hours{12}" in result
    assert "std::chrono::minutes{30}" in result


def test_format_datetime_cpp_midnight() -> None:
    """``format_datetime_cpp`` at midnight omits zero time components."""
    midnight = datetime.datetime.fromisoformat("2024-01-15T00:00:00")
    result = format_datetime_cpp(value=midnight)
    assert "std::chrono::sys_days" in result
    assert "hours" not in result
    assert "minutes" not in result
    assert "seconds" not in result
    assert "microseconds" not in result


def test_format_datetime_cpp_seconds_and_microseconds() -> None:
    """``format_datetime_cpp`` includes seconds and microseconds."""
    dt = datetime.datetime.fromisoformat("2024-01-15T12:30:45.123456")
    result = format_datetime_cpp(value=dt)
    assert "std::chrono::seconds{45}" in result
    assert "std::chrono::microseconds{123456}" in result


def test_custom_format_date() -> None:
    """A custom format_date callable is used for date values."""
    spec = LanguageSpec(
        null_literal="None",
        true_literal="True",
        false_literal="False",
        collection_open="(",
        collection_close=")",
        dict_separator=": ",
        dict_open="{",
        dict_close="}",
        format_dict_entry=None,
        trailing_comma=True,
        single_element_trailing_comma=False,
        format_date=format_date_python,
        format_datetime=format_datetime_iso,
        empty_collection=None,
        set_open="{",
        set_close="}",
        empty_set="set()",
        format_set_entry=None,
        comment_prefix="//",
    )
    result = literalize_yaml(
        yaml_string="- 2024-01-15\n",
        language=spec,
        prefix="",
        wrap=False,
    )
    assert result == "datetime.date(2024, 1, 15),"


def test_custom_format_datetime() -> None:
    """A custom format_datetime callable is used for datetime values."""
    spec = LanguageSpec(
        null_literal="None",
        true_literal="True",
        false_literal="False",
        collection_open="(",
        collection_close=")",
        dict_separator=": ",
        dict_open="{",
        dict_close="}",
        format_dict_entry=None,
        trailing_comma=True,
        single_element_trailing_comma=False,
        format_date=format_date_iso,
        format_datetime=format_datetime_python,
        empty_collection=None,
        set_open="{",
        set_close="}",
        empty_set="set()",
        format_set_entry=None,
        comment_prefix="//",
    )
    result = literalize_yaml(
        yaml_string="- 2024-01-15T12:30:00\n",
        language=spec,
        prefix="",
        wrap=False,
    )
    assert result == "datetime.datetime(2024, 1, 15, 12, 30, 0),"


def test_java_native_dates() -> None:
    """Java language spec with native date formatting."""
    spec = LanguageSpec(
        null_literal="null",
        true_literal="true",
        false_literal="false",
        collection_open="{",
        collection_close="}",
        dict_separator=": ",
        dict_open="{",
        dict_close="}",
        format_dict_entry=None,
        trailing_comma=True,
        single_element_trailing_comma=False,
        format_date=format_date_java,
        format_datetime=format_datetime_java_instant,
        empty_collection=None,
        set_open="Set.of(",
        set_close=")",
        empty_set=None,
        format_set_entry=None,
        comment_prefix="//",
    )
    result = literalize_yaml(
        yaml_string="- 2024-01-15\n- 2024-01-15T12:30:00\n",
        language=spec,
        prefix="",
        wrap=False,
    )
    lines = result.split(sep="\n")
    assert lines[0] == "LocalDate.of(2024, 1, 15),"
    assert lines[1] == 'Instant.parse("2024-01-15T12:30:00"),'


def test_ruby_native_dates() -> None:
    """Ruby language spec with native date formatting."""
    spec = LanguageSpec(
        null_literal="nil",
        true_literal="true",
        false_literal="false",
        collection_open="[",
        collection_close="]",
        dict_separator=" => ",
        dict_open="{",
        dict_close="}",
        format_dict_entry=None,
        trailing_comma=True,
        single_element_trailing_comma=False,
        format_date=format_date_ruby,
        format_datetime=format_datetime_ruby,
        empty_collection=None,
        set_open="Set.new([",
        set_close="])",
        empty_set="Set.new",
        format_set_entry=None,
        comment_prefix="#",
    )
    result = literalize_yaml(
        yaml_string="- 2024-01-15T12:30:00\n",
        language=spec,
        prefix="",
        wrap=False,
    )
    assert result == "Time.new(2024, 1, 15, 12, 30, 0),"


def test_yaml_set_inline_in_list() -> None:
    """A !!set nested in a list is formatted inline using set
    delimiters.
    """
    result = literalize_yaml(
        yaml_string="- !!set\n  ? a\n  ? b\n",
        language=PYTHON,
        prefix="",
        wrap=False,
    )
    assert result == '{"a", "b"},'


def test_yaml_set_inline_with_format_set_entry() -> None:
    """A !!set nested in a list uses format_set_entry when provided."""
    result = literalize_yaml(
        yaml_string="- !!set\n  ? a\n",
        language=GO,
        prefix="",
        wrap=False,
    )
    assert result == 'map[any]struct{}{"a": struct{}{}},'


def test_yaml_empty_set_inline() -> None:
    """An empty !!set nested in a list uses empty_set override."""
    result = literalize_yaml(
        yaml_string="- !!set {}\n",
        language=PYTHON,
        prefix="",
        wrap=False,
    )
    assert result == "set(),"


def test_default_format_date_is_iso() -> None:
    """The default format_date is ISO format."""
    assert PYTHON.format_date is format_date_iso
    assert JAVA.format_date is format_date_iso


def test_default_format_datetime_is_iso() -> None:
    """The default format_datetime is ISO format."""
    assert PYTHON.format_datetime is format_datetime_iso
    assert JAVA.format_datetime is format_datetime_iso


def test_yaml_comment_sequence_before() -> None:
    """Full-line comments before sequence items are preserved."""
    yaml_string = "# first\n- a\n# second\n- b\n"
    result = literalize_yaml(
        yaml_string=yaml_string,
        language=PYTHON,
        prefix="",
        wrap=True,
    )
    expected = textwrap.dedent(
        text="""\
        (
            # first
            "a",
            # second
            "b",
        )"""
    )
    assert result == expected


def test_yaml_comment_sequence_inline() -> None:
    """Inline comments on sequence items are preserved."""
    yaml_string = "- a  # note a\n- b  # note b\n"
    result = literalize_yaml(
        yaml_string=yaml_string,
        language=PYTHON,
        prefix="",
        wrap=True,
    )
    expected = textwrap.dedent(
        text="""\
        (
            "a",  # note a
            "b",  # note b
        )"""
    )
    assert result == expected


def test_yaml_comment_mapping() -> None:
    """Comments in mappings are preserved."""
    yaml_string = "# comment for a\na: 1  # inline a\n# comment for b\nb: 2\n"
    result = literalize_yaml(
        yaml_string=yaml_string,
        language=PYTHON,
        prefix="",
        wrap=True,
    )
    expected = textwrap.dedent(
        text="""\
        {
            # comment for a
            "a": 1,  # inline a
            # comment for b
            "b": 2,
        }"""
    )
    assert result == expected


def test_yaml_comment_javascript_prefix() -> None:
    """Comments use the target language's comment prefix."""
    yaml_string = "# comment\n- a\n"
    result = literalize_yaml(
        yaml_string=yaml_string,
        language=JAVASCRIPT,
        prefix="",
        wrap=True,
    )
    expected = textwrap.dedent(
        text="""\
        [
            // comment
            "a",
        ]"""
    )
    assert result == expected


def test_yaml_comment_trailing() -> None:
    """Trailing comments after the last element are preserved."""
    yaml_string = "- a\n# trailing\n"
    result = literalize_yaml(
        yaml_string=yaml_string,
        language=PYTHON,
        prefix="",
        wrap=True,
    )
    expected = textwrap.dedent(
        text="""\
        (
            "a",
            # trailing
        )"""
    )
    assert result == expected


def test_yaml_comment_no_wrap() -> None:
    """Comments work with wrap=False."""
    yaml_string = "# comment\n- a\n- b\n"
    result = literalize_yaml(
        yaml_string=yaml_string,
        language=PYTHON,
        prefix="    ",
        wrap=False,
    )
    expected = '    # comment\n    "a",\n    "b",'
    assert result == expected


def test_yaml_comment_scalar() -> None:
    """Comments on scalar YAML values are preserved."""
    yaml_string = "# note\n42\n"
    result = literalize_yaml(
        yaml_string=yaml_string,
        language=PYTHON,
        prefix="",
        wrap=False,
    )
    expected = "# note\n42"
    assert result == expected


def test_yaml_comment_scalar_inline() -> None:
    """Inline comments on scalar YAML values are preserved."""
    yaml_string = "42  # note\n"
    result = literalize_yaml(
        yaml_string=yaml_string,
        language=PYTHON,
        prefix="",
        wrap=False,
    )
    expected = "42  # note"
    assert result == expected


def test_yaml_no_comments_unchanged() -> None:
    """YAML without comments produces the same output as before."""
    yaml_string = "- a\n- b\n"
    result = literalize_yaml(
        yaml_string=yaml_string,
        language=PYTHON,
        prefix="",
        wrap=True,
    )
    expected = textwrap.dedent(
        text="""\
        (
            "a",
            "b",
        )"""
    )
    assert result == expected


def test_yaml_comment_multiple_before_lines() -> None:
    """Multiple comment lines before an element are all preserved."""
    yaml_string = "# line 1\n# line 2\n- a\n"
    result = literalize_yaml(
        yaml_string=yaml_string,
        language=PYTHON,
        prefix="",
        wrap=True,
    )
    expected = textwrap.dedent(
        text="""\
        (
            # line 1
            # line 2
            "a",
        )"""
    )
    assert result == expected


@pytest.mark.parametrize(
    argnames=("language", "expected"),
    argvalues=[
        (PYTHON, "#"),
        (RUBY, "#"),
        (JAVASCRIPT, "//"),
        (GO, "//"),
    ],
)
def test_comment_prefix(language: LanguageSpec, expected: str) -> None:
    """Each language has the expected comment prefix."""
    assert language.comment_prefix == expected


def test_yaml_comment_escaped_quote_in_value() -> None:
    """Escaped quotes do not end the quoted context."""
    yaml_string = 'key: "value \\" # not a comment" # real\n'
    result = literalize_yaml(
        yaml_string=yaml_string,
        language=PYTHON,
        prefix="",
        wrap=True,
    )
    expected = textwrap.dedent(
        text="""\
        {
            "key": "value \\" # not a comment",  # real
        }"""
    )
    assert result == expected


def test_yaml_comment_scalar_quoted_with_hash() -> None:
    """Inline comment after a quoted scalar containing ``#``."""
    yaml_string = '"hello # world"  # note\n'
    result = literalize_yaml(
        yaml_string=yaml_string,
        language=PYTHON,
        prefix="",
        wrap=False,
    )
    expected = '"hello # world"  # note'
    assert result == expected


def test_yaml_comment_double_hash() -> None:
    """Double-hash comments preserve the extra ``#``."""
    yaml_string = "## section\n- a\n"
    result = literalize_yaml(
        yaml_string=yaml_string,
        language=PYTHON,
        prefix="",
        wrap=True,
    )
    expected = textwrap.dedent(
        text="""\
        (
            # # section
            "a",
        )"""
    )
    assert result == expected


def test_yaml_comment_block_scalar_not_extracted() -> None:
    """Text inside a block scalar is not mistaken for a comment."""
    yaml_string = "description: |\n  # not a comment\nname: foo\n"
    result = literalize_yaml(
        yaml_string=yaml_string,
        language=PYTHON,
        prefix="",
        wrap=True,
    )
    expected = textwrap.dedent(
        text="""\
        {
            "description": "# not a comment\\n",
            "name": "foo",
        }"""
    )
    assert result == expected


def test_yaml_comment_scalar_with_document_markers() -> None:
    """Document markers ``---`` and ``...`` are ignored in scalars."""
    yaml_string = "---\n# note\n42\n...\n"
    result = literalize_yaml(
        yaml_string=yaml_string,
        language=PYTHON,
        prefix="",
        wrap=True,
    )
    expected = "# note\n42"
    assert result == expected


def test_yaml_comment_empty_comment_line() -> None:
    """A bare ``#`` with no text produces a prefix-only comment."""
    yaml_string = "- a\n#\n- b\n"
    result = literalize_yaml(
        yaml_string=yaml_string,
        language=PYTHON,
        prefix="",
        wrap=True,
    )
    expected = textwrap.dedent(
        text="""\
        (
            "a",
            #
            "b",
        )"""
    )
    assert result == expected


def test_yaml_comment_more_body_lines_than_comments() -> None:
    """Body lines beyond the number of comments are emitted plain."""
    yaml_string = "- a\n- b\n- c\n"
    result = literalize_yaml(
        yaml_string=yaml_string,
        language=PYTHON,
        prefix="",
        wrap=True,
    )
    expected = textwrap.dedent(
        text="""\
        (
            "a",
            "b",
            "c",
        )"""
    )
    assert result == expected


def test_yaml_comment_scalar_only_comments() -> None:
    """Scalar YAML with only markers and comments, no value line."""
    yaml_string = "---\n# just a comment\n...\n"
    result = literalize_yaml(
        yaml_string=yaml_string,
        language=PYTHON,
        prefix="",
        wrap=True,
    )
    expected = "# just a comment\nNone"
    assert result == expected


def test_yaml_comment_mapping_nested_value_none_token() -> None:
    """Mapping key with nested comment has None at token index 2."""
    yaml_string = "a:\n  # indented\n  x: 1\nb: 2\n"
    result = literalize_yaml(
        yaml_string=yaml_string,
        language=PYTHON,
        prefix="",
        wrap=True,
    )
    expected = textwrap.dedent(
        text="""\
        {
            "a": {"x": 1},
            "b": 2,
        }"""
    )
    assert result == expected
