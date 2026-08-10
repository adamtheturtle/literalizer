"""Perl multiline string escaping checks."""

import json

from literalizer import InputFormat, literalize
from literalizer.languages import Perl


def test_perl_multiline_fallback_escapes_symbols_once() -> None:
    """The double-quoted fallback escapes dollar and at signs once."""
    string_format = next(
        member
        for member in type(Perl().string_format)
        if member.name == "MULTILINE"
    )
    result = literalize(
        source=json.dumps(obj="line  \n$price @items\0"),
        input_format=InputFormat.JSON,
        language=Perl(string_format=string_format),
        variable_form=None,
    )

    assert r"\$price \@items\x{0}" in result.code
    assert r"\\$price" not in result.code
