"""JSON-format-specific behavior.

Cross-format checks (mixed dict values, heterogeneous collections,
invalid dict keys) live in :mod:`tests.errors`; this module is for
behaviors that only manifest when reading JSON.
"""

import pytest

from literalizer import InputFormat, literalize
from literalizer.exceptions import JSONParseError, ParseError
from literalizer.languages import Python

PYTHON = Python(
    date_format=Python.date_formats.PYTHON,
    datetime_format=Python.datetime_formats.PYTHON,
    bytes_format=Python.bytes_formats.HEX,
    sequence_format=Python.sequence_formats.TUPLE,
    set_format=Python.set_formats.SET,
    variable_type_hints=Python.variable_type_hints_formats.NEVER,
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
