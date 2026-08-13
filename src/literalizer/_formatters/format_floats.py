"""Float formatting functions for finite values."""

import math
from collections.abc import Callable
from decimal import Decimal

from beartype import beartype

from literalizer._types import OrderedMap, Value
from literalizer.exceptions import UnrepresentableSpecialFloatError


@beartype
def reject_special_floats(
    *, formatter: Callable[[float], str], language_name: str
) -> Callable[[float], str]:
    """Wrap a finite-float formatter with a clear special-float error."""

    @beartype
    def _format(value: float) -> str:
        """Reject a special float before delegating finite values."""
        if not math.isfinite(value):
            msg = f"{language_name} cannot represent special float {value!r}."
            raise UnrepresentableSpecialFloatError(msg)
        return formatter(value)

    return _format


@beartype
def data_has_special_float(*, data: Value) -> bool:
    """Return whether *data* contains NaN or an infinity.

    The document is walked with an explicit stack, and the walk stops
    at the first special float, so the callers that run this on every
    literalized document do not pay a recursive call per node.
    """
    pending: list[Value] = [data]
    while pending:
        value = pending.pop()
        match value:
            case float():
                if not math.isfinite(value):
                    return True
            case OrderedMap() | dict():
                pending.extend(value.keys())
                pending.extend(value.values())
            case list() | set():
                pending.extend(value)
            case _:
                pass
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
    """Format a finite float in round-tripping fixed-point notation.

    Example: ``1500.0`` -> ``"1500.000000"``, ``1e-9`` -> ``"0.000000001"``.
    """
    six_places = f"{value:f}"
    if float(six_places) == value:
        return six_places
    return format(Decimal(value=repr(value)), "f")
