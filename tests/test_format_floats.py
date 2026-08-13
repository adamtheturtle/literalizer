"""Tests for float formatting helpers."""

from literalizer._formatters.format_floats import format_float_scientific


def test_scientific_float_preserves_round_trip_precision() -> None:
    """Scientific notation parses back to the original binary float."""
    value = 3.141592653589793
    formatted = format_float_scientific(value=value)
    assert formatted == "3.141592653589793"
    assert float(formatted) == value


def test_scientific_float_preserves_large_round_trip_precision() -> None:
    """Large coefficients retain all significant decimal digits."""
    value = 1234567890.123
    formatted = format_float_scientific(value=value)
    assert formatted == "1.234567890123e9"
    assert float(formatted) == value


def test_scientific_float_preserves_signed_zero() -> None:
    """Zero keeps a float marker and its sign."""
    assert format_float_scientific(value=0.0) == "0.0"
    assert format_float_scientific(value=-0.0) == "-0.0"
