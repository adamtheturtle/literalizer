"""Tests for literalizer JSON conversion."""

import json
import re

import pytest

from literalizer import (
    InputFormat,
    literalize,
)
from literalizer.exceptions import (
    InvalidDictKeyError,
    JSONParseError,
    MixedDictValuesError,
    ParseError,
)
from literalizer.languages import (
    Dhall,
    Mojo,
    Nix,
    Python,
    R,
)

PYTHON = Python(
    date_format=Python.date_formats.PYTHON,
    datetime_format=Python.datetime_formats.PYTHON,
    bytes_format=Python.bytes_formats.HEX,
    sequence_format=Python.sequence_formats.TUPLE,
    set_format=Python.set_formats.SET,
    variable_type_hints=Python.variable_type_hints_formats.AUTO,
)


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


def test_dhall_quoted_dict_key_json() -> None:
    """Dhall backtick-label validation decodes simple escapes."""
    result = literalize(
        source=json.dumps(obj={'a"b': 1}),
        input_format=InputFormat.JSON,
        language=Dhall(),
        pre_indent_level=0,
        include_delimiters=True,
    )

    assert result.code == '{\n  `a"b` = +1,\n}'


def test_json_escaped_ref_key_literalizes_as_ref() -> None:
    """JSON escapes in ref marker keys are decoded before detection."""
    result = literalize(
        source='{"\\u0024ref": "my_var"}',
        input_format=InputFormat.JSON,
        language=PYTHON,
    )

    assert result.code == "my_var"


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
