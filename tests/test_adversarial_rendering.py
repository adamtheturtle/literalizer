"""Regressions for source-level escape and continuation hazards."""

import json

import pytest

from literalizer import InputFormat, NewVariable, literalize
from literalizer._language import Language
from literalizer.languages import C, Perl, Php, Ruby, Tcl


@pytest.mark.parametrize(
    argnames="language",
    argvalues=[
        Ruby(string_format=Ruby.string_formats.SINGLE),
        Php(string_format=Php.string_formats.SINGLE),
        Perl(string_format=Perl.string_formats.SINGLE),
    ],
)
def test_single_quoted_crlf_uses_escaped_fallback(
    language: Language,
) -> None:
    """Source newline normalization must not change a string value."""
    result = literalize(
        source=json.dumps(obj={"x": "line1\r\nline2"}),
        input_format=InputFormat.JSON,
        language=language,
    )
    assert "\\r\\n" in result.code
    assert "line1\r\nline2" not in result.code


def test_tcl_nul_escape_does_not_consume_following_hex_digits() -> None:
    """A variable-width Tcl hex escape must not swallow ``after``."""
    result = literalize(
        source=json.dumps(obj={"x": "before\0after"}),
        input_format=InputFormat.JSON,
        language=Tcl(),
    )
    assert "before\\u0000after" in result.code


def test_line_comment_trailing_backslash_is_neutralized() -> None:
    """A preserved comment must not splice away the next C source line."""
    result = literalize(
        source="# comment ending backslash \\\nx: 1\n",
        input_format=InputFormat.YAML,
        language=C(),
        variable_form=NewVariable(name="x", modifiers=frozenset()),
        wrap_in_file=True,
    )
    assert "// comment ending backslash \\ \n" in result.code
