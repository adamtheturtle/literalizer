"""JavaScript language specification."""

from __future__ import annotations

import enum
from typing import TYPE_CHECKING

from beartype import beartype

from literalizer._formatters import (
    dict_entry_with_separator,
    fixed_dict_open,
    fixed_sequence_open,
    format_bytes_hex,
    format_date_js,
    format_datetime_js,
    format_string_backslash,
    passthrough_sequence_entry,
    passthrough_set_entry,
)

if TYPE_CHECKING:
    import datetime
    from collections.abc import Callable

    from literalizer._types import Value


@beartype
def _format_js_omap_entry(key: str, value: str) -> str:
    """Format a JavaScript ordered-map entry."""
    return f"{key}: {value}"


@beartype
def _format_variable_declaration(name: str, value: str) -> str:
    """Format a JavaScript variable declaration."""
    return f"const {name} = {value};"


@beartype
def _format_variable_assignment(name: str, value: str) -> str:
    """Format a JavaScript variable assignment."""
    return f"{name} = {value};"


@beartype
class JavaScript:
    """JavaScript language specification.

    Args:
        date_format: How to format :class:`datetime.date` values.

            * ``DateFormat.JS`` — ``new Date(...)`` call,
              e.g. ``new Date("2024-01-15")``.

        datetime_format: How to format :class:`datetime.datetime` values.

            * ``DatetimeFormat.JS`` — ``new Date(...)`` call,
              e.g. ``new Date("2024-01-15T12:30:00")``.
    """

    class DateFormat(enum.Enum):
        """Date formatting options for JavaScript."""

        JS = enum.member(value=format_date_js)

        def __call__(self, date_value: datetime.date, /) -> str:
            """Format a date."""
            return self.value(value=date_value)

    class DatetimeFormat(enum.Enum):
        """Datetime formatting options for JavaScript."""

        JS = enum.member(value=format_datetime_js)

        def __call__(self, dt_value: datetime.datetime, /) -> str:
            """Format a datetime."""
            return self.value(value=dt_value)

    class BytesFormat(enum.Enum):
        """Bytes formatting options."""

        HEX = enum.member(value=format_bytes_hex)

        def __call__(self, data: bytes, /) -> str:
            """Format bytes."""
            return self.value(value=data)

    class SequenceFormat(enum.Enum):
        """Sequence type options for JavaScript."""

        ARRAY = "array"

    class SetFormat(enum.Enum):
        """Set type options for JavaScript."""

        SET = "set"

    def __init__(
        self,
        *,
        date_format: DateFormat,
        datetime_format: DatetimeFormat,
        bytes_format: BytesFormat,
        sequence_format: SequenceFormat,
    ) -> None:
        """Initialize JavaScript language specification."""
        self.sequence_format = sequence_format
        self.null_literal = "null"
        self.true_literal = "true"
        self.false_literal = "false"
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
        self.format_bytes: Callable[[bytes], str] = bytes_format
        self.format_date: Callable[[datetime.date], str] = date_format
        self.format_datetime: Callable[[datetime.datetime], str] = (
            datetime_format
        )

        self.format_string: Callable[[str], str] = format_string_backslash
        self.empty_sequence: str | None = None
        self.empty_dict: str | None = None
        self.set_open = "new Set(["
        self.set_close = "])"
        self.empty_set: str | None = "new Set()"
        self.format_sequence_entry: Callable[[str], str] = (
            passthrough_sequence_entry
        )
        self.format_set_entry: Callable[[str], str] = passthrough_set_entry
        self.comment_prefix = "//"
        self.comment_suffix = ""
        self.omap_open = "{"
        self.omap_close = "}"
        self.format_omap_entry: Callable[[str, str], str] = (
            _format_js_omap_entry
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
