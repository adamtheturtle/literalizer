"""Regression tests for D subnormal floating-point literals."""

import pytest

from literalizer import InputFormat, literalize
from literalizer.languages import D


@pytest.mark.parametrize(
    argnames="value",
    argvalues=[5e-324, -5e-324, 1e-310],
)
@pytest.mark.parametrize(
    argnames="float_format_name",
    argvalues=["REPR", "SCIENTIFIC", "FIXED"],
)
def test_subnormal_float_uses_hex_literal(
    value: float, float_format_name: str
) -> None:
    """Use D's accepted exact syntax for every float-format option."""
    assert isinstance(value, float)
    float_format = next(
        member
        for member in D.float_formats
        if member.name == float_format_name
    )
    result = literalize(
        source=repr(value),
        input_format=InputFormat.JSON,
        language=D(float_format=float_format),
    )

    assert value.hex() in result.code
