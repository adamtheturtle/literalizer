"""Float formatting functions."""

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

    Trailing zeros in the coefficient and a redundant ``.0`` are
    stripped so the output is compact.
    """
    # Use Python's %e which always produces one digit before the
    # decimal point, then clean up.
    raw = f"{value:e}"
    mantissa, exp_part = raw.split("e")
    # Strip trailing zeros from the mantissa.
    mantissa = mantissa.rstrip("0").rstrip(".")
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
