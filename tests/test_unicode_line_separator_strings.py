"""Regression tests for Unicode line separators in string literals."""

import pytest

from literalizer import InputFormat, Language, NewVariable, literalize
from literalizer.languages import Ada, CSharp, Elixir, Erlang, Fortran

_LINE_SEPARATORS = "\x85\u2028\u2029"
_CSHARP_VERBATIM = next(
    member for member in CSharp.string_formats if member.name == "VERBATIM"
)


@pytest.mark.parametrize(
    argnames=("language", "escape_fragment"),
    argvalues=[
        (Ada(), "Character'Val(226)"),
        (CSharp(), r"\u2028"),
        (CSharp(string_format=_CSHARP_VERBATIM), r"\u2028"),
        (Elixir(), r"\u2028"),
        (Erlang(), r"\x{2028}"),
        (Fortran(), "achar(226)"),
    ],
)
def test_unicode_line_separators_are_not_emitted_raw(
    language: Language, escape_fragment: str
) -> None:
    """Keep Unicode line separators out of generated string tokens."""
    result = literalize(
        source='"a\\u0085b\\u2028c\\u2029d"',
        input_format=InputFormat.JSON,
        language=language,
        variable_form=NewVariable(name="my_data", modifiers=frozenset()),
        wrap_in_file=True,
    )

    assert not any(character in result.code for character in _LINE_SEPARATORS)
    assert escape_fragment in result.code
