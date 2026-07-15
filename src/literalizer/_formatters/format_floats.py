"""Float formatting functions for finite values."""

import math

from beartype import beartype

from literalizer._types import OrderedMap, Value


@beartype
def data_has_special_float(*, data: Value) -> bool:
    """Return whether *data* contains NaN or an infinity."""
    match data:
        case float():
            return not math.isfinite(data)
        case OrderedMap() | dict():
            return any(
                data_has_special_float(data=value) for value in data.values()
            )
        case list() | set():
            return any(data_has_special_float(data=value) for value in data)
        case _:
            return False


@beartype
def format_float_repr(value: float) -> str:
    """Format a finite float using Python's ``repr``.

    This produces the shortest representation that round-trips:
    ``1500.0`` stays as ``"1500.0"``, ``0.001`` as ``"0.001"``.

    When ``repr`` emits scientific notation without a dotted mantissa
    (``1e+16``), a ``.0`` is inserted so the result reads ``1.0e+16``.
    Several languages -- Ada, Cobol, Elixir, Erlang, Gleam, Nix, YAML
    -- require a ``.`` in the mantissa to parse a numeric literal as a
    float rather than as an integer, identifier, or string.  The
    redundant ``+`` on positive exponents is kept because YAML's
    resolver regex requires it to recognize the literal as a float;
    languages that reject the ``+`` (currently only Gleam) override
    :meth:`format_float` to strip it.
    """
    raw = repr(value)
    if "e" in raw:
        mantissa, _, exponent = raw.partition("e")
        if "." not in mantissa:
            return f"{mantissa}.0e{exponent}"
    return raw


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
