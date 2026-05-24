"""Float formatting functions for finite values."""

import math

from beartype import beartype

from literalizer._types import Value


@beartype
def format_float_repr(value: float) -> str:
    """Format a finite float using Python's ``repr``.

    This produces the shortest representation that round-trips:
    ``1500.0`` stays as ``"1500.0"``, ``0.001`` as ``"0.001"``.
    """
    return repr(value)


@beartype
def format_float_scientific(value: float) -> str:
    """Format a finite float in scientific notation.

    Example: ``1500.0`` -> ``"1.5e3"``, ``0.001`` -> ``"1e-3"``.

    Trailing zeros in the coefficient are stripped so the output is
    compact, but a trailing ``.0`` is preserved to keep the value
    recognizable as a float.
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


@beartype
def data_has_float(*, data: Value) -> bool:
    """Return ``True`` if *data* contains a finite ``float`` scalar.

    Descends into lists, sets, and both dict keys and values.  Used by
    languages that need to emit a preamble (e.g. an ``import``)
    conditionally on the presence of any float, such as Perl's
    ``MATH_BIG_FLOAT`` float-format strategy.
    """
    match data:
        case float():
            return math.isfinite(data)
        case list() | set():
            return any(data_has_float(data=v) for v in data)
        case dict():
            return any(
                data_has_float(data=item)
                for entry in data.items()
                for item in entry
            )
        case _:
            return False
