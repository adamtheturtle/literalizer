"""Tests for literalizer converter."""

from __future__ import annotations

import ast
import datetime
import json
import textwrap
from typing import Any

import pytest
import yaml
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
    format_datetime_python,
    format_datetime_ruby,
    literalize,
    literalize_json,
    literalize_yaml,
)


@pytest.mark.parametrize(
    argnames=("language", "expected"),
    argvalues=[
        (PYTHON, '(True, None, "hi", (1, 2)),'),
        (JAVASCRIPT, '[true, null, "hi", [1, 2]],'),
        (TYPESCRIPT, '[true, null, "hi", [1, 2]],'),
        (GO, '{true, nil, "hi", {1, 2}},'),
        (CPP, '{true, nullptr, "hi", {1, 2}},'),
        (JAVA, '{true, null, "hi", {1, 2}},'),
        (CSHARP, '(true, null, "hi", (1, 2)),'),
        (RUBY, '[true, nil, "hi", [1, 2]],'),
        (KOTLIN, 'listOf(true, null, "hi", listOf(1, 2)),'),
    ],
)
def test_language_list(*, language: Language, expected: str) -> None:
    """Each language produces the correct list literal."""
    data = [[True, None, "hi", [1, 2]]]
    result = literalize(data=data, language=language, prefix="", wrap=False)
    assert result == expected


def test_ruby_dict() -> None:
    """Ruby dicts use => syntax and nil."""
    data = [{"key": None}]
    result = literalize(data=data, language=RUBY, prefix="", wrap=False)
    assert result == '{"key" => nil},'


def test_dict_python() -> None:
    """Python dict renders key-value pairs with a prefix."""
    data = {"user_1": "team_alpha", "user_2": "team_alpha"}
    result = literalize(data=data, language=PYTHON, prefix="    ", wrap=False)
    assert result == '    "user_1": "team_alpha",\n    "user_2": "team_alpha",'


def test_dict_ruby() -> None:
    """Ruby dict renders with => syntax."""
    data = {"user_1": "team_alpha"}
    result = literalize(data=data, language=RUBY, prefix="  ", wrap=False)
    assert result == '  "user_1" => "team_alpha",'


def test_dict_wrap() -> None:
    """Wrapping a dict adds braces and indentation."""
    data = {"a": 1, "b": 2}
    result = literalize(data=data, language=PYTHON, prefix="", wrap=True)
    expected = textwrap.dedent(
        text="""\
        {
            "a": 1,
            "b": 2,
        }"""
    )
    assert result == expected


def test_dict_empty() -> None:
    """An empty dict produces an empty string."""
    result = literalize(data={}, language=PYTHON, prefix="", wrap=False)
    assert result == ""


def test_dict_empty_with_wrap() -> None:
    """An empty dict with wrap still produces an empty string."""
    result = literalize(data={}, language=PYTHON, prefix="", wrap=True)
    assert result == ""


def test_integers() -> None:
    """Integer values are rendered literally."""
    result = literalize(
        data=[42, 0, -7], language=PYTHON, prefix="", wrap=False
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
    result = literalize(
        data=[1000.0, 3.14], language=PYTHON, prefix="", wrap=False
    )
    expected = textwrap.dedent(
        text="""\
        1000.0,
        3.14,"""
    )
    assert result == expected


def test_string_escaping() -> None:
    """Special characters in strings are properly escaped."""
    data = ['say "hi"', "a\\b", "line1\nline2"]
    result = literalize(data=data, language=PYTHON, prefix="", wrap=False)
    lines = result.split(sep="\n")
    assert lines[0] == '"say \\"hi\\"",'
    assert lines[1] == '"a\\\\b",'
    assert lines[2] == '"line1\\nline2",'


def test_nested_arrays() -> None:
    """Nested arrays are rendered recursively."""
    data = [[[1, 2], [3, 4]]]
    result = literalize(data=data, language=PYTHON, prefix="", wrap=False)
    assert result == "((1, 2), (3, 4)),"


def test_dicts() -> None:
    """Dicts inside a list are rendered inline."""
    data = [{"name": "alice", "age": 30}]
    result = literalize(data=data, language=PYTHON, prefix="", wrap=False)
    assert result == '{"name": "alice", "age": 30},'


def test_nested_dict_in_list() -> None:
    """A dict nested inside a list is rendered inline."""
    data = [["a", {"x": 1}]]
    result = literalize(data=data, language=PYTHON, prefix="", wrap=False)
    assert result == '("a", {"x": 1}),'


def test_nested_list_in_dict() -> None:
    """A list nested inside a dict is rendered inline."""
    data = [{"items": [1, 2]}]
    result = literalize(data=data, language=PYTHON, prefix="", wrap=False)
    assert result == '{"items": (1, 2)},'


def test_prefix_spaces() -> None:
    """Space-based prefix is prepended to each line."""
    data = [True, False]
    result = literalize(
        data=data,
        language=PYTHON,
        prefix="        ",
        wrap=False,
    )
    assert result == "        True,\n        False,"


def test_prefix_tabs() -> None:
    """Tab-based prefix is prepended to each line."""
    data = [True, False]
    result = literalize(
        data=data,
        language=GO,
        prefix="\t\t",
        wrap=False,
    )
    assert result == "\t\ttrue,\n\t\tfalse,"


def test_wrap() -> None:
    """Wrapping adds brackets and indentation."""
    result = literalize(
        data=[True, False],
        language=PYTHON,
        prefix="",
        wrap=True,
    )
    expected = textwrap.dedent(
        text="""\
        [
            True,
            False,
        ]"""
    )
    assert result == expected


def test_wrap_with_prefix() -> None:
    """Wrapping respects the given prefix."""
    result = literalize(
        data=[["a", 1.0]],
        language=PYTHON,
        prefix="    ",
        wrap=True,
    )
    expected = textwrap.dedent(
        text="""\
        [
            ("a", 1.0),
        ]"""
    )
    assert result == expected


def test_empty_data() -> None:
    """An empty list produces an empty string."""
    result = literalize(data=[], language=PYTHON, prefix="", wrap=False)
    assert result == ""


def test_empty_data_with_wrap() -> None:
    """An empty list with wrap still produces an empty string."""
    result = literalize(data=[], language=PYTHON, prefix="", wrap=True)
    assert result == ""


@pytest.mark.parametrize(
    argnames=("data", "language", "expected"),
    argvalues=[
        (42, PYTHON, "42"),
        (3.14, PYTHON, "3.14"),
        ("hello", PYTHON, '"hello"'),
        (True, PYTHON, "True"),
        (False, PYTHON, "False"),
        (None, PYTHON, "None"),
        (True, JAVASCRIPT, "true"),
        (None, GO, "nil"),
        (None, RUBY, "nil"),
        (None, CPP, "nullptr"),
    ],
)
def test_scalar(*, data: Any, language: Language, expected: str) -> None:  # noqa: ANN401
    """Scalar values are formatted as native literals."""
    result = literalize(data=data, language=language, prefix="", wrap=False)
    assert result == expected


def test_scalar_with_prefix() -> None:
    """Scalar values respect the prefix parameter."""
    result = literalize(data=42, language=PYTHON, prefix="    ", wrap=False)
    assert result == "    42"


def test_scalar_wrap_ignored() -> None:
    """Wrap is ignored for scalar values."""
    result = literalize(data=42, language=PYTHON, prefix="", wrap=True)
    assert result == "42"


def test_unsupported_type_raises() -> None:
    """An unsupported scalar type raises TypeError."""
    with pytest.raises(
        expected_exception=TypeError, match="Unsupported scalar type"
    ):
        literalize(
            data=[object()],
            language=PYTHON,
            prefix="",
            wrap=False,
        )


def test_custom_language() -> None:
    """A custom LanguageSpec works as a language."""
    custom = LanguageSpec(
        null_literal="NIL",
        true_literal="YES",
        false_literal="NO",
        collection_open="<",
        collection_close=">",
        dict_separator=" -> ",
    )
    result = literalize(
        data=[True, None, "hi"],
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
    result = literalize(
        data=data,
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
    result = literalize(
        data=data,
        language=GO,
        prefix="        ",
        wrap=False,
    )
    lines = result.split(sep="\n")
    assert lines[0] == '        {"user_1", 49, 1000.0},'
    assert lines[1] == '        {"user_9", 10, 1003.0},'


type _JSONValue = (
    str | int | float | bool | None | list[_JSONValue] | dict[str, _JSONValue]
)


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
    with pytest.raises(expected_exception=json.JSONDecodeError):
        literalize_json(
            json_string="not json",
            language=PYTHON,
            prefix="",
            wrap=False,
        )


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
        ("null", GO, "nil"),
    ],
)
def test_literalize_json_scalar(
    *,
    json_string: str,
    language: Language,
    expected: str,
) -> None:
    """``literalize_json`` handles scalar JSON values."""
    result = literalize_json(
        json_string=json_string,
        language=language,
        prefix="",
        wrap=False,
    )
    assert result == expected


@given(data=json_arrays)
def test_roundtrip_array(data: list[Any]) -> None:
    """JSON array -> Python literal -> ast.literal_eval round-trips."""
    result = literalize(
        data=data,
        language=PYTHON,
        prefix="",
        wrap=True,
    )
    if not data:
        assert result == ""
        return
    parsed = ast.literal_eval(node_or_string=result)
    assert parsed == [_lists_to_tuples(value=v) for v in data]


@given(data=json_scalars)
def test_roundtrip_scalar(data: Any) -> None:  # noqa: ANN401
    """Scalar -> Python literal -> ast.literal_eval round-trips."""
    result = literalize(
        data=data,
        language=PYTHON,
        prefix="",
        wrap=False,
    )
    parsed = ast.literal_eval(node_or_string=result)
    assert parsed == data


@given(data=json_objects)
def test_roundtrip_dict(data: dict[str, Any]) -> None:
    """JSON object -> Python literal -> ast.literal_eval round-trips."""
    result = literalize(
        data=data,
        language=PYTHON,
        prefix="",
        wrap=True,
    )
    if not data:
        assert result == ""
        return
    parsed = ast.literal_eval(node_or_string=result)
    assert parsed == _lists_to_tuples(value=data)


@given(data=json_arrays)
def test_roundtrip_json_array(data: list[Any]) -> None:
    """Json.dumps -> literalize_json matches literalize for arrays."""
    json_string = json.dumps(obj=data)
    result_via_json = literalize_json(
        json_string=json_string,
        language=PYTHON,
        prefix="",
        wrap=True,
    )
    result_direct = literalize(
        data=data,
        language=PYTHON,
        prefix="",
        wrap=True,
    )
    assert result_via_json == result_direct


@given(data=json_objects)
def test_roundtrip_json_object(data: dict[str, Any]) -> None:
    """Json.dumps -> literalize_json matches literalize for objects."""
    json_string = json.dumps(obj=data)
    result_via_json = literalize_json(
        json_string=json_string,
        language=PYTHON,
        prefix="",
        wrap=True,
    )
    result_direct = literalize(
        data=data,
        language=PYTHON,
        prefix="",
        wrap=True,
    )
    assert result_via_json == result_direct


@given(data=json_scalars)
def test_roundtrip_json_scalar(data: Any) -> None:  # noqa: ANN401
    """Json.dumps -> literalize_json matches literalize for scalars."""
    json_string = json.dumps(obj=data)
    result_via_json = literalize_json(
        json_string=json_string,
        language=PYTHON,
        prefix="",
        wrap=False,
    )
    result_direct = literalize(
        data=data,
        language=PYTHON,
        prefix="",
        wrap=False,
    )
    assert result_via_json == result_direct


# YAML safe_load turns certain strings into dates/booleans, so we
# restrict the text strategy to only strings that survive a YAML
# dump/load cycle unchanged.  Dates and datetimes are tested as
# their own types in yaml_scalars below.
def _yaml_roundtrips_as_str(s: str) -> bool:
    """Return True if ``s`` survives a YAML dump/load cycle as a
    string.
    """
    loaded = yaml.safe_load(stream=yaml.dump(data=s))
    return bool(loaded == s)


yaml_safe_text = st.text(
    alphabet=st.characters(
        categories=("L", "M", "N", "P", "S", "Z"),
        exclude_characters="\x00",
    )
).filter(_yaml_roundtrips_as_str)  # type: ignore[misc]

yaml_scalars = (
    st.none()
    | st.booleans()
    | st.integers()
    | st.floats(allow_nan=False, allow_infinity=False)
    | yaml_safe_text
    | st.dates()
    | st.datetimes()
)

yaml_values: st.SearchStrategy[Any] = st.recursive(
    base=yaml_scalars,
    extend=lambda children: (
        st.lists(elements=children)
        | st.dictionaries(keys=yaml_safe_text, values=children)
    ),
)

yaml_arrays = st.lists(elements=yaml_values, max_size=10)
yaml_objects = st.dictionaries(
    keys=yaml_safe_text, values=yaml_values, max_size=10
)


@given(data=yaml_arrays)
def test_roundtrip_yaml_array(data: list[Any]) -> None:
    """Yaml.dump -> literalize_yaml matches literalize for arrays."""
    yaml_string = yaml.dump(data=data, sort_keys=False)
    result_via_yaml = literalize_yaml(
        yaml_string=yaml_string,
        language=PYTHON,
        prefix="",
        wrap=True,
    )
    result_direct = literalize(
        data=data,
        language=PYTHON,
        prefix="",
        wrap=True,
    )
    assert result_via_yaml == result_direct


@given(data=yaml_objects)
def test_roundtrip_yaml_object(data: dict[str, Any]) -> None:
    """Yaml.dump -> literalize_yaml matches literalize for objects."""
    yaml_string = yaml.dump(data=data, sort_keys=False)
    result_via_yaml = literalize_yaml(
        yaml_string=yaml_string,
        language=PYTHON,
        prefix="",
        wrap=True,
    )
    result_direct = literalize(
        data=data,
        language=PYTHON,
        prefix="",
        wrap=True,
    )
    assert result_via_yaml == result_direct


@given(data=yaml_scalars)
def test_roundtrip_yaml_scalar(data: Any) -> None:  # noqa: ANN401
    """Yaml.dump -> literalize_yaml matches literalize for scalars."""
    yaml_string = yaml.dump(data=data, sort_keys=False)
    result_via_yaml = literalize_yaml(
        yaml_string=yaml_string,
        language=PYTHON,
        prefix="",
        wrap=False,
    )
    result_direct = literalize(
        data=data,
        language=PYTHON,
        prefix="",
        wrap=False,
    )
    assert result_via_yaml == result_direct


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
    with pytest.raises(expected_exception=yaml.YAMLError):
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


def test_literalize_date() -> None:
    """``literalize`` formats datetime.date values as ISO string
    literals.
    """
    result = literalize(
        data=[datetime.date(year=2024, month=1, day=15)],
        language=PYTHON,
        prefix="",
        wrap=False,
    )
    assert result == '"2024-01-15",'


def test_literalize_datetime() -> None:
    """``literalize`` formats datetime.datetime values as ISO string
    literals.
    """
    result = literalize(
        data=[
            datetime.datetime(  # noqa: DTZ001
                year=2024,
                month=1,
                day=15,
                hour=12,
                minute=30,
                second=0,
            ),
        ],
        language=PYTHON,
        prefix="",
        wrap=False,
    )
    assert result == '"2024-01-15T12:30:00",'


_SAMPLE_DATE = datetime.date(year=2024, month=1, day=15)
_SAMPLE_DATETIME = datetime.datetime(  # noqa: DTZ001
    year=2024,
    month=1,
    day=15,
    hour=12,
    minute=30,
    second=0,
)
_SAMPLE_DATETIME_MICRO = datetime.datetime(  # noqa: DTZ001
    year=2024,
    month=1,
    day=15,
    hour=12,
    minute=30,
    second=0,
    microsecond=123456,
)


def test_format_date_iso() -> None:
    """``format_date_iso`` returns a quoted ISO string."""
    assert format_date_iso(value=_SAMPLE_DATE) == '"2024-01-15"'


def test_format_datetime_iso() -> None:
    """``format_datetime_iso`` returns a quoted ISO string."""
    assert (
        format_datetime_iso(value=_SAMPLE_DATETIME) == '"2024-01-15T12:30:00"'
    )


def test_format_date_python() -> None:
    """``format_date_python`` returns a constructor call."""
    assert (
        format_date_python(value=_SAMPLE_DATE) == "datetime.date(2024, 1, 15)"
    )


def test_format_datetime_python() -> None:
    """``format_datetime_python`` returns a constructor call."""
    assert (
        format_datetime_python(value=_SAMPLE_DATETIME)
        == "datetime.datetime(2024, 1, 15, 12, 30, 0)"
    )


def test_format_datetime_python_microsecond() -> None:
    """``format_datetime_python`` includes microseconds when set."""
    assert (
        format_datetime_python(value=_SAMPLE_DATETIME_MICRO)
        == "datetime.datetime(2024, 1, 15, 12, 30, 0, 123456)"
    )


def test_format_datetime_epoch() -> None:
    """``format_datetime_epoch`` returns a numeric timestamp."""
    result = format_datetime_epoch(value=_SAMPLE_DATETIME)
    # The exact value depends on local timezone for naive datetimes,
    # so just check it parses as a float.
    float(result)


def test_format_date_java() -> None:
    """``format_date_java`` returns a LocalDate.of call."""
    assert format_date_java(value=_SAMPLE_DATE) == "LocalDate.of(2024, 1, 15)"


def test_format_datetime_java_instant() -> None:
    """``format_datetime_java_instant`` returns an Instant.parse call."""
    assert (
        format_datetime_java_instant(value=_SAMPLE_DATETIME)
        == 'Instant.parse("2024-01-15T12:30:00")'
    )


def test_format_datetime_java_zoned() -> None:
    """``format_datetime_java_zoned`` returns a ZonedDateTime.of call."""
    result = format_datetime_java_zoned(value=_SAMPLE_DATETIME)
    assert result == (
        'ZonedDateTime.of(2024, 1, 15, 12, 30, 0, 0, ZoneId.of("UTC"))'
    )


def test_format_date_ruby() -> None:
    """``format_date_ruby`` returns a Date.new call."""
    assert format_date_ruby(value=_SAMPLE_DATE) == "Date.new(2024, 1, 15)"


def test_format_datetime_ruby() -> None:
    """``format_datetime_ruby`` returns a Time.new call."""
    assert (
        format_datetime_ruby(value=_SAMPLE_DATETIME)
        == "Time.new(2024, 1, 15, 12, 30, 0)"
    )


def test_format_date_js() -> None:
    """``format_date_js`` returns a new Date call."""
    assert format_date_js(value=_SAMPLE_DATE) == 'new Date("2024-01-15")'


def test_format_datetime_js() -> None:
    """``format_datetime_js`` returns a new Date call."""
    assert (
        format_datetime_js(value=_SAMPLE_DATETIME)
        == 'new Date("2024-01-15T12:30:00")'
    )


def test_format_date_csharp() -> None:
    """``format_date_csharp`` returns a new DateOnly call."""
    assert (
        format_date_csharp(value=_SAMPLE_DATE) == "new DateOnly(2024, 1, 15)"
    )


def test_format_datetime_csharp() -> None:
    """``format_datetime_csharp`` returns a new DateTime call."""
    assert (
        format_datetime_csharp(value=_SAMPLE_DATETIME)
        == "new DateTime(2024, 1, 15, 12, 30, 0)"
    )


def test_format_date_go() -> None:
    """``format_date_go`` returns a time.Date call."""
    assert format_date_go(value=_SAMPLE_DATE) == (
        "time.Date(2024, time.January, 15, 0, 0, 0, 0, time.UTC)"
    )


def test_format_datetime_go() -> None:
    """``format_datetime_go`` returns a time.Date call."""
    assert format_datetime_go(value=_SAMPLE_DATETIME) == (
        "time.Date(2024, time.January, 15, 12, 30, 0, 0, time.UTC)"
    )


def test_format_date_kotlin() -> None:
    """``format_date_kotlin`` returns a LocalDate.of call."""
    assert (
        format_date_kotlin(value=_SAMPLE_DATE) == "LocalDate.of(2024, 1, 15)"
    )


def test_format_datetime_kotlin() -> None:
    """``format_datetime_kotlin`` returns a LocalDateTime.of call."""
    assert (
        format_datetime_kotlin(value=_SAMPLE_DATETIME)
        == "LocalDateTime.of(2024, 1, 15, 12, 30, 0)"
    )


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
    midnight = datetime.datetime(  # noqa: DTZ001
        year=2024,
        month=1,
        day=15,
        hour=0,
        minute=0,
        second=0,
    )
    result = format_datetime_cpp(value=midnight)
    assert "std::chrono::sys_days" in result
    assert "hours" not in result
    assert "minutes" not in result
    assert "seconds" not in result
    assert "microseconds" not in result


def test_format_datetime_cpp_seconds_and_microseconds() -> None:
    """``format_datetime_cpp`` includes seconds and microseconds."""
    dt = datetime.datetime(  # noqa: DTZ001
        year=2024,
        month=1,
        day=15,
        hour=12,
        minute=30,
        second=45,
        microsecond=123456,
    )
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
        format_date=format_date_python,
    )
    result = literalize(
        data=[_SAMPLE_DATE],
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
        format_datetime=format_datetime_python,
    )
    result = literalize(
        data=[_SAMPLE_DATETIME],
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
        format_date=format_date_java,
        format_datetime=format_datetime_java_instant,
    )
    result = literalize(
        data=[_SAMPLE_DATE, _SAMPLE_DATETIME],
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
        format_date=format_date_ruby,
        format_datetime=format_datetime_ruby,
    )
    result = literalize(
        data=[_SAMPLE_DATETIME],
        language=spec,
        prefix="",
        wrap=False,
    )
    assert result == "Time.new(2024, 1, 15, 12, 30, 0),"


def test_yaml_with_custom_date_format() -> None:
    """YAML dates use the custom formatter from the language spec."""
    spec = LanguageSpec(
        null_literal="None",
        true_literal="True",
        false_literal="False",
        collection_open="(",
        collection_close=")",
        dict_separator=": ",
        format_date=format_date_python,
    )
    yaml_string = "- 2024-01-15\n"
    result = literalize_yaml(
        yaml_string=yaml_string,
        language=spec,
        prefix="",
        wrap=False,
    )
    assert result == "datetime.date(2024, 1, 15),"


def test_default_format_date_is_iso() -> None:
    """The default format_date is ISO format."""
    assert PYTHON.format_date is format_date_iso
    assert JAVA.format_date is format_date_iso


def test_default_format_datetime_is_iso() -> None:
    """The default format_datetime is ISO format."""
    assert PYTHON.format_datetime is format_datetime_iso
    assert JAVA.format_datetime is format_datetime_iso
