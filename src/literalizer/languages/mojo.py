"""Mojo language specification."""

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
def _format_mojo_omap_entry(key: str, value: str) -> str:
    """Format one Mojo ordered-map entry as a ``Tuple(key, value)``."""
    return f"Tuple({key}, {value})"


@beartype
def _format_variable_declaration(name: str, value: str) -> str:
    """Format a Mojo variable declaration in Python-compatible script
    style.
    """
    return f"var {name} = {value}"


@beartype
def _format_variable_assignment(name: str, value: str) -> str:
    """Format a Mojo variable assignment."""
    return f"{name} = {value}"


_date_format: Callable[[datetime.date], str] = format_date_iso
_datetime_format: Callable[[datetime.datetime], str] = format_datetime_iso
_string_format: Callable[[str], str] = format_string_backslash


@beartype
class Mojo:
    """Mojo language specification.

    Mojo does not support heterogeneous collections — every element in a
    list or set must share a single type.  When a collection contains
    scalar values of mixed types (e.g. ``[1, 2.5, 3]``), **all values
    are coerced to their string representations** so that the resulting
    literal is valid Mojo (e.g. ``["1", "2.5", "3"]``).

    For sets, this coercion can cause the output to have fewer elements
    than the input when distinct values of different types coerce to the
    same string (e.g. ``{1, "1"}`` both become ``"1"``).
    """

    class BytesFormat(enum.Enum):
        """Bytes formatting options."""

        HEX = enum.member(value=format_bytes_hex)

    class SequenceFormat(enum.Enum):
        """Sequence type options for Mojo."""

        LIST = "list"

    class SetFormat(enum.Enum):
        """Set type options for Mojo."""

        SET = "set"

    @property
    def bytes_formats(self) -> type[BytesFormat]:
        """Enum class whose members list the available bytes formats."""
        return type(self).BytesFormat

    @property
    def set_formats(self) -> type[SetFormat]:
        """Enum class whose members list the available set formats."""
        return type(self).SetFormat

    @property
    def sequence_formats(self) -> type[SequenceFormat]:
        """Enum class whose members list the available sequence
        formats.
        """
        return type(self).SequenceFormat

    def __init__(
        self,
        *,
        bytes_format: BytesFormat,
        sequence_format: SequenceFormat,
    ) -> None:
        """Initialize Mojo language specification."""
        self.sequence_format = sequence_format
        self.null_literal = "None"
        self.true_literal = "True"
        self.false_literal = "False"
        self.sequence_open: Callable[[list[Value]], str] = fixed_sequence_open(
            open_str="["
        )
        self.sequence_close = "]"
        self.dict_open: Callable[[dict[str, Value]], str] = fixed_dict_open(
            open_str="{"
        )
        self.dict_close = "}"
        self.format_dict_entry: Callable[[str, str], str] = (
            dict_entry_with_separator(separator=": ")
        )
        self.multiline_trailing_comma = True
        self.single_element_trailing_comma = False
        self.format_bytes: Callable[[bytes], str] = bytes_format.value  # ty: ignore[invalid-assignment]  # pyrefly: ignore[bad-assignment]
        self.format_date: Callable[[datetime.date], str] = _date_format
        self.format_datetime: Callable[[datetime.datetime], str] = (
            _datetime_format
        )
        self.format_string: Callable[[str], str] = _string_format
        self.empty_sequence: str | None = None
        self.empty_dict: str | None = None
        self.set_open = "["
        self.set_close = "]"
        self.empty_set: str | None = None
        self.format_sequence_entry: Callable[[str], str] = (
            passthrough_sequence_entry
        )
        self.format_set_entry: Callable[[str], str] = passthrough_set_entry
        self.comment_prefix = "#"
        self.comment_suffix = ""
        self.omap_open = "["
        self.omap_close = "]"
        self.format_omap_entry: Callable[[str, str], str] = (
            _format_mojo_omap_entry
        )
        self.multiline_close_indent = ""
        self.element_separator = ", "
        self.skip_null_dict_values = False
        self.coerce_heterogeneous_scalars_to_strings = True
        self.coerce_heterogeneous_sibling_lists_to_strings = True
        self.coerce_heterogeneous_dict_values_to_strings = True
        self.supports_collection_comments = True
        self.format_variable_declaration: Callable[[str, str], str] = (
            _format_variable_declaration
        )
        self.format_variable_assignment: Callable[[str, str], str] = (
            _format_variable_assignment
        )
