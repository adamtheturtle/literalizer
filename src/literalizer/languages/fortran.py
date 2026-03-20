"""Fortran language specification."""

import datetime
from collections.abc import Callable
from typing import TYPE_CHECKING

from beartype import beartype

from literalizer._formatters import (
    fixed_dict_open,
    fixed_sequence_open,
    format_bytes_hex,
    format_date_iso,
    format_datetime_iso,
    format_string_fortran,
)

if TYPE_CHECKING:
    from literalizer._types import Value

_FVAL_PREFIXES = (
    "fnull()",
    "fbool(",
    "fint(",
    "freal(",
    "fstr(",
    "flist(",
    "fmap(",
    "fset(",
    "fentry(",
)


@beartype
def _to_fval(value: str) -> str:
    """Convert a pre-formatted value string to an ``fval_t`` constructor.

    Inspects the string representation to determine the appropriate
    constructor: ``fstr``, ``fint``, ``freal``, or passes through values
    that are already ``fval_t`` expressions (``fnull``, ``fbool``,
    ``flist``, ``fmap``, ``fset``, ``fentry``).
    """
    if any(value.startswith(p) for p in _FVAL_PREFIXES):
        return value
    if (value.startswith("'") and value.endswith("'")) or (
        value.startswith('"') and value.endswith('"')
    ):
        return f"fstr({value})"
    negative = value.startswith("-")
    rest = value[1:] if negative else value
    int_result = None
    try:
        int(rest)
        int_result = f"fint({value})"
    except ValueError:
        pass
    if int_result is not None:
        return int_result
    float_result = None
    try:
        float(rest)
        float_result = f"freal({value})"
    except ValueError:  # pragma: no cover
        pass
    if float_result is not None:
        return float_result
    return value  # pragma: no cover


def _fortran_comment_pos(line: str) -> int | None:
    """Return the index of the ``!`` comment character in *line* that
    lies outside any string literal, or ``None`` if there is no comment.
    """
    in_single_quote = False
    in_double_quote = False
    i = 0
    while i < len(line):
        c = line[i]
        if c == "'" and not in_double_quote:
            if in_single_quote and i + 1 < len(line) and line[i + 1] == "'":
                i += 2
                continue
            in_single_quote = not in_single_quote
        elif c == '"' and not in_single_quote:
            in_double_quote = not in_double_quote
        elif c == "!" and not in_single_quote and not in_double_quote:
            return i
        i += 1
    return None


@beartype
def _add_continuation(value: str) -> str:
    """Add Fortran ``&`` line-continuation to non-comment, non-last
    lines.

    In Fortran free-form source a logical line may span multiple physical
    lines.  The ``&`` continuation character must be the last
    non-whitespace, non-comment character on the physical line.  Pure
    comment lines (blank or starting with ``!``) are transparent to the
    continuation mechanism and receive no ``&``.
    """
    lines = value.splitlines()
    if len(lines) <= 1:
        return value
    result: list[str] = []
    for i, line in enumerate(iterable=lines):
        is_last = i == len(lines) - 1
        stripped = line.strip()
        is_pure_comment = not stripped or stripped.startswith("!")
        if is_last or is_pure_comment:
            result.append(line)
        else:
            pos = _fortran_comment_pos(line=line)
            if pos is not None:
                result.append(line[:pos].rstrip() + " &  " + line[pos:])
            else:
                result.append(line + " &")
    return "\n".join(result)


@beartype
def _format_fortran_dict_entry(key: str, value: str) -> str:
    """Format a Fortran dict entry as an ``fentry(key, fval_t value)``
    call.
    """
    return f"fentry({key}, {_to_fval(value=value)})"


@beartype
def _format_variable_declaration(name: str, value: str) -> str:
    r"""Format a Fortran variable declaration and initialisation.

    Example: ``"x"`` and ``"flist([fval_t :: fint(1)])"`` →
    ``"type(fval_t) :: x\nx = flist([fval_t :: fint(1)])"``
    """
    fval = _to_fval(value=value)
    continued = _add_continuation(value=fval)
    return f"type(fval_t) :: {name}\n{name} = {continued}"


@beartype
def _format_variable_assignment(name: str, value: str) -> str:
    """Format a Fortran assignment to an existing ``fval_t`` variable.

    Example: ``"x"`` and ``"flist([fval_t :: fint(1)])"`` →
    ``"x = flist([fval_t :: fint(1)])"``
    """
    fval = _to_fval(value=value)
    continued = _add_continuation(value=fval)
    return f"{name} = {continued}"


_bytes_format: Callable[[bytes], str] = format_bytes_hex
_date_format: Callable[[datetime.date], str] = format_date_iso
_datetime_format: Callable[[datetime.datetime], str] = format_datetime_iso
_string_format: Callable[[str], str] = format_string_fortran


class Fortran:
    """Fortran language specification."""

    @beartype
    def __init__(self) -> None:
        """Initialize Fortran language specification."""
        self.null_literal = "fnull()"
        self.true_literal = "fbool(.true.)"
        self.false_literal = "fbool(.false.)"
        self.sequence_open: Callable[[list[Value]], str] = fixed_sequence_open(
            open_str="flist([fval_t :: "
        )
        self.sequence_close = "])"
        self.dict_open: Callable[[dict[str, Value]], str] = fixed_dict_open(
            open_str="fmap([fval_t :: "
        )
        self.dict_close = "])"
        self.format_dict_entry: Callable[[str, str], str] = (
            _format_fortran_dict_entry
        )
        self.multiline_trailing_comma = False
        self.single_element_trailing_comma = False
        self.format_bytes: Callable[[bytes], str] = _bytes_format
        self.format_date: Callable[[datetime.date], str] = _date_format
        self.format_datetime: Callable[[datetime.datetime], str] = (
            _datetime_format
        )
        self.format_string: Callable[[str], str] = _string_format
        self.empty_sequence: str | None = None
        self.empty_dict: str | None = None
        self.set_open = "fset([fval_t :: "
        self.set_close = "])"
        self.empty_set: str | None = None
        self.format_sequence_entry: Callable[[str], str] = _to_fval
        self.format_set_entry: Callable[[str], str] = _to_fval
        self.comment_prefix = "!"
        self.comment_suffix = ""
        self.omap_open = "fmap([fval_t :: "
        self.omap_close = "])"
        self.format_omap_entry: Callable[[str, str], str] = (
            _format_fortran_dict_entry
        )
        self.multiline_close_indent = ""
        self.element_separator = ", "
        self.skip_null_dict_values = False
        self.coerce_heterogeneous_to_strings = False
        self.supports_collection_comments = True
        self.format_variable_declaration: Callable[[str, str], str] = (
            _format_variable_declaration
        )
        self.format_variable_assignment: Callable[[str, str], str] = (
            _format_variable_assignment
        )
