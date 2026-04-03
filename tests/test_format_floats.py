"""Tests for float formatting functions."""

import math

from literalizer._formatters.format_floats import format_float_scientific
from literalizer.languages.elm import (
    _format_elm_float_repr,  # pyright: ignore[reportPrivateUsage]
)


def test_scientific_inf() -> None:
    """Inf uses the provided inf_literal."""
    assert (
        format_float_scientific(
            value=math.inf,
            inf_literal="inf",
            neg_inf_literal="-inf",
            nan_literal="nan",
        )
        == "inf"
    )


def test_scientific_negative_inf() -> None:
    """Negative inf uses the provided neg_inf_literal."""
    assert (
        format_float_scientific(
            value=-math.inf,
            inf_literal="inf",
            neg_inf_literal="-inf",
            nan_literal="nan",
        )
        == "-inf"
    )


def test_scientific_nan() -> None:
    """NaN uses the provided nan_literal."""
    assert (
        format_float_scientific(
            value=math.nan,
            inf_literal="inf",
            neg_inf_literal="-inf",
            nan_literal="nan",
        )
        == "nan"
    )


def test_elm_float_negative() -> None:
    """Negative floats are parenthesized in Elm."""
    assert _format_elm_float_repr(-3.14) == "EFloat (-3.14)"


def test_elm_float_positive() -> None:
    """Positive floats are not parenthesized in Elm."""
    assert _format_elm_float_repr(3.14) == "EFloat 3.14"
