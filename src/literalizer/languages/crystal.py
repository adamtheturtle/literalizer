"""Crystal language specification."""

from __future__ import annotations

import enum
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
    import datetime
    from collections.abc import Callable

    from literalizer._types import Value


@beartype
def _format_variable_declaration(name: str, value: str) -> str:
    """Format a Crystal variable declaration."""
    return f"{name} = {value}"


@beartype
def _format_variable_assignment(name: str, value: str) -> str:
    """Format a Crystal variable assignment."""
    return f"{name} = {value}"


_string_format: Callable[[str], str] = format_string_backslash


@beartype
class Crystal:
    """Crystal language specification.

    Args:
        sequence_format: Which Crystal sequence type to use.

            * ``sequence_formats.ARRAY`` — array literal,
              e.g. ``[1, 2, 3]``.
            * ``sequence_formats.TUPLE`` — tuple literal,
              e.g. ``{1, 2, 3}``.
    """

    class date_formats(enum.Enum):
        """Date format options for Crystal."""

        ISO = enum.member(value=format_date_iso)

    class datetime_formats(enum.Enum):
        """Datetime format options for Crystal."""

        ISO = enum.member(value=format_datetime_iso)

    class bytes_formats(enum.Enum):
        """Bytes formatting options."""

        HEX = enum.member(value=format_bytes_hex)

    class sequence_formats(enum.Enum):
        """Sequence type options for Crystal."""

        ARRAY = "array"
        TUPLE = "tuple"

    class set_formats(enum.Enum):
        """Set type options for Crystal."""

        SET = "set"

    def __init__(
        self,
        *,
        date_format: date_formats,
        datetime_format: datetime_formats,
        bytes_format: bytes_formats,
        sequence_format: sequence_formats,
    ) -> None:
        """Initialize Crystal language specification."""
        self.sequence_format = sequence_format
        self.null_literal = "nil"
        self.true_literal = "true"
        self.false_literal = "false"
        self.sequence_open: Callable[[list[Value]], str]
        self.sequence_close: str
        self.empty_sequence: str | None
        if sequence_format == Crystal.sequence_formats.TUPLE:
            self.sequence_open = fixed_sequence_open(open_str="{")
            self.sequence_close = "}"
            self.empty_sequence = None
        else:
            self.sequence_open = fixed_sequence_open(open_str="[")
            self.sequence_close = "]"
            self.empty_sequence = "[] of Nil"
        self.dict_open: Callable[[dict[str, Value]], str] = fixed_dict_open(
            open_str="{"
        )
        self.dict_close = "}"
        self.format_dict_entry: Callable[[str, str], str] = (
            dict_entry_with_separator(separator=" => ")
        )
        self.multiline_trailing_comma = True
        self.single_element_trailing_comma = False
        self.format_bytes: Callable[[bytes], str] = bytes_format.value  # ty: ignore[invalid-assignment]  # pyrefly: ignore[bad-assignment]
        self.format_date: Callable[[datetime.date], str] = date_format.value  # ty: ignore[invalid-assignment]  # pyrefly: ignore[bad-assignment]
        self.format_datetime: Callable[[datetime.datetime], str] = (
            datetime_format.value  # ty: ignore[invalid-assignment]  # pyrefly: ignore[bad-assignment]
        )
        self.format_string: Callable[[str], str] = _string_format
        self.empty_dict: str | None = "{} of Nil => Nil"
        self.set_open = "Set{"
        self.set_close = "}"
        self.empty_set: str | None = "Set(Nil).new"
        self.format_sequence_entry: Callable[[str], str] = (
            passthrough_sequence_entry
        )
        self.format_set_entry: Callable[[str], str] = passthrough_set_entry
        self.comment_prefix = "#"
        self.comment_suffix = ""
        self.omap_open = "{"
        self.omap_close = "}"
        self.format_omap_entry: Callable[[str, str], str] = (
            dict_entry_with_separator(separator=" => ")
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
