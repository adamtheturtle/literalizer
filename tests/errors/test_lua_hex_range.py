"""Validation tests for Lua hexadecimal integer bounds."""

import pytest

from literalizer import InputFormat, literalize
from literalizer.exceptions import UnrepresentableIntegerError
from literalizer.languages import Lua

I64_MIN = -(1 << 63)
I64_MAX = (1 << 63) - 1


@pytest.mark.parametrize(
    argnames="value",
    argvalues=[I64_MIN - 1, I64_MAX + 1, 1 << 64, (1 << 64) + 5],
)
def test_hex_rejects_values_outside_signed_i64(value: int) -> None:
    """Do not emit hexadecimal numerals that Lua wraps modulo 2^64."""
    integer_format = next(
        member for member in Lua.integer_formats if member.name == "HEX"
    )

    with pytest.raises(
        expected_exception=UnrepresentableIntegerError,
        match=rf"^Lua cannot represent {value} as a hexadecimal integer$",
    ):
        literalize(
            source=f"{value}",
            input_format=InputFormat.JSON,
            language=Lua(integer_format=integer_format),
        )
