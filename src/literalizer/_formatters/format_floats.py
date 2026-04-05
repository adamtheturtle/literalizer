"""Float formatting functions."""

import math

from beartype import beartype


@beartype
def format_float_repr(
    value: float,
    *,
    inf_literal: str,
    neg_inf_literal: str,
    nan_literal: str,
) -> str:
    """Format a float using Python's ``repr``.

    This produces the shortest representation that round-trips:
    ``1500.0`` stays as ``"1500.0"``, ``0.001`` as ``"0.001"``.

    Special values (inf, -inf, nan) use the provided literals.
    """
    if math.isinf(value):
        return neg_inf_literal if value < 0 else inf_literal
    if math.isnan(value):
        return nan_literal
    return repr(value)


@beartype
def format_float_scientific(
    value: float,
    *,
    inf_literal: str,
    neg_inf_literal: str,
    nan_literal: str,
) -> str:
    """Format a float in scientific notation.

    Example: ``1500.0`` -> ``"1.5e3"``, ``0.001`` -> ``"1e-3"``.

    Special values (inf, -inf, nan) use the provided literals.
    Trailing zeros in the coefficient are stripped so the output is
    compact, but a trailing ``.0`` is preserved to keep the value
    recognizable as a float.
    """
    # inf, -inf, nan do not have an "e" component.
    if math.isinf(value):
        return neg_inf_literal if value < 0 else inf_literal
    if math.isnan(value):
        return nan_literal
    raw = f"{value:e}"
    mantissa, exponent_part = raw.split(sep="e")
    # Strip trailing zeros but keep at least one decimal digit.
    mantissa = mantissa.rstrip("0")
    if mantissa.endswith("."):
        mantissa += "0"
    exponent_value = int(exponent_part)
    if exponent_value == 0:
        return mantissa
    return f"{mantissa}e{exponent_value}"


@beartype
def format_float_fixed(
    value: float,
    *,
    inf_literal: str,
    neg_inf_literal: str,
    nan_literal: str,
) -> str:
    """Format a float in fixed-point notation (``%f``).

    Example: ``1500.0`` -> ``"1500.000000"``, ``0.001`` -> ``"0.001000"``.
    """
    if math.isinf(value):
        return neg_inf_literal if value < 0 else inf_literal
    if math.isnan(value):
        return nan_literal
    return f"{value:f}"
