"""Focused tests for shared string-formatting helpers."""

from literalizer._formatters.format_strings import (
    format_string_concat_control,
)


def test_concat_control_formatter_can_escape_backslashes() -> None:
    """Backslash-escaping formatters double literal backslashes."""
    formatter = format_string_concat_control(
        quote_char='"',
        quote_escape='""',
        control_char_template="char({})",
        concat_operator=" + ",
        escape_backslash=True,
    )

    assert formatter("a\\b") == '"a\\\\b"'
