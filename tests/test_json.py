"""Tests for literalizer JSON conversion."""

import json
import re
import textwrap

import pytest

from literalizer import (
    InputFormat,
    NewVariable,
    literalize,
)
from literalizer.exceptions import (
    InvalidDictKeyError,
    JSONParseError,
    MixedDictValuesError,
    ParseError,
)
from literalizer.languages import (
    Cpp,
    Dhall,
    Go,
    Mojo,
    Nix,
    Python,
    R,
)

GO = Go(
    date_format=Go.date_formats.GO,
    datetime_format=Go.datetime_formats.GO,
    bytes_format=Go.bytes_formats.HEX,
    sequence_format=Go.sequence_formats.SLICE,
)
PYTHON = Python(
    date_format=Python.date_formats.PYTHON,
    datetime_format=Python.datetime_formats.PYTHON,
    bytes_format=Python.bytes_formats.HEX,
    sequence_format=Python.sequence_formats.TUPLE,
    set_format=Python.set_formats.SET,
    variable_type_hints=Python.variable_type_hints_formats.AUTO,
)


def test_dict_python() -> None:
    """Python dict renders key-value pairs with a pre-indent level."""
    data = {"user_1": "team_alpha", "user_2": "team_alpha"}
    result = literalize(
        source=json.dumps(obj=data),
        input_format=InputFormat.JSON,
        language=PYTHON,
        pre_indent_level=1,
        include_delimiters=False,
    )
    expected = '    "user_1": "team_alpha",\n    "user_2": "team_alpha",'
    assert result.code == expected


def test_dict_empty_no_delimiters() -> None:
    """An empty dict produces an empty string when delimiters are
    excluded.
    """
    result = literalize(
        source=json.dumps(obj={}),
        input_format=InputFormat.JSON,
        language=PYTHON,
        pre_indent_level=0,
        include_delimiters=False,
    )
    assert result.code == ""


def test_indent_spaces() -> None:
    """Space-based prefix is prepended to each line."""
    result = literalize(
        source=json.dumps(obj=[True, False]),
        input_format=InputFormat.JSON,
        language=PYTHON,
        pre_indent_level=2,
        include_delimiters=False,
    )
    assert result.code == "        True,\n        False,"


def test_indent_tabs() -> None:
    """Pre-indent level is applied using the Go language indent."""
    result = literalize(
        source=json.dumps(obj=[True, False]),
        input_format=InputFormat.JSON,
        language=GO,
        pre_indent_level=2,
        include_delimiters=False,
    )
    assert result.code == "\t\ttrue,\n\t\tfalse,"


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
    result = literalize(
        source=json.dumps(obj=[True, False]),
        input_format=InputFormat.JSON,
        language=language,
        pre_indent_level=0,
        include_delimiters=True,
    )
    expected = "(\n\tTrue,\n\tFalse,\n)"
    assert result.code == expected


def test_empty_list_no_delimiters() -> None:
    """An empty list produces an empty string when delimiters are
    excluded.
    """
    result = literalize(
        source=json.dumps(obj=[]),
        input_format=InputFormat.JSON,
        language=PYTHON,
        pre_indent_level=0,
        include_delimiters=False,
    )
    assert result.code == ""


def test_scalar_with_indent() -> None:
    """Scalar values respect the pre_indent_level parameter."""
    result = literalize(
        source="42",
        input_format=InputFormat.JSON,
        language=PYTHON,
        pre_indent_level=1,
        include_delimiters=False,
    )
    assert result.code == "    42"


def test_literalize_json_array() -> None:
    """``literalize_json`` parses a JSON array string."""
    json_string = '[["user_1", 1000.0], ["user_2", 2000.0]]'
    result = literalize(
        source=json_string,
        input_format=InputFormat.JSON,
        language=PYTHON,
        pre_indent_level=1,
        include_delimiters=False,
    )
    expected = '    ("user_1", 1000.0),\n    ("user_2", 2000.0),'
    assert result.code == expected


def test_literalize_json_invalid() -> None:
    """``literalize_json`` raises on invalid JSON."""
    with pytest.raises(expected_exception=JSONParseError):
        literalize(
            source="not json",
            input_format=InputFormat.JSON,
            language=PYTHON,
            pre_indent_level=0,
            include_delimiters=False,
        )


def test_part1_sample_python() -> None:
    """Realistic test matching part1_sample_input.json structure."""
    data = [
        ["user_1", 1000.0],
        ["user_1", 1001.0],
        ["user_1", 1002.0],
        ["user_1", 1003.0],
    ]
    result = literalize(
        source=json.dumps(obj=data),
        input_format=InputFormat.JSON,
        language=PYTHON,
        pre_indent_level=2,
        include_delimiters=False,
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
    result = literalize(
        source=json.dumps(obj=data),
        input_format=InputFormat.JSON,
        language=GO,
        pre_indent_level=2,
        include_delimiters=False,
    )
    lines = result.code.split(sep="\n")
    assert lines[0] == '\t\t[]any{"user_1", 49, 1000.0},'
    assert lines[1] == '\t\t[]any{"user_9", 10, 1003.0},'


def test_literalize_json_invalid_is_parse_error() -> None:
    """``JSONParseError`` is a subclass of ``ParseError``."""
    with pytest.raises(expected_exception=ParseError):
        literalize(
            source="not json",
            input_format=InputFormat.JSON,
            language=PYTHON,
            pre_indent_level=0,
            include_delimiters=False,
        )


MOJO = Mojo(
    date_format=Mojo.date_formats.ISO,
    datetime_format=Mojo.datetime_formats.ISO,
    bytes_format=Mojo.bytes_formats.HEX,
    sequence_format=Mojo.sequence_formats.LIST,
)


def test_cpp_array_null_list_fallback_json() -> None:
    """C++ ARRAY format falls back when schema type is not directly
    convertible (e.g. all-null list).
    """
    cpp_array = Cpp(sequence_format=Cpp.sequence_formats.ARRAY)
    result = literalize(
        source=json.dumps(obj=[None, None]),
        input_format=InputFormat.JSON,
        language=cpp_array,
        pre_indent_level=0,
        include_delimiters=True,
    )
    expected = textwrap.dedent(
        text="""\
        {
            nullptr,
            nullptr,
        }""",
    )
    assert result.code == expected


def test_mixed_dict_values_none_with_list_json_raises() -> None:
    """Dicts with None alongside a list raise for Mojo."""
    with pytest.raises(expected_exception=MixedDictValuesError):
        literalize(
            source=json.dumps(obj={"tags": ["admin"], "extra": None}),
            input_format=InputFormat.JSON,
            language=MOJO,
            pre_indent_level=0,
            include_delimiters=True,
        )


def test_mixed_dict_values_with_list_json_raises() -> None:
    """Dicts with string and list values raise for Mojo."""
    with pytest.raises(expected_exception=MixedDictValuesError):
        literalize(
            source=json.dumps(
                obj={"name": "Bob", "tags": ["admin", "user"]},
            ),
            input_format=InputFormat.JSON,
            language=MOJO,
            pre_indent_level=0,
            include_delimiters=True,
        )


def test_r_empty_dict_key_positional_json() -> None:
    """R with POSITIONAL empty_dict_key emits unnamed list elements."""
    spec = R(
        date_format=R.date_formats.R,
        datetime_format=R.datetime_formats.R,
        empty_dict_key=R.empty_dict_keys.POSITIONAL,
        bytes_format=R.bytes_formats.HEX,
        sequence_format=R.sequence_formats.LIST,
    )
    result = literalize(
        source=json.dumps(obj={"": "value"}),
        input_format=InputFormat.JSON,
        language=spec,
        pre_indent_level=0,
        include_delimiters=True,
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
    expected_msg = re.escape(
        pattern='R does not support the dict key "". '
        "Use empty_dict_key=R.EmptyDictKey.POSITIONAL to emit them "
        "as unnamed list elements instead."
    )
    with pytest.raises(
        expected_exception=InvalidDictKeyError,
        match=f"^{expected_msg}$",
    ):
        literalize(
            source=json.dumps(obj={"": "value"}),
            input_format=InputFormat.JSON,
            language=spec,
            pre_indent_level=0,
            include_delimiters=True,
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
    result = literalize(
        source=json.dumps(obj={"key": "value"}),
        input_format=InputFormat.JSON,
        language=spec,
        pre_indent_level=0,
        include_delimiters=True,
    )
    expected = textwrap.dedent(
        text="""\
        list(
            "key" = "value"
        )"""
    )
    assert result.code == expected


def test_dhall_empty_dict_key_error_json() -> None:
    """Dhall raises InvalidDictKeyError for empty-string dict keys."""
    expected_msg = re.escape(
        pattern='Dhall does not support the dict key "". '
        "Backtick-quoted labels must be non-empty and contain only "
        "printable ASCII (no backticks or control characters)."
    )
    with pytest.raises(
        expected_exception=InvalidDictKeyError,
        match=f"^{expected_msg}$",
    ):
        literalize(
            source=json.dumps(obj={"": "value"}),
            input_format=InputFormat.JSON,
            language=Dhall(),
            pre_indent_level=0,
            include_delimiters=True,
        )


def test_dhall_control_char_in_string_json() -> None:
    """Dhall escapes control characters using braced unicode escapes."""
    result = literalize(
        source=json.dumps(obj="\x01"),
        input_format=InputFormat.JSON,
        language=Dhall(),
        pre_indent_level=0,
        include_delimiters=True,
        variable_form=NewVariable(name="my_data"),
    )
    expected = 'let my_data = "\\u{0001}" in my_data'
    assert result.code == expected


def test_dhall_control_char_key_error_json() -> None:
    """Dhall rejects control characters in dict keys."""
    expected_msg = re.escape(
        pattern='Dhall does not support the dict key "\\u{0001}". '
        "Backtick-quoted labels must be non-empty and contain only "
        "printable ASCII (no backticks or control characters)."
    )
    with pytest.raises(
        expected_exception=InvalidDictKeyError,
        match=f"^{expected_msg}$",
    ):
        literalize(
            source=json.dumps(obj={"\x01": "value"}),
            input_format=InputFormat.JSON,
            language=Dhall(),
            pre_indent_level=0,
            include_delimiters=True,
        )


def test_nix_control_char_key_error_json() -> None:
    """Nix rejects control characters in dict keys."""
    expected_msg = re.escape(
        pattern='Nix does not support the dict key "\x01". '
        "Attribute names must be non-empty and must not contain "
        "control characters."
    )
    with pytest.raises(
        expected_exception=InvalidDictKeyError,
        match=f"^{expected_msg}$",
    ):
        literalize(
            source=json.dumps(obj={"\x01": "value"}),
            input_format=InputFormat.JSON,
            language=Nix(),
            pre_indent_level=0,
            include_delimiters=True,
        )


def test_dhall_backtick_label_unescaping_json() -> None:
    """Dhall backtick labels contain raw content, not escape sequences."""
    result = literalize(
        source=json.dumps(obj={"$other": "value"}),
        input_format=InputFormat.JSON,
        language=Dhall(),
        pre_indent_level=0,
        include_delimiters=True,
        variable_form=NewVariable(name="my_data"),
    )
    expected = textwrap.dedent(
        text="""\
        let my_data = {
          `$other` = "value",
        } in my_data"""
    )
    assert result.code == expected
