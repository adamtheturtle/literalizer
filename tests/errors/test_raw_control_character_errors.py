"""Raw C0 control characters never leak into generated source."""

import pytest

import literalizer
from literalizer._language import LanguageCls
from literalizer.exceptions import (
    InvalidDictKeyError,
    UnrepresentableStringError,
)
from literalizer.languages import ALL_LANGUAGES, Cobol

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


@pytest.mark.parametrize(
    argnames="language_cls",
    argvalues=_LANGUAGES,
    ids=[language.__name__ for language in _LANGUAGES],
)
@pytest.mark.parametrize(
    argnames="code_point",
    argvalues=[*range(1, 9), 11, 12, *range(14, 32)],
)
def test_control_character_dict_key_is_escaped_or_rejected(
    language_cls: LanguageCls,
    code_point: int,
) -> None:
    """C0 characters cannot leak through string-valued dict keys."""
    character = chr(code_point)
    try:
        result = literalizer.literalize(
            source=f'{{"before\\u{code_point:04x}after": 1}}',
            input_format=literalizer.InputFormat.JSON,
            language=language_cls(),
        )
    except (InvalidDictKeyError, UnrepresentableStringError):
        return
    assert character not in result.code


def test_cobol_control_character_key_uses_safe_data_name() -> None:
    """COBOL derives a safe identifier without rendering the raw key."""
    result = literalizer.literalize(
        source='{"before\\u0001after": 1}',
        input_format=literalizer.InputFormat.JSON,
        language=Cobol(),
    )

    assert "\x01" not in result.code
