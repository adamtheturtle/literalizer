"""Forth float precision regression tests."""

from literalizer import InputFormat, literalize
from literalizer.languages import Forth


def test_forth_subnormal_uses_shortest_round_trip_literal() -> None:
    """A subnormal retains the same binary64 value when parsed again."""
    result = literalize(
        source="[1e-320, 0.1]",
        input_format=InputFormat.JSON,
        language=Forth(),
    )

    assert "1.0e-320 +float" in result.code
    assert "9.999889e-321" not in result.code
