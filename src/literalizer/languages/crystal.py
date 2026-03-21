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
from literalizer._language import HasFormatEnums

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
class Crystal(metaclass=HasFormatEnums):
    """Crystal language specification.

    Args:
        sequence_format: Which Crystal sequence type to use.

            * ``sequence_formats.ARRAY`` — array literal,
              e.g. ``[1, 2, 3]``.
            * ``sequence_formats.TUPLE`` — tuple literal,
              e.g. ``{1, 2, 3}``.
    """

    class DateFormats(enum.Enum):
        """Date format options for Crystal."""

        ISO = enum.member(value=format_date_iso)

        def __call__(self, date_value: datetime.date, /) -> str:
            """Format a date."""
            return self.value(value=date_value)

    class DatetimeFormats(enum.Enum):
        """Datetime format options for Crystal."""

        ISO = enum.member(value=format_datetime_iso)

        def __call__(self, dt_value: datetime.datetime, /) -> str:
            """Format a datetime."""
            return self.value(value=dt_value)

    class BytesFormats(enum.Enum):
        """Bytes formatting options."""

        HEX = enum.member(value=format_bytes_hex)

        def __call__(self, data: bytes, /) -> str:
            """Format bytes."""
            return self.value(value=data)

    class SequenceFormats(enum.Enum):
        """Sequence type options for Crystal."""

        ARRAY = "array"
        TUPLE = "tuple"

    class SetFormats(enum.Enum):
        """Set type options for Crystal."""

        SET = "set"

    date_formats = DateFormats
    datetime_formats = DatetimeFormats
    bytes_formats = BytesFormats
    sequence_formats = SequenceFormats
    set_formats = SetFormats

    def __init__(
        self,
        *,
        date_format: DateFormats = DateFormats.ISO,
        datetime_format: DatetimeFormats = DatetimeFormats.ISO,
        bytes_format: BytesFormats = BytesFormats.HEX,
        sequence_format: SequenceFormats = SequenceFormats.ARRAY,
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
        self.format_bytes: Callable[[bytes], str] = bytes_format
        self.format_date: Callable[[datetime.date], str] = date_format
        self.format_datetime: Callable[[datetime.datetime], str] = (
            datetime_format
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
        self.coerce_heterogeneous_dict_values_to_strings = False
        self.coerce_heterogeneous_list_values_to_strings = False
        self.supports_collection_comments = True
        self.format_variable_declaration: Callable[[str, str], str] = (
            _format_variable_declaration
        )
        self.format_variable_assignment: Callable[[str, str], str] = (
            _format_variable_assignment
        )
