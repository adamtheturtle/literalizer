"""Tests for literalizer JSON5 conversion."""

import pytest

from literalizer import (
    InputFormat,
    literalize,
)
from literalizer.exceptions import (
    JSON5ParseError,
    ParseError,
)
from literalizer.languages import (
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
        )
