"""Tests for literalizer converter."""

from __future__ import annotations

import ast
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
    literalize,
    literalize_json,
    literalize_yaml,
)


@pytest.mark.parametrize(
    ("language", "expected"),
    [
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
    expected = textwrap.dedent("""\
        {
            "a": 1,
            "b": 2,
        }""")
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
    expected = textwrap.dedent("""\
        42,
        0,
        -7,""")
    assert result == expected


def test_floats() -> None:
    """Float values are rendered literally."""
    result = literalize(
        data=[1000.0, 3.14], language=PYTHON, prefix="", wrap=False
    )
    expected = textwrap.dedent("""\
        1000.0,
        3.14,""")
    assert result == expected


def test_string_escaping() -> None:
    """Special characters in strings are properly escaped."""
    data = ['say "hi"', "a\\b", "line1\nline2"]
    result = literalize(data=data, language=PYTHON, prefix="", wrap=False)
    lines = result.split("\n")
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
    expected = textwrap.dedent("""\
        [
            True,
            False,
        ]""")
    assert result == expected


def test_wrap_with_prefix() -> None:
    """Wrapping respects the given prefix."""
    result = literalize(
        data=[["a", 1.0]],
        language=PYTHON,
        prefix="    ",
        wrap=True,
    )
    expected = textwrap.dedent("""\
        [
            ("a", 1.0),
        ]""")
    assert result == expected


def test_empty_data() -> None:
    """An empty list produces an empty string."""
    result = literalize(data=[], language=PYTHON, prefix="", wrap=False)
    assert result == ""


def test_empty_data_with_wrap() -> None:
    """An empty list with wrap still produces an empty string."""
    result = literalize(data=[], language=PYTHON, prefix="", wrap=True)
    assert result == ""


def test_unsupported_type_raises() -> None:
    """An unsupported scalar type raises TypeError."""
    with pytest.raises(TypeError, match="Unsupported scalar type"):
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
    assert result.split("\n") == expected_lines


def test_part2_sample_go() -> None:
    """Realistic test matching part2_sample_input.json structure."""
    data = [["user_1", 49, 1000.0], ["user_9", 10, 1003.0]]
    result = literalize(
        data=data,
        language=GO,
        prefix="        ",
        wrap=False,
    )
    lines = result.split("\n")
    assert lines[0] == '        {"user_1", 49, 1000.0},'
    assert lines[1] == '        {"user_9", 10, 1003.0},'


def _lists_to_tuples(value: Any) -> Any:  # noqa: ANN401
    """Recursively convert lists to tuples to match Python converter
    output.
    """
    if isinstance(value, list):
        return tuple(_lists_to_tuples(v) for v in value)  # pyright: ignore[reportUnknownVariableType]
    if isinstance(value, dict):
        return {  # pyright: ignore[reportUnknownVariableType]
            k: _lists_to_tuples(v)
            for k, v in value.items()  # pyright: ignore[reportUnknownVariableType]
        }
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
    json_scalars,
    lambda children: st.lists(children) | st.dictionaries(json_text, children),
)
json_arrays = st.lists(json_values, max_size=10)
json_objects = st.dictionaries(json_text, json_values, max_size=10)


def test_literalize_json_array() -> None:
    """Literalize_json parses a JSON array string."""
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
    """Literalize_json parses a JSON object string."""
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
    """Literalize_json raises on invalid JSON."""
    with pytest.raises(json.JSONDecodeError):
        literalize_json(
            json_string="not json",
            language=PYTHON,
            prefix="",
            wrap=False,
        )


def test_literalize_json_scalar_raises() -> None:
    """Literalize_json raises TypeError for scalar JSON."""
    with pytest.raises(TypeError, match="Expected a JSON array or object"):
        literalize_json(
            json_string="42",
            language=PYTHON,
            prefix="",
            wrap=False,
        )


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
    parsed = ast.literal_eval(result)
    assert parsed == [_lists_to_tuples(v) for v in data]


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
    parsed = ast.literal_eval(result)
    assert parsed == _lists_to_tuples(data)


def test_literalize_yaml_sequence() -> None:
    """Literalize_yaml parses a YAML sequence string."""
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
    """Literalize_yaml parses a YAML mapping string."""
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
    """Literalize_yaml raises on invalid YAML."""
    with pytest.raises(yaml.YAMLError):
        literalize_yaml(
            yaml_string=":\n  :\n    - ][",
            language=PYTHON,
            prefix="",
            wrap=False,
        )


def test_literalize_yaml_scalar_raises() -> None:
    """Literalize_yaml raises TypeError for scalar YAML."""
    with pytest.raises(TypeError, match="Expected a YAML sequence or mapping"):
        literalize_yaml(
            yaml_string="42",
            language=PYTHON,
            prefix="",
            wrap=False,
        )
