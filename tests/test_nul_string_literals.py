r"""Embedded NUL characters in string literals (#3006).

Targets that can escape NUL emit a fixed-width ``\x00`` form so the
source stays compiler-valid even when digits follow the escape.
Languages whose string model cannot hold NUL (R, COBOL) raise
:class:`~literalizer.exceptions.UnrepresentableStringError` before
source is returned.
"""

import pytest

from literalizer import InputFormat, Language, NewVariable, literalize
from literalizer.exceptions import UnrepresentableStringError
from literalizer.languages import (
    Cobol,
    Crystal,
    D,
    Go,
    Nim,
    Odin,
    Python,
    R,
    V,
)


def _render(*, language: Language, source: str = '{"x": "\\u0000"}') -> str:
    """Literalize *source* under *language* and return the code text."""
    return literalize(
        source=source,
        input_format=InputFormat.JSON,
        language=language,
        variable_form=NewVariable(name="my_data", modifiers=frozenset()),
    ).code


@pytest.mark.parametrize(
    argnames="language",
    argvalues=[
        Crystal(),
        D(),
        Go(),
        Nim(),
        Odin(),
        Python(),
        Python(string_format=Python.string_formats.SINGLE),
        Python(string_format=Python.string_formats.RAW),
        V(),
    ],
)
def test_string_literals_escape_nul(language: Language) -> None:
    r"""NUL data is represented by ``\x00``, never a raw NUL byte."""
    rendered = _render(language=language)

    assert "\0" not in rendered
    assert r"\x00" in rendered


@pytest.mark.parametrize(
    argnames="language",
    argvalues=[
        Crystal(),
        D(),
        Go(),
        Nim(),
        Odin(),
        Python(),
        V(),
    ],
)
def test_string_literals_escape_nul_before_digit(language: Language) -> None:
    r"""``\x00`` stays distinct when a digit follows the NUL."""
    rendered = _render(language=language, source='{"x": "\\u00001"}')

    assert "\0" not in rendered
    assert r"\x001" in rendered


@pytest.mark.parametrize(argnames="language", argvalues=[R(), Cobol()])
def test_string_literals_reject_unrepresentable_nul(
    language: Language,
) -> None:
    """Targets without embedded-NUL strings reject the value."""
    with pytest.raises(
        expected_exception=UnrepresentableStringError,
    ) as caught:
        _render(language=language)

    assert caught.value.character_name == "NUL"
