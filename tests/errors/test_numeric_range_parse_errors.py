"""Numeric tokens outside the binary64 value model."""

import math

import pytest

from literalizer import InputFormat, literalize
from literalizer.exceptions import ParseError
from literalizer.languages import Python


@pytest.mark.parametrize(
    argnames=("source", "input_format"),
    argvalues=[
        ("1e309", InputFormat.JSON),
        ("-1e-4000", InputFormat.JSON),
        ("1e309", InputFormat.JSON5),
        ("-1e-4000", InputFormat.JSON5),
        ("1e309", InputFormat.YAML),
        ("-1e-4000", InputFormat.YAML),
        ("value = 1e309", InputFormat.TOML),
        ("value = -1e-4000", InputFormat.TOML),
    ],
)
def test_finite_float_outside_binary64_range_raises(
    source: str,
    input_format: InputFormat,
) -> None:
    """Finite source numbers must not silently become infinity or zero."""
    with pytest.raises(
        expected_exception=ParseError,
        match="outside binary64 range",
    ):
        literalize(
            source=source,
            input_format=input_format,
            language=Python(),
        )


@pytest.mark.parametrize(
    argnames=("source", "input_format"),
    argvalues=[
        ("0e-4000", InputFormat.JSON),
        ("0e-4000", InputFormat.JSON5),
        ("0e-4000", InputFormat.YAML),
        ("value = 0e-4000", InputFormat.TOML),
    ],
)
def test_exact_zero_with_extreme_exponent_remains_valid(
    source: str,
    input_format: InputFormat,
) -> None:
    """An extreme exponent is safe when the exact source value is zero."""
    literalize(
        source=source,
        input_format=input_format,
        language=Python(),
    )


@pytest.mark.parametrize(
    argnames=("source", "input_format"),
    argvalues=[
        ("-0", InputFormat.JSON),
        ("-0", InputFormat.JSON5),
        ("-0", InputFormat.YAML),
        ("value = -0", InputFormat.TOML),
    ],
)
def test_negative_zero_integer_sign_is_preserved(
    source: str,
    input_format: InputFormat,
) -> None:
    """Signed integer zero enters the value model as negative float
    zero.
    """
    result = literalize(
        source=source,
        input_format=input_format,
        language=Python(),
    )
    value = (
        result.source_data["value"]
        if isinstance(result.source_data, dict)
        else result.source_data
    )

    assert isinstance(value, float)
    assert value == 0
    assert math.copysign(1, value) == -1
    assert "-0.0" in result.code
