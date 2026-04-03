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


def test_elm_float_negative() -> None:
    """Negative floats are parenthesized in Elm."""
    assert _format_elm_float_repr(-3.14) == "EFloat (-3.14)"


def test_elm_float_positive() -> None:
    """Positive floats are not parenthesized in Elm."""
    assert _format_elm_float_repr(3.14) == "EFloat 3.14"
