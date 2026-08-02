"""Validation tests for C++ multiline raw-string delimiter bases."""

import pytest

from literalizer.exceptions import InvalidCppRawStringDelimiterError
from literalizer.languages import Cpp


@pytest.mark.parametrize(
    argnames="delimiter",
    argvalues=[
        "",
        "abcdefghijklmnopq",
        "has space",
        "left(",
        "right)",
        "back\\slash",
        "line\nbreak",
        "tab\tcharacter",
        "non-ascii-£",
        "dollar$",
        "at@",
        "grave`",
    ],
)
def test_invalid_cpp_raw_string_delimiter_raises(delimiter: str) -> None:
    """Invalid C++ ``d-char`` bases are rejected during construction."""
    with pytest.raises(
        expected_exception=InvalidCppRawStringDelimiterError,
        match="multiline_raw_string_delimiter_base",
    ):
        Cpp(multiline_raw_string_delimiter_base=delimiter)


def test_valid_cpp_raw_string_delimiter_punctuation() -> None:
    """Every permitted C++14 graphical punctuation category is
    accepted.
    """
    Cpp(multiline_raw_string_delimiter_base="_{}[]#<>%:;.?*")
