"""Regression tests for Haxe hexadecimal integer boundaries."""

import pytest

from literalizer import InputFormat, literalize
from literalizer.languages import Haxe


@pytest.mark.parametrize(
    argnames=("value", "expected"),
    argvalues=[
        (-(1 << 31) - 1, "-2147483649"),
        (-(1 << 31), "-0x80000000"),
        ((1 << 31) - 1, "0x7fffffff"),
        (1 << 31, "2147483648"),
        ((1 << 63) - 1, "9223372036854775807"),
    ],
    ids=("below-i32", "i32-min", "i32-max", "above-i32", "i64-max"),
)
def test_hex_falls_back_outside_signed_i32(value: int, expected: str) -> None:
    """Avoid Haxe integer wrapping and invalid wide hexadecimal
    literals.
    """
    integer_format = next(
        member for member in Haxe.integer_formats if member.name == "HEX"
    )
    result = literalize(
        source=f"{value}",
        input_format=InputFormat.JSON,
        language=Haxe(integer_format=integer_format),
    )

    assert expected in result.code
