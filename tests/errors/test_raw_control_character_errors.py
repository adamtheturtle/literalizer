"""Raw C0 control characters never leak into generated source."""

import pytest

import literalizer
from literalizer._language import LanguageCls
from literalizer.exceptions import UnrepresentableStringError
from literalizer.languages import ALL_LANGUAGES

_LANGUAGES = sorted(ALL_LANGUAGES, key=lambda language: language.__name__)


@pytest.mark.parametrize(
    argnames="language_cls",
    argvalues=_LANGUAGES,
    ids=[language.__name__ for language in _LANGUAGES],
)
@pytest.mark.parametrize(
    argnames="code_point",
    argvalues=[*range(1, 9), 11, 12, *range(14, 32)],
)
def test_control_character_is_escaped_or_rejected(
    language_cls: LanguageCls,
    code_point: int,
) -> None:
    """Every back end either escapes a C0 character or rejects the
    input.
    """
    character = chr(code_point)
    try:
        result = literalizer.literalize(
            source=f'{{"value": "before\\u{code_point:04x}after"}}',
            input_format=literalizer.InputFormat.JSON,
            language=language_cls(),
        )
    except UnrepresentableStringError:
        return
    assert character not in result.code
