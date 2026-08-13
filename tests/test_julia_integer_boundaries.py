"""Regression tests for Julia integers at the signed 64-bit boundary."""

import pytest

from literalizer import InputFormat, literalize
from literalizer.languages import Julia


@pytest.mark.parametrize(
    argnames="integer_format_name",
    argvalues=["HEX", "OCTAL", "BINARY"],
    ids=("hex", "octal", "binary"),
)
@pytest.mark.parametrize(
    argnames="value",
    argvalues=[-(1 << 63), 1 << 63],
    ids=("i64-min", "beyond-i64"),
)
def test_base_format_falls_back_to_decimal_at_i64_boundary(
    integer_format_name: str,
    value: int,
) -> None:
    """Avoid converting an unsigned base literal that exceeds
    ``Int64``.
    """
    integer_format = next(
        member
        for member in Julia.integer_formats
        if member.name == integer_format_name
    )
    result = literalize(
        source=f"{value}",
        input_format=InputFormat.JSON,
        language=Julia(integer_format=integer_format),
    )

    assert result.code == f"{value}"
