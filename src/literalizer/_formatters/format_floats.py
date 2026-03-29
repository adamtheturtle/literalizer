"""Float formatting functions."""

import math

from beartype import beartype


@beartype
def format_float_repr(value: float) -> str:
    """Format a float using Python's ``repr``.

    This produces the shortest representation that round-trips:
    ``1500.0`` stays as ``"1500.0"``, ``0.001`` as ``"0.001"``.
    """
    return repr(value)


@beartype
def format_float_scientific(value: float) -> str:
    """Format a float in scientific notation.

    Example: ``1500.0`` -> ``"1.5e3"``, ``0.001`` -> ``"1e-3"``.

    Special values (inf, -inf, nan) are returned via ``repr``.
    Trailing zeros in the coefficient are stripped so the output is
    compact, but a trailing ``.0`` is preserved to keep the value
    recognizable as a float.
    """
    # inf, -inf, nan do not have an "e" component.
    if math.isinf(value) or math.isnan(value):
        return repr(value)
    raw = f"{value:e}"
    mantissa, exp_part = raw.split(sep="e")
    # Strip trailing zeros but keep at least one decimal digit.
    mantissa = mantissa.rstrip("0")
    if mantissa.endswith("."):
        mantissa += "0"
    exp_val = int(exp_part)
    if exp_val == 0:
        return mantissa
    return f"{mantissa}e{exp_val}"


@beartype
def format_float_fixed(value: float) -> str:
    """Format a float in fixed-point notation (``%f``).

    Example: ``1500.0`` -> ``"1500.000000"``, ``0.001`` -> ``"0.001000"``.
    """
    return f"{value:f}"
