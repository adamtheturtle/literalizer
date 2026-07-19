r"""Embedded null bytes in string literals that a language cannot escape.

Languages whose string model can escape a null byte are covered by the
``string_embedded_nul`` golden-file axis (issue #3006); this module holds
the two behaviors a golden file cannot express: the languages that reject
the value, and COBOL's ``json_type=CJSON`` byte-splicing path.
"""

import pytest

from literalizer import InputFormat, Language, NewVariable, literalize
from literalizer.exceptions import UnrepresentableStringError
from literalizer.languages import Cobol, R


def _render(*, language: Language, source: str = '{"x": "\\u0000"}') -> str:
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
        _render(language=language)

    assert caught.value.character_name == "NUL"


def test_cobol_cjson_embeds_nul_hex_byte() -> None:
    r"""COBOL ``json_type=CJSON`` splices a null byte as an ``X"00"`` byte.

    The cJSON tree build rebuilds each string as a null-terminated
    buffer, so an embedded null byte is representable there and must not
    raise.
    """
    rendered = _render(language=Cobol(json_type=Cobol.json_types.CJSON))

    assert 'X"00" & X"00"' in rendered
