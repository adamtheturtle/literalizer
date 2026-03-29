"""String formatting functions."""

import re
from collections.abc import Callable

from beartype import beartype


@beartype
def format_string_concat_control(
    *,
    quote_char: str,
    quote_escape: str,
    control_char_template: str,
    concat_operator: str,
    escape_backslash: bool,
) -> Callable[[str], str]:
    """Return a string formatter that splits on control characters and
    concatenates parts with a language-specific operator.

    Text segments are wrapped in *quote_char* with embedded quotes
    escaped to *quote_escape*.  Control characters (code points 0-31)
    are emitted using *control_char_template* (which receives the code
    point as a positional format argument) and joined with
    *concat_operator*.

    When *escape_backslash* is ``True``, literal backslashes in text
    segments are doubled before quote escaping.

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

    @beartype
    def _format(value: str) -> str:
        """Format a string with control character concatenation."""
        control_char_threshold = 32
        parts: list[str] = []
        for segment in re.split(pattern=r"([\x00-\x1f])", string=value):
            if not segment:
                continue
            if len(segment) == 1 and ord(segment) < control_char_threshold:
                parts.append(control_char_template.format(ord(segment)))
            else:
                escaped = segment
                if escape_backslash:
                    escaped = escaped.replace("\\", "\\\\")
                escaped = escaped.replace(quote_char, quote_escape)
                parts.append(f"{quote_char}{escaped}{quote_char}")
        if not parts:
            return empty
        if len(parts) == 1:
            return parts[0]
        return concat_operator.join(parts)

    return _format


@beartype
def escape_control_chars(value: str, *, fmt: str) -> str:
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
def format_string_backslash(value: str) -> str:
    r"""Format a string using backslash escaping.

    Escapes backslashes, double quotes, and newlines with a backslash
    prefix, then wraps the result in double quotes.

    Example: ``hello "world"`` -> ``"hello \"world\""``.
    """
    escaped = (
        value.replace("\\", "\\\\")
        .replace('"', '\\"')
        .replace("\r", "\\r")
        .replace("\n", "\\n")
        .replace("\t", "\\t")
    )
    return f'"{escaped}"'


@beartype
def format_string_backslash_control(
    value: str,
    *,
    control_char_fmt: str,
) -> str:
    r"""Format a string using backslash escaping plus control-char escaping.

    Combines :func:`format_string_backslash`-style replacements with
    :func:`escape_control_chars` in one step.  The *control_char_fmt*
    is passed directly to :func:`escape_control_chars`.

    Example with ``control_char_fmt="\\x{:02x}"``::

        format_string_backslash_control("\x01hi", control_char_fmt="\\x{:02x}")
        # => '"\\x01hi"'
    """
    escaped = (
        value.replace("\\", "\\\\")
        .replace('"', '\\"')
        .replace("\r", "\\r")
        .replace("\n", "\\n")
        .replace("\t", "\\t")
    )
    escaped = escape_control_chars(value=escaped, fmt=control_char_fmt)
    return f'"{escaped}"'


@beartype
def format_string_backslash_single(value: str) -> str:
    r"""Format a string using backslash escaping with single quotes.

    Escapes backslashes, single quotes, and newlines with a backslash
    prefix, then wraps the result in single quotes.

    Example: ``hello 'world'`` -> ``'hello \'world\''``.
    """
    escaped = (
        value.replace("\\", "\\\\")
        .replace("'", "\\'")
        .replace("\r", "\\r")
        .replace("\n", "\\n")
        .replace("\t", "\\t")
    )
    return f"'{escaped}'"


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


@beartype
def format_string_bash_single(value: str) -> str:
    r"""Format a string for Bash single-quoted context.

    Bash single-quoted strings are completely literal — no escape
    sequences are recognized.  The only way to embed a single quote is
    to end the quoted region, insert an escaped single quote, and open
    a new quoted region: ``'\''``.

    Backslashes, newlines, tabs, and all other characters are kept
    verbatim.

    Example: ``hello 'world'`` -> ``'hello'\''world'``.
    """
    escaped = value.replace("'", r"'\''")
    return f"'{escaped}'"


@beartype
def format_string_backslash_dollar(value: str) -> str:
    r"""Format a string using backslash escaping, including ``$``.

    Escapes backslashes, double quotes, newlines, tabs, and dollar signs
    with a backslash prefix, then wraps the result in double quotes.

    Example: ``price $10`` -> ``"price \$10"``.
    """
    escaped = (
        value.replace("\\", "\\\\")
        .replace('"', '\\"')
        .replace("\r", "\\r")
        .replace("\n", "\\n")
        .replace("\t", "\\t")
        .replace("$", "\\$")
    )
    return f'"{escaped}"'


@beartype
def format_string_backslash_hash(value: str) -> str:
    r"""Format a string using backslash escaping, including ``#{``.

    Escapes backslashes, double quotes, newlines, tabs, and the
    interpolation sequence ``#{`` with a backslash prefix, then wraps the
    result in double quotes.

    Example: ``Issue #{42}`` -> ``"Issue \#{42}"``.
    """
    escaped = (
        value.replace("\\", "\\\\")
        .replace('"', '\\"')
        .replace("\r", "\\r")
        .replace("\n", "\\n")
        .replace("\t", "\\t")
        .replace("#{", "\\#{")
    )
    return f'"{escaped}"'


@beartype
def format_string_backslash_dollar_single(value: str) -> str:
    r"""Format a string using backslash escaping with single quotes,
    including ``$``.

    Escapes backslashes, single quotes, newlines, tabs, and dollar signs
    with a backslash prefix, then wraps the result in single quotes.

    Example: ``price $10`` -> ``'price \$10'``.
    """
    escaped = (
        value.replace("\\", "\\\\")
        .replace("'", "\\'")
        .replace("\r", "\\r")
        .replace("\n", "\\n")
        .replace("\t", "\\t")
        .replace("$", "\\$")
    )
    return f"'{escaped}'"
