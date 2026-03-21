"""F# language specification."""

import datetime
import enum
from collections.abc import Callable
from typing import TYPE_CHECKING

from beartype import beartype

from literalizer._formatters import (
    fixed_dict_open,
    fixed_sequence_open,
    format_bytes_hex,
    format_date_iso,
    format_datetime_iso,
    format_string_backslash,
)

if TYPE_CHECKING:
    from literalizer._types import Value


@beartype
def _to_val(value: str) -> str:
    """Convert a value to an F# union type expression."""
    _val_prefixes = (
        "FNull",
        "FBool",
        "FList",
        "FMap",
        "FSet",
        "FStr",
        "FInt",
        "FFloat",
    )
    if any(value.startswith(p) for p in _val_prefixes):
        return value
    if value.startswith('"') and value.endswith('"'):
        return f"FStr {value}"
    negative = value.startswith("-")
    rest = value[1:] if negative else value
    int_result = None
    try:
        int(rest)
        int_result = f"FInt({value}L)" if negative else f"FInt {value}L"
    except ValueError:
        pass
    if int_result is not None:
        return int_result
    float_result = None
    try:
        float(rest)
        float_result = f"FFloat({value})" if negative else f"FFloat {value}"
    except ValueError:  # pragma: no cover
        pass
    if float_result is not None:
        return float_result
    return value  # pragma: no cover


@beartype
def _format_fsharp_dict_entry(key: str, value: str) -> str:
    """Format an F# dict entry as a ``(key, FVal value)`` tuple."""
    return f"({key}, {_to_val(value=value)})"


@beartype
def _format_fsharp_omap_entry(key: str, value: str) -> str:
    """Format an F# ordered-map entry as a ``(key, FVal value)`` tuple."""
    return f"({key}, {_to_val(value=value)})"


@beartype
def _format_fsharp_set_entry(item: str) -> str:
    """Format an F# set entry with the appropriate ``Val`` constructor."""
    return _to_val(value=item)


@beartype
def _format_fsharp_sequence_entry(item: str) -> str:
    """Format an F# sequence entry with the appropriate ``Val``
    constructor.
    """
    return _to_val(value=item)


@beartype
def _format_variable_declaration(name: str, value: str) -> str:
    """Format an F# variable declaration."""
    return f"let {name}: Val = {_to_val(value=value)}"


@beartype
def _format_variable_assignment(name: str, value: str) -> str:
    """Format an F# variable assignment."""
    return f"let {name}: Val = {_to_val(value=value)}"


_date_format: Callable[[datetime.date], str] = format_date_iso
_datetime_format: Callable[[datetime.datetime], str] = format_datetime_iso
_string_format: Callable[[str], str] = format_string_backslash


@beartype
class FSharp:
    """F# language specification."""

    class BytesFormat(enum.Enum):
        """Bytes formatting options."""

        HEX = enum.member(value=format_bytes_hex)

        def __call__(self, data: bytes, /) -> str:
            """Format bytes."""
            return self.value(value=data)

    class SequenceFormat(enum.Enum):
        """Sequence type options for F#."""

        LIST = "list"

    class SetFormat(enum.Enum):
        """Set type options for F#."""

        SET = "set"

    def __init__(
        self,
        *,
        bytes_format: BytesFormat,
        sequence_format: SequenceFormat,
    ) -> None:
        """Initialize FSharp language specification."""
        self.sequence_format = sequence_format
        self.null_literal = "FNull"
        self.true_literal = "FBool true"
        self.false_literal = "FBool false"
        self.sequence_open: Callable[[list[Value]], str] = fixed_sequence_open(
            open_str="FList ["
        )
        self.sequence_close = "]"
        self.dict_open: Callable[[dict[str, Value]], str] = fixed_dict_open(
            open_str="FMap ["
        )
        self.dict_close = "]"
        self.format_dict_entry: Callable[[str, str], str] = (
            _format_fsharp_dict_entry
        )
        self.multiline_trailing_comma = False
        self.single_element_trailing_comma = False
        self.format_bytes: Callable[[bytes], str] = bytes_format
        self.format_date: Callable[[datetime.date], str] = _date_format
        self.format_datetime: Callable[[datetime.datetime], str] = (
            _datetime_format
        )
        self.format_string: Callable[[str], str] = _string_format
        self.empty_sequence: str | None = None
        self.empty_dict: str | None = None
        self.set_open = "FSet ["
        self.set_close = "]"
        self.empty_set: str | None = None
        self.format_set_entry: Callable[[str], str] = _format_fsharp_set_entry
        self.comment_prefix = "//"
        self.comment_suffix = ""
        self.omap_open = "FMap ["
        self.omap_close = "]"
        self.format_omap_entry: Callable[[str, str], str] = (
            _format_fsharp_omap_entry
        )
        self.multiline_close_indent = ""
        self.skip_null_dict_values = False
        self.coerce_heterogeneous_scalars_to_strings = False
        self.coerce_heterogeneous_sibling_lists_to_strings = False
        self.coerce_heterogeneous_dict_values_to_strings = False
        self.supports_collection_comments = True
        self.format_variable_declaration: Callable[[str, str], str] = (
            _format_variable_declaration
        )
        self.format_variable_assignment: Callable[[str, str], str] = (
            _format_variable_assignment
        )
        self.element_separator = "; "
        self.format_sequence_entry: Callable[[str], str] = (
            _format_fsharp_sequence_entry
        )
