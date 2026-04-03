"""Tests for float formatting functions."""

import math

from literalizer._formatters.format_floats import format_float_scientific
from literalizer.languages.elm import (
    _format_elm_float_repr,  # pyright: ignore[reportPrivateUsage]
)


def test_scientific_inf() -> None:
    """Inf is returned via repr."""
    assert format_float_scientific(value=math.inf) == "inf"


def test_scientific_negative_inf() -> None:
    """Negative inf is returned via repr."""
    assert format_float_scientific(value=-math.inf) == "-inf"


def test_scientific_nan() -> None:
    """NaN is returned via repr."""
    assert format_float_scientific(value=math.nan) == "nan"


def test_scientific_whole_number() -> None:
    """Whole-number floats preserve trailing .0."""
    assert format_float_scientific(value=0.0) == "0.0"
    assert format_float_scientific(value=1.0) == "1.0"


def test_scientific_large_value() -> None:
    """Large values use scientific notation."""
    assert format_float_scientific(value=1500.0) == "1.5e3"


def test_scientific_small_value() -> None:
    """Small values use scientific notation."""
    assert format_float_scientific(value=0.001) == "1.0e-3"


def test_elm_float_negative() -> None:
    """Negative floats are parenthesized in Elm."""
    assert _format_elm_float_repr(-3.14) == "EFloat (-3.14)"


def test_elm_float_positive() -> None:
    """Positive floats are not parenthesized in Elm."""
    assert _format_elm_float_repr(3.14) == "EFloat 3.14"
