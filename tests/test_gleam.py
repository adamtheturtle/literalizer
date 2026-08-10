"""Focused tests for Gleam rendering."""

from literalizer import InputFormat, literalize
from literalizer.languages import Gleam


def test_negative_gleam_integer_format() -> None:
    """Honor non-decimal formats for negative integers."""
    cases = [
        (Gleam.integer_formats.HEX, "GInt(-{0x5})"),
        (Gleam.integer_formats.OCTAL, "GInt(-{0o5})"),
        (Gleam.integer_formats.BINARY, "GInt(-{0b101})"),
    ]
    for integer_format, expected in cases:
        result = literalize(
            source="-5",
            input_format=InputFormat.JSON,
            language=Gleam(integer_format=integer_format),
        )

        assert result.code == expected
