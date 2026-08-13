"""Regression tests for Haskell C1 control-character strings."""

from literalizer import InputFormat, literalize
from literalizer.languages import Haskell


def test_c1_controls_use_bounded_hex_escapes() -> None:
    """Escape DEL/C1 characters without consuming following hex digits."""
    result = literalize(
        source='"\\u007f0\\u0080a\\u009fF"',
        input_format=InputFormat.JSON,
        language=Haskell(),
    )

    assert result.code == (
        'data Val = HStr String\nHStr "\\x7f\\&0\\x80\\&a\\x9f\\&F"'
    )
