"""Embedded null bytes that a language rejects rather than escaping.

Languages that can represent a null byte in their output are covered by
the ``string_embedded_nul`` golden-file axis (issue #3006); this module
holds the one behavior a golden file cannot express: the languages that
raise :class:`~literalizer.exceptions.UnrepresentableStringError`.
"""

import pytest

from literalizer import InputFormat, Language, NewVariable, literalize
from literalizer.exceptions import UnrepresentableStringError
from literalizer.languages import Cobol, R


def _render(*, language: Language, source: str) -> str:
    """Literalize *source* under *language* and return the code text."""
    return literalize(
        source=source,
        input_format=InputFormat.JSON,
        language=language,
        variable_form=NewVariable(name="my_data", modifiers=frozenset()),
    ).code


@pytest.mark.parametrize(argnames="language", argvalues=[R(), Cobol()])
def test_string_literals_reject_unrepresentable_nul(
    language: Language,
) -> None:
    """Targets without embedded null bytes in strings reject the value."""
    with pytest.raises(
        expected_exception=UnrepresentableStringError,
    ) as caught:
        _render(language=language, source='{"x": "\\u0000"}')

    assert caught.value.character_name == "NUL"
