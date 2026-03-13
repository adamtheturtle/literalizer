"""Tests for literalizer converter."""

from __future__ import annotations

import ast
import textwrap
from typing import Any

import pytest
from hypothesis import given
from hypothesis import strategies as st

from literalizer import convert_json_to_native_literal


@pytest.mark.parametrize(
    ("language", "expected"),
    [
        ("py", '(True, None, "hi", (1, 2)),'),
        ("js", '[true, null, "hi", [1, 2]],'),
        ("ts", '[true, null, "hi", [1, 2]],'),
        ("go", '{true, nil, "hi", {1, 2}},'),
        ("cpp", '{true, nullptr, "hi", {1, 2}},'),
        ("java", '{true, null, "hi", {1, 2}},'),
        ("cs", '(true, null, "hi", (1, 2)),'),
        ("rb", '[true, nil, "hi", [1, 2]],'),
        ("kt", 'listOf(true, null, "hi", listOf(1, 2)),'),
    ],
)
def test_language_list(*, language: str, expected: str) -> None:
    data = [[True, None, "hi", [1, 2]]]
    result = convert_json_to_native_literal(data=data, language=language, prefix="", wrap=False)
    assert result == expected


def test_ruby_dict() -> None:
    data = [{"key": None}]
    result = convert_json_to_native_literal(data=data, language="rb", prefix="", wrap=False)
    assert result == '{"key" => nil},'


def test_dict_python() -> None:
    data = {"user_1": "team_alpha", "user_2": "team_alpha"}
    result = convert_json_to_native_literal(data=data, language="py", prefix="    ", wrap=False)
    assert result == '    "user_1": "team_alpha",\n    "user_2": "team_alpha",'


def test_dict_ruby() -> None:
    data = {"user_1": "team_alpha"}
    result = convert_json_to_native_literal(data=data, language="rb", prefix="  ", wrap=False)
    assert result == '  "user_1" => "team_alpha",'


def test_dict_wrap() -> None:
    data = {"a": 1, "b": 2}
    result = convert_json_to_native_literal(data=data, language="py", prefix="", wrap=True)
    expected = textwrap.dedent("""\
        {
            "a": 1,
            "b": 2,
        }""")
    assert result == expected


def test_dict_empty() -> None:
    result = convert_json_to_native_literal(data={}, language="py", prefix="", wrap=False)
    assert result == ""


def test_dict_empty_with_wrap() -> None:
    result = convert_json_to_native_literal(data={}, language="py", prefix="", wrap=True)
    assert result == ""


def test_integers() -> None:
    result = convert_json_to_native_literal(data=[42, 0, -7], language="py", prefix="", wrap=False)
    expected = textwrap.dedent("""\
        42,
        0,
        -7,""")
    assert result == expected


def test_floats() -> None:
    result = convert_json_to_native_literal(data=[1000.0, 3.14], language="py", prefix="", wrap=False)
    expected = textwrap.dedent("""\
        1000.0,
        3.14,""")
    assert result == expected


def test_string_escaping() -> None:
    data = ['say "hi"', "a\\b", "line1\nline2"]
    result = convert_json_to_native_literal(data=data, language="py", prefix="", wrap=False)
    lines = result.split("\n")
    assert lines[0] == '"say \\"hi\\"",'
    assert lines[1] == '"a\\\\b",'
    assert lines[2] == '"line1\\nline2",'


def test_nested_arrays() -> None:
    data = [[[1, 2], [3, 4]]]
    result = convert_json_to_native_literal(data=data, language="py", prefix="", wrap=False)
    assert result == "((1, 2), (3, 4)),"


def test_dicts() -> None:
    data = [{"name": "alice", "age": 30}]
    result = convert_json_to_native_literal(data=data, language="py", prefix="", wrap=False)
    assert result == '{"name": "alice", "age": 30},'


def test_nested_dict_in_list() -> None:
    data = [["a", {"x": 1}]]
    result = convert_json_to_native_literal(data=data, language="py", prefix="", wrap=False)
    assert result == '("a", {"x": 1}),'


def test_nested_list_in_dict() -> None:
    data = [{"items": [1, 2]}]
    result = convert_json_to_native_literal(data=data, language="py", prefix="", wrap=False)
    assert result == '{"items": (1, 2)},'


def test_prefix_spaces() -> None:
    data = [True, False]
    result = convert_json_to_native_literal(
        data=data,
        language="py",
        prefix="        ",
        wrap=False,
    )
    assert result == "        True,\n        False,"


def test_prefix_tabs() -> None:
    data = [True, False]
    result = convert_json_to_native_literal(
        data=data,
        language="go",
        prefix="\t\t",
        wrap=False,
    )
    assert result == "\t\ttrue,\n\t\tfalse,"


def test_wrap() -> None:
    result = convert_json_to_native_literal(
        data=[True, False],
        language="py",
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
    result = convert_json_to_native_literal(
        data=[["a", 1.0]],
        language="py",
        prefix="    ",
        wrap=True,
    )
    expected = textwrap.dedent("""\
        [
            ("a", 1.0),
        ]""")
    assert result == expected


def test_empty_data() -> None:
    result = convert_json_to_native_literal(data=[], language="py", prefix="", wrap=False)
    assert result == ""


def test_empty_data_with_wrap() -> None:
    result = convert_json_to_native_literal(data=[], language="py", prefix="", wrap=True)
    assert result == ""


def test_unknown_language_raises() -> None:
    with pytest.raises(KeyError):
        convert_json_to_native_literal(data=[True], language="xyz", prefix="", wrap=False)


def test_unsupported_type_raises() -> None:
    with pytest.raises(TypeError, match="Unsupported scalar type"):
        convert_json_to_native_literal(
            data=[object()],
            language="py",
            prefix="",
            wrap=False,
        )


def test_part1_sample_python() -> None:
    """Realistic test matching part1_sample_input.json structure."""
    data = [
        ["user_1", 1000.0],
        ["user_1", 1001.0],
        ["user_1", 1002.0],
        ["user_1", 1003.0],
    ]
    result = convert_json_to_native_literal(
        data=data,
        language="py",
        prefix="        ",
        wrap=False,
    )
    lines = result.split("\n")
    assert len(lines) == 4
    assert lines[0] == '        ("user_1", 1000.0),'
    assert lines[3] == '        ("user_1", 1003.0),'


def test_part2_sample_go() -> None:
    """Realistic test matching part2_sample_input.json structure."""
    data = [["user_1", 49, 1000.0], ["user_9", 10, 1003.0]]
    result = convert_json_to_native_literal(
        data=data,
        language="go",
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


json_text = st.text(alphabet=st.characters(categories=("L", "M", "N", "P", "S", "Z"), exclude_characters="\x00"))
json_scalars = st.none() | st.booleans() | st.integers() | st.floats(allow_nan=False, allow_infinity=False) | json_text
json_values: st.SearchStrategy[Any] = st.recursive(
    json_scalars,
    lambda children: st.lists(children) | st.dictionaries(json_text, children),
)
json_arrays = st.lists(json_values, max_size=10)
json_objects = st.dictionaries(json_text, json_values, max_size=10)


@given(data=json_arrays)
def test_roundtrip_array(data: list[Any]) -> None:
    """JSON array -> Python literal -> ast.literal_eval round-trips."""
    result = convert_json_to_native_literal(
        data=data,
        language="py",
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
    result = convert_json_to_native_literal(
        data=data,
        language="py",
        prefix="",
        wrap=True,
    )
    if not data:
        assert result == ""
        return
    parsed = ast.literal_eval(result)
    assert parsed == _lists_to_tuples(data)
