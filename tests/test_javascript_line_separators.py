"""ECMAScript 2015 line-terminator escaping tests."""

import pytest

from literalizer import InputFormat, literalize
from literalizer._language import Language
from literalizer.languages import JavaScript


@pytest.mark.parametrize(
    argnames=("language", "quote"),
    argvalues=[
        (
            JavaScript(string_format=JavaScript.string_formats.DOUBLE),
            '"',
        ),
        (
            JavaScript(string_format=JavaScript.string_formats.SINGLE),
            "'",
        ),
    ],
)
def test_es2015_quoted_strings_escape_unicode_line_separators(
    language: Language,
    quote: str,
) -> None:
    """Keep ES2015 line terminators out of quoted string tokens."""
    result = literalize(
        source='"a\\u2028b\\u2029c"',
        input_format=InputFormat.JSON,
        language=language,
    )

    assert result.code == rf"{quote}a\u2028b\u2029c{quote}"


def test_template_strings_preserve_unicode_line_separators() -> None:
    """Template literals admit the separators as literal characters."""
    result = literalize(
        source='"a\\u2028b\\u2029c"',
        input_format=InputFormat.JSON,
        language=JavaScript(
            string_format=JavaScript.string_formats.MULTILINE,
        ),
    )

    assert result.code == "`a\u2028b\u2029c`"


def test_multiline_carriage_return_fallback_escapes_line_separators() -> None:
    """Keep fallback double-quoted output valid ES2015 syntax."""
    result = literalize(
        source='"a\\r\\u2028b"',
        input_format=InputFormat.JSON,
        language=JavaScript(
            string_format=JavaScript.string_formats.MULTILINE,
        ),
    )

    assert result.code == r'"a\r\u2028b"'
