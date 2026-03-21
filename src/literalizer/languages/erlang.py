"""Erlang language specification."""

import datetime
import enum
from collections.abc import Callable
from typing import TYPE_CHECKING

from beartype import beartype

from literalizer._formatters import (
    dict_entry_with_separator,
    fixed_dict_open,
    fixed_sequence_open,
    format_date_iso,
    format_datetime_iso,
    format_string_backslash,
    passthrough_sequence_entry,
    passthrough_set_entry,
)

if TYPE_CHECKING:
    from literalizer._types import Value


@beartype
def _format_erlang_omap_entry(key: str, value: str) -> str:
    """Format an Erlang ordered-map entry as a ``{key, value}`` tuple."""
    return f"{{{key}, {value}}}"


@beartype
def _format_bytes(value: bytes) -> str:
    """Format bytes as an Erlang binary literal."""
    parts = ", ".join(f"{b}" for b in value)
    return f"<<{parts}>>"


@beartype
def _format_variable_declaration(name: str, value: str) -> str:
    """Format an Erlang variable declaration."""
    erlang_name = name[0].upper() + name[1:]
    return f"{erlang_name} = {value}"


@beartype
def _format_variable_assignment(name: str, value: str) -> str:
    """Format an Erlang variable assignment."""
    erlang_name = name[0].upper() + name[1:]
    return f"{erlang_name} = {value}"


_date_format: Callable[[datetime.date], str] = format_date_iso
_datetime_format: Callable[[datetime.datetime], str] = format_datetime_iso
_string_format: Callable[[str], str] = format_string_backslash


@beartype
class Erlang:
    """Erlang language specification.

    Args:
        sequence_format: Which Erlang sequence type to use.

            * ``SequenceFormat.LIST`` (default) — list literal,
              e.g. ``[1, 2, 3]``.
            * ``SequenceFormat.TUPLE`` — tuple literal,
              e.g. ``{1, 2, 3}``.
    """

    class BytesFormat(enum.Enum):
        """Bytes formatting options."""

        BINARY = enum.member(value=_format_bytes)

    class SequenceFormat(enum.Enum):
        """Sequence type options for Erlang."""

        LIST = "list"
        TUPLE = "tuple"

    class SetFormat(enum.Enum):
        """Set type options for Erlang."""

        SET = "set"

    def __init__(
        self,
        *,
        bytes_format: BytesFormat,
        sequence_format: SequenceFormat,
    ) -> None:
        """Initialize Erlang language specification."""
        self.sequence_format = sequence_format
        self.null_literal = "undefined"
        self.true_literal = "true"
        self.false_literal = "false"
        self.sequence_open: Callable[[list[Value]], str]
        self.sequence_close: str
        if sequence_format == Erlang.SequenceFormat.TUPLE:
            self.sequence_open = fixed_sequence_open(open_str="{")
            self.sequence_close = "}"
        else:
            self.sequence_open = fixed_sequence_open(open_str="[")
            self.sequence_close = "]"
        self.dict_open: Callable[[dict[str, Value]], str] = fixed_dict_open(
            open_str="#{"
        )
        self.dict_close = "}"
        self.format_dict_entry: Callable[[str, str], str] = (
            dict_entry_with_separator(separator=" => ")
        )
        self.multiline_trailing_comma = False
        self.single_element_trailing_comma = False
        self.format_bytes: Callable[[bytes], str] = bytes_format.value  # ty: ignore[invalid-assignment]  # pyrefly: ignore[bad-assignment]
        self.format_date: Callable[[datetime.date], str] = _date_format
        self.format_datetime: Callable[[datetime.datetime], str] = (
            _datetime_format
        )
        self.format_string: Callable[[str], str] = _string_format
        self.empty_sequence: str | None = None
        self.empty_dict: str | None = None
        self.set_open = "sets:from_list(["
        self.set_close = "])"
        self.empty_set: str | None = "sets:from_list([])"
        self.format_sequence_entry: Callable[[str], str] = (
            passthrough_sequence_entry
        )
        self.format_set_entry: Callable[[str], str] = passthrough_set_entry
        self.comment_prefix = "%"
        self.comment_suffix = ""
        self.omap_open = "["
        self.omap_close = "]"
        self.format_omap_entry: Callable[[str, str], str] = (
            _format_erlang_omap_entry
        )
        self.multiline_close_indent = ""
        self.element_separator = ", "
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
