"""Go integer-width portability tests."""

import pytest

from literalizer import InputFormat, literalize
from literalizer.languages import Go

_I32_MIN = -(2**31)
_I32_MAX = (2**31) - 1


@pytest.mark.parametrize(
    argnames="value",
    argvalues=[_I32_MIN, _I32_MAX],
)
def test_go_int32_boundaries_use_int(value: int) -> None:
    """Values inside the portable ``int`` range retain that type."""
    result = literalize(
        source=f"[{value}]",
        input_format=InputFormat.JSON,
        language=Go(),
    )

    assert result.code.startswith("[]int{")


@pytest.mark.parametrize(
    argnames="value",
    argvalues=[_I32_MIN - 1, _I32_MAX + 1],
)
def test_go_values_outside_int32_use_int64(value: int) -> None:
    """Values outside signed 32-bit range use a portable type."""
    result = literalize(
        source=f"[{value}]",
        input_format=InputFormat.JSON,
        language=Go(),
    )

    assert result.code.startswith("[]int64{")
