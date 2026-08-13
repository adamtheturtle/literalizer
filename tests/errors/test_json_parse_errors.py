"""JSON parsing error behavior.

Cross-format checks (mixed dict values, heterogeneous collections,
invalid dict keys) live elsewhere in :mod:`tests.errors`; this module
is for errors that only manifest when reading JSON.
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


@pytest.mark.parametrize(
    argnames="source",
    argvalues=['{"a": 1, "a": 2}', '{"outer": {"a": 1, "a": 2}}'],
)
def test_literalize_json_rejects_duplicate_keys(source: str) -> None:
    """JSON objects reject repeated keys at every nesting level."""
    with pytest.raises(
        expected_exception=JSONParseError, match="duplicate key 'a'"
    ):
        literalize(
            source=source,
            input_format=InputFormat.JSON,
            language=PYTHON,
        )


@pytest.mark.parametrize(
    argnames="constant",
    argvalues=["NaN", "Infinity", "-Infinity"],
)
def test_literalize_json_rejects_nonstandard_constants(
    constant: str,
) -> None:
    """Strict JSON rejects Python's non-standard numeric constants."""
    with pytest.raises(
        expected_exception=JSONParseError,
        match=f"Invalid JSON constant: {constant}",
    ):
        literalize(
            source=f"[{constant}]",
            input_format=InputFormat.JSON,
            language=PYTHON,
        )
