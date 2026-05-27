"""Float formatting functions for finite values."""

from beartype import beartype


@beartype
def format_float_repr(value: float) -> str:
    """Format a finite float using Python's ``repr``.

    This produces the shortest representation that round-trips:
    ``1500.0`` stays as ``"1500.0"``, ``0.001`` as ``"0.001"``.

    The redundant ``+`` sign Python emits on positive exponents
    (``1e+16``) is stripped to ``1e16``. No target language's literal
    grammar requires the explicit ``+``, and at least one (Gleam's
    Erlang target) rejects it, so the unsigned form is the safe
    common denominator.
    """
    return repr(value).replace("e+", "e")


@beartype
def format_float_scientific(value: float) -> str:
    """Format a finite float in scientific notation.

    Example: ``1500.0`` -> ``"1.5e3"``, ``0.001`` -> ``"1e-3"``.

    Trailing zeros in the coefficient are stripped so the output is
    compact, but a trailing ``.0`` is preserved to keep the value
    recognizable as a float. The redundant ``+`` sign on positive
    exponents is dropped (see :func:`format_float_repr`).
    """
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
def format_float_fixed(value: float) -> str:
    """Format a finite float in fixed-point notation (``%f``).

    Example: ``1500.0`` -> ``"1500.000000"``, ``0.001`` -> ``"0.001000"``.
    """
    return f"{value:f}"
