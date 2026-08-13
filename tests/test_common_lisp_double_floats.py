"""Regression tests for Common Lisp double-float literals."""

import re

import pytest

from literalizer import InputFormat, literalize
from literalizer.languages import CommonLisp


@pytest.mark.parametrize(
    argnames="value",
    argvalues=[0.1, 1e308, 5e-324],
)
@pytest.mark.parametrize(
    argnames="float_format_name",
    argvalues=["REPR", "SCIENTIFIC", "FIXED"],
)
def test_finite_float_uses_double_marker(
    value: float, float_format_name: str
) -> None:
    """Emit a double-float under the default Common Lisp reader state."""
    float_format = next(
        member
        for member in CommonLisp.float_formats
        if member.name == float_format_name
    )
    result = literalize(
        source=repr(value),
        input_format=InputFormat.JSON,
        language=CommonLisp(float_format=float_format),
    )

    assert re.search(pattern=r"d[+-]?\d+", string=result.code.lower())
