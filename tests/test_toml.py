"""Tests for literalizer TOML conversion."""

import pytest

from literalizer import (
    InputFormat,
    literalize,
)
from literalizer._comments import extract_toml_comments
from literalizer.exceptions import (
    ParseError,
    TOMLParseError,
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


def test_invalid_toml() -> None:
    """``literalize_toml`` raises on invalid TOML."""
    with pytest.raises(expected_exception=TOMLParseError):
        literalize(
            source="not = [valid toml",
            input_format=InputFormat.TOML,
            language=PYTHON,
            pre_indent_level=0,
            include_delimiters=False,
        )


def test_invalid_toml_is_parse_error() -> None:
    """``TOMLParseError`` is a subclass of ``ParseError``."""
    with pytest.raises(expected_exception=ParseError):
        literalize(
            source="not = [valid toml",
            input_format=InputFormat.TOML,
            language=PYTHON,
            pre_indent_level=0,
            include_delimiters=False,
        )


def test_extract_toml_comments_non_document() -> None:
    """``extract_toml_comments`` returns empty for non-document input."""
    result = extract_toml_comments(toml_doc={"not": "a document"})
    assert not result.elements
    assert not result.trailing
