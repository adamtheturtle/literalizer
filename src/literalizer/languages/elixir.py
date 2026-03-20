"""Elixir language specification."""

import datetime
import enum
from collections.abc import Callable
from typing import TYPE_CHECKING

from beartype import beartype

from literalizer._formatters import (
    dict_entry_with_separator,
    fixed_dict_open,
    fixed_sequence_open,
    format_bytes_hex,
    format_date_iso,
    format_datetime_iso,
    format_string_backslash,
    passthrough_sequence_entry,
    passthrough_set_entry,
)

if TYPE_CHECKING:
    from literalizer._types import Value


@beartype
def _format_elixir_omap_entry(key: str, value: str) -> str:
    """Format an Elixir ordered-map entry as a ``{key, value}`` tuple."""
    return f"{{{key}, {value}}}"


@beartype
def _format_variable_declaration(name: str, value: str) -> str:
    """Format an Elixir variable declaration."""
    return f"{name} = {value}"


@beartype
def _format_variable_assignment(name: str, value: str) -> str:
    """Format an Elixir variable assignment."""
    return f"{name} = {value}"


_bytes_format: Callable[[bytes], str] = format_bytes_hex
_date_format: Callable[[datetime.date], str] = format_date_iso
_datetime_format: Callable[[datetime.datetime], str] = format_datetime_iso
_string_format: Callable[[str], str] = format_string_backslash


@beartype
class Elixir:
    """Elixir language specification.

    Args:
        sequence_format: Which Elixir sequence type to use.

            * ``SequenceFormat.LIST`` (default) — list literal,
              e.g. ``[1, 2, 3]``.
            * ``SequenceFormat.TUPLE`` — tuple literal,
              e.g. ``{1, 2, 3}``.
    """

    class SequenceFormat(enum.Enum):
        """Sequence type options for Elixir."""

        LIST = "list"
        TUPLE = "tuple"

    def __init__(
        self,
        *,
        sequence_format: SequenceFormat = SequenceFormat.LIST,
    ) -> None:
        """Initialize Elixir language specification."""
        self.null_literal = "nil"
        self.true_literal = "true"
        self.false_literal = "false"
        self.sequence_open: Callable[[list[Value]], str]
        self.sequence_close: str
        if sequence_format == Elixir.SequenceFormat.TUPLE:
            self.sequence_open = fixed_sequence_open(open_str="{")
            self.sequence_close = "}"
        else:
            self.sequence_open = fixed_sequence_open(open_str="[")
            self.sequence_close = "]"
        self.dict_open: Callable[[dict[str, Value]], str] = fixed_dict_open(
            open_str="%{"
        )
        self.dict_close = "}"
        self.format_dict_entry: Callable[[str, str], str] = (
            dict_entry_with_separator(separator=" => ")
        )
        self.multiline_trailing_comma = True
        self.single_element_trailing_comma = False
        self.format_bytes: Callable[[bytes], str] = _bytes_format
        self.format_date: Callable[[datetime.date], str] = _date_format
        self.format_datetime: Callable[[datetime.datetime], str] = (
            _datetime_format
        )
        self.format_string: Callable[[str], str] = _string_format
        self.empty_sequence: str | None = None
        self.empty_dict: str | None = None
        self.set_open = "MapSet.new(["
        self.set_close = "])"
        self.empty_set: str | None = "MapSet.new()"
        self.format_sequence_entry: Callable[[str], str] = (
            passthrough_sequence_entry
        )
        self.format_set_entry: Callable[[str], str] = passthrough_set_entry
        self.comment_prefix = "#"
        self.comment_suffix = ""
        self.omap_open = "["
        self.omap_close = "]"
        self.format_omap_entry: Callable[[str, str], str] = (
            _format_elixir_omap_entry
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
