"""OCaml language specification."""

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
    """Convert a value to an OCaml union type expression."""
    _val_prefixes = (
        "ONull",
        "OBool",
        "OList",
        "OMap",
        "OSet",
        "OStr",
        "OInt",
        "OFloat",
    )
    if any(value.startswith(p) for p in _val_prefixes):
        return value
    if value.startswith('"') and value.endswith('"'):
        return f"OStr {value}"
    negative = value.startswith("-")
    rest = value[1:] if negative else value
    int_result = None
    try:
        int(rest)
        int_result = f"OInt ({value})" if negative else f"OInt {value}"
    except ValueError:
        pass
    if int_result is not None:
        return int_result
    float_result = None
    try:
        float(rest)
        float_result = f"OFloat ({value})" if negative else f"OFloat {value}"
    except ValueError:  # pragma: no cover
        pass
    if float_result is not None:
        return float_result
    return value  # pragma: no cover


@beartype
def _format_ocaml_dict_entry(key: str, value: str) -> str:
    """Format an OCaml dict entry as a ``(key, OXxx value)`` tuple."""
    return f"({key}, {_to_val(value=value)})"


@beartype
def _format_ocaml_omap_entry(key: str, value: str) -> str:
    """Format an OCaml ordered-map entry as a ``(key, OXxx value)``
    tuple.
    """
    return f"({key}, {_to_val(value=value)})"


@beartype
def _format_ocaml_set_entry(item: str) -> str:
    """Format an OCaml set entry with the appropriate ``val_t``
    constructor.
    """
    return _to_val(value=item)


@beartype
def _format_ocaml_sequence_entry(item: str) -> str:
    """Format an OCaml list entry with the appropriate ``val_t``
    constructor.
    """
    return _to_val(value=item)


@beartype
def _format_variable_declaration(name: str, value: str) -> str:
    """Format an OCaml variable declaration."""
    return f"let {name} : val_t = {_to_val(value=value)}"


@beartype
def _format_variable_assignment(name: str, value: str) -> str:
    """Format an OCaml variable assignment."""
    return _format_variable_declaration(name=name, value=value)


_bytes_format: Callable[[bytes], str] = format_bytes_hex
_date_format: Callable[[datetime.date], str] = format_date_iso
_datetime_format: Callable[[datetime.datetime], str] = format_datetime_iso
_string_format: Callable[[str], str] = format_string_backslash


@beartype
class OCaml:
    """OCaml language specification."""

    class SequenceFormat(enum.Enum):
        """Sequence type options for OCaml."""

        LIST = "list"

    class SetFormat(enum.Enum):
        """Set type options for OCaml."""

        SET = "set"

    def __init__(
        self,
        *,
        sequence_format: SequenceFormat,
    ) -> None:
        """Initialize OCaml language specification."""
        self.sequence_format = sequence_format
        self.null_literal = "ONull"
        self.true_literal = "OBool true"
        self.false_literal = "OBool false"
        self.sequence_open: Callable[[list[Value]], str] = fixed_sequence_open(
            open_str="OList ["
        )
        self.sequence_close = "]"
        self.dict_open: Callable[[dict[str, Value]], str] = fixed_dict_open(
            open_str="OMap ["
        )
        self.dict_close = "]"
        self.format_dict_entry: Callable[[str, str], str] = (
            _format_ocaml_dict_entry
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
        self.set_open = "OSet ["
        self.set_close = "]"
        self.empty_set: str | None = None
        self.format_set_entry: Callable[[str], str] = _format_ocaml_set_entry
        self.comment_prefix = "(*"
        self.comment_suffix = " *)"
        self.omap_open = "OMap ["
        self.omap_close = "]"
        self.format_omap_entry: Callable[[str, str], str] = (
            _format_ocaml_omap_entry
        )
        self.multiline_close_indent = ""
        self.skip_null_dict_values = False
        self.coerce_heterogeneous_to_strings = False
        self.coerce_heterogeneous_lists_to_strings = False
        self.supports_collection_comments = True
        self.format_variable_declaration: Callable[[str, str], str] = (
            _format_variable_declaration
        )
        self.format_variable_assignment: Callable[[str, str], str] = (
            _format_variable_assignment
        )
        self.element_separator = "; "
        self.format_sequence_entry: Callable[[str], str] = (
            _format_ocaml_sequence_entry
        )
