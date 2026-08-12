"""String formatting functions."""

import re
from collections.abc import Callable, Sequence
from typing import Protocol, runtime_checkable

from beartype import beartype

from literalizer.exceptions import UnrepresentableStringError


@runtime_checkable
class _StringFormatter(Protocol):
    """Protocol for string formatting functions."""

    def __call__(self, value: str) -> str:
        """Format *value* using backslash escaping."""
        ...  # pylint: disable=unnecessary-ellipsis


@beartype
def _backslash_escape(*, value: str, quote_char: str) -> str:
    r"""Apply base backslash escapes to *value*.

    Escapes backslashes, *quote_char*, ``\r``, ``\n``, and ``\t``.
    Does **not** wrap the result in quotes.
    """
    return (
        value.replace("\\", "\\\\")
        .replace(quote_char, f"\\{quote_char}")
        .replace("\r", "\\r")
        .replace("\n", "\\n")
        .replace("\t", "\\t")
    )


@beartype
def _apply_backslash_formatter(
    value: str,
    quote_char: str,
    extra_replacements: Sequence[tuple[str, str]],
) -> str:
    """Format *value* using backslash escaping."""
    # Performance fast path: most strings are simple identifiers, keys, or
    # labels, so avoid the replacement chain unless the value contains a
    # character or sequence that would actually change the escaped output.
    has_base_escape = (
        "\\" in value
        or quote_char in value
        or "\r" in value
        or "\n" in value
        or "\t" in value
    )
    if not has_base_escape and not any(
        old in value for old, _new in extra_replacements
    ):
        return f"{quote_char}{value}{quote_char}"

    escaped = _backslash_escape(value=value, quote_char=quote_char)
    for old, new in extra_replacements:
        escaped = escaped.replace(old, new)
    return f"{quote_char}{escaped}{quote_char}"


@beartype
def make_backslash_string_formatter(
    *,
    quote_char: str,
    extra_replacements: Sequence[tuple[str, str]],
) -> _StringFormatter:
    r"""Return a backslash-escape string formatter.

    Every returned formatter applies the same base escapes — backslash,
    *quote_char*, ``\r``, ``\n``, ``\t`` — then any *extra_replacements*
    in order, and finally wraps the result in *quote_char*.

    *extra_replacements* is a sequence of ``(old, new)`` pairs passed to
    :meth:`str.replace`.
    """

    def _format(value: str) -> str:
        """Delegate to module-level implementation."""
        return _apply_backslash_formatter(
            value=value,
            quote_char=quote_char,
            extra_replacements=extra_replacements,
        )

    return _format


format_string_backslash = make_backslash_string_formatter(
    quote_char='"',
    extra_replacements=(),
)
r"""Format a string using backslash escaping.

Escapes backslashes, double quotes, and newlines with a backslash
prefix, then wraps the result in double quotes.

Example: ``hello "world"`` -> ``"hello \"world\""``.
"""

format_string_backslash_nul_hex = make_backslash_string_formatter(
    quote_char='"',
    extra_replacements=[("\0", "\\x00")],
)
format_string_backslash_single_nul_hex = make_backslash_string_formatter(
    quote_char="'",
    extra_replacements=[("\0", r"\x00")],
)
r"""Format a double-quoted string and escape the null byte as ``\x00``.

Fixed-width hex avoids digit-greedy octal/decimal escapes such as
``\0`` followed by ``0``-``7`` (or Nim's decimal ``\0``).
"""

format_string_backslash_nul_octal = make_backslash_string_formatter(
    quote_char='"',
    extra_replacements=[("\0", "\\000")],
)
r"""Format a double-quoted string and escape NUL as fixed-width ``\000``."""

format_string_backslash_nul_unicode = make_backslash_string_formatter(
    quote_char='"',
    extra_replacements=[("\0", "\\u0000")],
)
r"""Format a double-quoted string and escape NUL as ``\u0000``."""

format_string_backslash_nul_braced_unicode = make_backslash_string_formatter(
    quote_char='"',
    extra_replacements=[("\0", "\\u{0000}")],
)
r"""Format a double-quoted string and escape NUL as ``\u{0000}``."""

format_string_backslash_dollar = make_backslash_string_formatter(
    quote_char='"',
    extra_replacements=[("$", "\\$")],
)
r"""Format a string using backslash escaping, including ``$``.

Escapes backslashes, double quotes, newlines, tabs, and dollar signs
with a backslash prefix, then wraps the result in double quotes.

Example: ``price $10`` -> ``"price \$10"``.
"""

format_string_backslash_dollar_nul_hex = make_backslash_string_formatter(
    quote_char='"',
    extra_replacements=[("$", "\\$"), ("\0", "\\x00")],
)
r"""Escape dollar interpolation and NUL in a double-quoted string."""

format_string_backslash_dollar_nul_unicode = make_backslash_string_formatter(
    quote_char='"',
    extra_replacements=[("$", "\\$"), ("\0", "\\u0000")],
)
r"""Escape dollar interpolation and NUL with a Unicode escape."""


@beartype
def reject_nul_string_formatter(
    formatter: Callable[[str], str],
    /,
    *,
    language_name: str,
) -> Callable[[str], str]:
    """Wrap *formatter* to reject strings with an embedded null byte."""

    def _format(value: str) -> str:
        """Reject a null byte, then delegate to the wrapped formatter."""
        if "\0" in value:
            raise UnrepresentableStringError(
                language_name=language_name,
                character_name="NUL",
            )
        return formatter(value)

    return _format


@beartype
def format_string_concat_control(
    *,
    quote_char: str,
    quote_escape: str,
    control_char_template: str,
    concat_operator: str,
) -> Callable[[str], str]:
    """Return a string formatter that splits on control characters and
    concatenates parts with a language-specific operator.

    Text segments are wrapped in *quote_char* with embedded quotes
    escaped to *quote_escape*.  Control characters (code points 0-31)
    are emitted using *control_char_template* (which receives the code
    point as a positional format argument) and joined with
    *concat_operator*.

    Example::

        format_string = format_string_concat_control(
            quote_char="'",
            quote_escape="''",
            control_char_template="achar({})",
            concat_operator=" // ",
        )
        format_string("hello")  # => "'hello'"
    """
    empty = f"{quote_char}{quote_char}"

    def _format(value: str) -> str:
        """Delegate to module-level implementation."""
        return _apply_concat_control(
            value=value,
            quote_char=quote_char,
            quote_escape=quote_escape,
            control_char_template=control_char_template,
            concat_operator=concat_operator,
            empty=empty,
        )

    return _format


@beartype
def _apply_concat_control(
    value: str,
    *,
    quote_char: str,
    quote_escape: str,
    control_char_template: str,
    concat_operator: str,
    empty: str,
) -> str:
    """Format a string with control character concatenation."""
    control_char_threshold = 32
    parts: list[str] = []
    for segment in re.split(pattern=r"([\x00-\x1f])", string=value):
        if not segment:
            continue
        if len(segment) == 1 and ord(segment) < control_char_threshold:
            parts.append(control_char_template.format(ord(segment)))
        else:
            escaped = segment.replace(quote_char, quote_escape)
            parts.append(f"{quote_char}{escaped}{quote_char}")
    match parts:
        case []:
            return empty
        case [single]:
            return single
        case _:
            return concat_operator.join(parts)


@beartype
def escape_control_chars(*, value: str, fmt: str) -> str:
    r"""Replace C0 control characters (U+0000-U+001F) with escape sequences.

    Call **after** replacing named escapes (``\t``, ``\n``, ``\r``) so that
    only truly unhandled control characters are affected.

    The format pattern passed in ``fmt`` receives the code point as a
    positional integer, e.g. ``"\\x{:02x}"`` -> ``\\x01``.
    """
    return re.sub(
        pattern=r"[\x00-\x1f]",
        repl=lambda m: fmt.format(ord(m.group())),
        string=value,
    )


@beartype
def format_string_backslash_control(
    *,
    value: str,
    control_char_fmt: str,
) -> str:
    r"""Format a string using backslash escaping plus control-char escaping.

    Combines :func:`format_string_backslash`-style replacements with
    :func:`escape_control_chars` in one step.  The *control_char_fmt*
    is passed directly to :func:`escape_control_chars`.

    Example with ``control_char_fmt="\\x{:02x}"`` and ``value="\x01hi"``
    returns ``'"\\x01hi"'``.
    """
    escaped = _backslash_escape(value=value, quote_char='"')
    escaped = escape_control_chars(value=escaped, fmt=control_char_fmt)
    return f'"{escaped}"'


@beartype
def format_string_backslash_single_minimal(value: str) -> str:
    r"""Format a string with single quotes, escaping only ``\\`` and ``\'``.

    For languages like Ruby, Perl, and PHP where single-quoted strings
    only recognize ``\\`` and ``\'`` as escape sequences.  Actual
    newline, carriage-return, and tab characters are embedded literally.

    Example: ``hello 'world'`` -> ``'hello \'world\''``.
    """
    escaped = value.replace("\\", "\\\\").replace("'", "\\'")
    return f"'{escaped}'"
