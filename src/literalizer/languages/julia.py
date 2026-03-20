"""Julia language specification."""

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
    format_date_julia,
    format_datetime_iso,
    format_datetime_julia,
    format_string_backslash,
    passthrough_sequence_entry,
    passthrough_set_entry,
)

if TYPE_CHECKING:
    import datetime
    from collections.abc import Callable

    from literalizer._types import Value


@beartype
def _format_julia_omap_entry(key: str, value: str) -> str:
    """Format a Julia ordered-map entry as a pair arrow expression."""
    return f"{key} => {value}"


@beartype
def _format_variable_declaration(name: str, value: str) -> str:
    """Format a Julia variable declaration."""
    return f"{name} = {value}"


@beartype
class Julia:
    """Julia language specification.

    Args:
        date_format: How to format :class:`datetime.date` values.

            * ``DateFormat.ISO`` (default) — ISO 8601 string,
              e.g. ``"2024-01-15"``.
            * ``DateFormat.JULIA`` — ``Date(...)`` constructor call,
              e.g. ``Date(2024, 1, 15)``.

        datetime_format: How to format :class:`datetime.datetime` values.

            * ``DatetimeFormat.ISO`` (default) — ISO 8601 string,
              e.g. ``"2024-01-15T12:30:00"``.
            * ``DatetimeFormat.JULIA`` — ``DateTime(...)`` constructor
              call, e.g. ``DateTime(2024, 1, 15, 12, 30, 0)``.

        sequence_format: Which Julia sequence type to use.

            * ``SequenceFormat.ARRAY`` (default) — array literal,
              e.g. ``[1, 2, 3]``.
            * ``SequenceFormat.TUPLE`` — tuple literal,
              e.g. ``(1, 2, 3)``.
    """

    class DateFormat(enum.Enum):
        """Date formatting options for Julia."""

        ISO = enum.member(value=format_date_iso)
        JULIA = enum.member(value=format_date_julia)

    class DatetimeFormat(enum.Enum):
        """Datetime formatting options for Julia."""

        ISO = enum.member(value=format_datetime_iso)
        JULIA = enum.member(value=format_datetime_julia)

    class BytesFormat(enum.Enum):
        """Bytes formatting options."""

        HEX = enum.member(value=format_bytes_hex)

    class SequenceFormat(enum.Enum):
        """Sequence type options for Julia."""

        ARRAY = "array"
        TUPLE = "tuple"

    class SetFormat(enum.Enum):
        """Set type options for Julia."""

        SET = "set"

    def __init__(
        self,
        *,
        date_format: DateFormat,
        datetime_format: DatetimeFormat,
        bytes_format: BytesFormat,
        sequence_format: SequenceFormat,
    ) -> None:
        """Initialize Julia language specification."""
        self.sequence_format = sequence_format
        self.null_literal = "nothing"
        self.true_literal = "true"
        self.false_literal = "false"
        self.sequence_open: Callable[[list[Value]], str]
        self.sequence_close: str
        self.single_element_trailing_comma: bool
        if sequence_format == Julia.SequenceFormat.TUPLE:
            self.sequence_open = fixed_sequence_open(open_str="(")
            self.sequence_close = ")"
            self.single_element_trailing_comma = True
        else:
            self.sequence_open = fixed_sequence_open(open_str="[")
            self.sequence_close = "]"
            self.single_element_trailing_comma = False
        self.dict_open: Callable[[dict[str, Value]], str] = fixed_dict_open(
            open_str="Dict("
        )
        self.dict_close = ")"
        self.format_dict_entry: Callable[[str, str], str] = (
            dict_entry_with_separator(separator=" => ")
        )
        self.multiline_trailing_comma = True
        self.format_bytes: Callable[[bytes], str] = bytes_format.value  # ty: ignore[invalid-assignment]  # pyrefly: ignore[bad-assignment]
        self.format_date: Callable[[datetime.date], str] = date_format.value  # ty: ignore[invalid-assignment]  # pyrefly: ignore[bad-assignment]
        self.format_datetime: Callable[[datetime.datetime], str] = (
            datetime_format.value  # ty: ignore[invalid-assignment]  # pyrefly: ignore[bad-assignment]
        )
        self.format_string: Callable[[str], str] = format_string_backslash
        self.empty_sequence: str | None = None
        self.empty_dict: str | None = "Dict()"
        self.set_open = "Set(["
        self.set_close = "])"
        self.empty_set: str | None = "Set()"
        self.format_sequence_entry: Callable[[str], str] = (
            passthrough_sequence_entry
        )
        self.format_set_entry: Callable[[str], str] = passthrough_set_entry
        self.comment_prefix = "#"
        self.comment_suffix = ""
        self.omap_open = "["
        self.omap_close = "]"
        self.format_omap_entry: Callable[[str, str], str] = (
            _format_julia_omap_entry
        )
        self.multiline_close_indent = ""
        self.element_separator = ", "
        self.skip_null_dict_values = False
        self.coerce_heterogeneous_to_strings = False
        self.coerce_heterogeneous_lists_to_strings = False
        self.supports_collection_comments = True
        self.format_variable_declaration: Callable[[str, str], str] = (
            _format_variable_declaration
        )
        self.format_variable_assignment: Callable[[str, str], str] = (
            _format_variable_declaration
        )
