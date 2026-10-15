"""Compatibility for the independent JSON5 golden validation parser."""

import re

from beartype import beartype

_JSON5_STRING_OR_COMMENT = re.compile(
    pattern=(
        r"\"(?:[^\"\\]|\\.)*\""
        r"|'(?:[^'\\]|\\.)*'"
        r"|//[^\n\r\u2028\u2029]*"
        r"|/\*.*?\*/"
    ),
    flags=re.DOTALL,
)

_JSON5_ESCAPE_OR_SEPARATOR = re.compile(
    pattern=r"\\.|[\u2028\u2029]",
    flags=re.DOTALL,
)

_JSON5_RAW_LINE_SEPARATORS = {
    "\u2028": "\\u2028",
    "\u2029": "\\u2029",
}


@beartype
def escape_json5_line_separators(*, source: str) -> str:
    r"""Escape raw U+2028 and U+2029 inside JSON5 string literals.

    JSON5 allows both of them raw inside a string, precisely so that
    every JSON document is also a JSON5 document, but the ``json5``
    package refuses one while reading the string.  Escaping them
    before the parse restores the guarantee, and the parser turns the
    escapes back into the same two characters (issue #4518).

    Outside a string both are line terminators, which end a ``//``
    comment, so only the ones a string literal encloses are rewritten.
    """
    if not any(
        separator in source for separator in _JSON5_RAW_LINE_SEPARATORS
    ):
        return source

    def _escape_separator(match: re.Match[str]) -> str:
        """Return the escape for a bare separator, or the text as-is."""
        return _JSON5_RAW_LINE_SEPARATORS.get(match.group(), match.group())

    def _escape_token(match: re.Match[str]) -> str:
        """Return the matched token with any enclosed separator
        escaped.
        """
        token = match.group()
        if token[0] not in {"'", '"'}:
            return token
        # A backslash before a separator is a line continuation, which
        # escaping the separator would turn into an escaped backslash
        # followed by the text "u2028", so escape pairs are matched
        # first and passed through whole.
        return _JSON5_ESCAPE_OR_SEPARATOR.sub(
            repl=_escape_separator,
            string=token,
        )

    return _JSON5_STRING_OR_COMMENT.sub(repl=_escape_token, string=source)
