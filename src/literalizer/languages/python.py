"""Python language specification."""

from __future__ import annotations

import enum
from typing import TYPE_CHECKING

from beartype import beartype

from literalizer._formatters import (
    dict_entry_with_separator,
    fixed_dict_open,
    fixed_sequence_open,
    format_bytes_hex,
    format_bytes_python,
    format_date_iso,
    format_date_python,
    format_datetime_epoch,
    format_datetime_iso,
    format_datetime_python,
    format_string_backslash,
    passthrough_sequence_entry,
    passthrough_set_entry,
)

if TYPE_CHECKING:
    import datetime
    from collections.abc import Callable

    from literalizer._types import Value


@beartype
def _format_python_omap_entry(key: str, value: str) -> str:
    """Format one Python ``OrderedDict`` entry as a ``(key, value)`` tuple."""
    return f"({key}, {value})"


@beartype
def _format_variable_declaration(name: str, value: str) -> str:
    """Format a Python variable declaration."""
    return f"{name} = {value}"


@beartype
def _format_variable_assignment(name: str, value: str) -> str:
    """Format a Python variable assignment."""
    return f"{name} = {value}"


class Python:
    """Python language specification.

    Args:
        date_format: How to format :class:`datetime.date` values.

            * ``DateFormat.ISO`` (default) — ISO 8601 string,
              e.g. ``"2024-01-15"``.
            * ``DateFormat.PYTHON`` — ``datetime.date`` constructor call,
              e.g. ``datetime.date(2024, 1, 15)``.

        datetime_format: How to format :class:`datetime.datetime` values.

            * ``DatetimeFormat.ISO`` (default) — ISO 8601 string,
              e.g. ``"2024-01-15T12:30:00"``.
            * ``DatetimeFormat.PYTHON`` — ``datetime.datetime`` constructor
              call, e.g. ``datetime.datetime(2024, 1, 15, 12, 30, 0)``.
            * ``DatetimeFormat.EPOCH`` — Unix epoch float,
              e.g. ``1705312200.0``.

        bytes_format: How to format :class:`bytes` values.

            * ``BytesFormat.HEX`` (default) — lowercase hex string,
              e.g. ``"48656c6c6f"``.
            * ``BytesFormat.PYTHON`` — Python bytes literal,
              e.g. ``b'Hello'``.
    """

    class DateFormat(enum.Enum):
        """Date formatting options for Python."""

        ISO = enum.member(value=format_date_iso)
        PYTHON = enum.member(value=format_date_python)

    class DatetimeFormat(enum.Enum):
        """Datetime formatting options for Python."""

        ISO = enum.member(value=format_datetime_iso)
        PYTHON = enum.member(value=format_datetime_python)
        EPOCH = enum.member(value=format_datetime_epoch)

    class BytesFormat(enum.Enum):
        """Bytes formatting options for Python."""

        HEX = enum.member(value=format_bytes_hex)
        PYTHON = enum.member(value=format_bytes_python)

    @beartype
    def __init__(
        self,
        *,
        date_format: DateFormat = DateFormat.ISO,
        datetime_format: DatetimeFormat = DatetimeFormat.ISO,
        bytes_format: BytesFormat = BytesFormat.HEX,
    ) -> None:
        """Initialize Python language specification."""
        self.null_literal = "None"
        self.true_literal = "True"
        self.false_literal = "False"
        self.sequence_open: Callable[[list[Value]], str] = fixed_sequence_open(
            open_str="("
        )
        self.sequence_close = ")"
        self.dict_open: Callable[[dict[str, Value]], str] = fixed_dict_open(
            open_str="{"
        )
        self.dict_close = "}"
        self.format_dict_entry: Callable[[str, str], str] = (
            dict_entry_with_separator(separator=": ")
        )
        self.multiline_trailing_comma = True
        self.single_element_trailing_comma = True

        self.format_bytes: Callable[[bytes], str] = bytes_format.value  # ty: ignore[invalid-assignment]
        self.format_date: Callable[[datetime.date], str] = date_format.value  # ty: ignore[invalid-assignment]
        self.format_datetime: Callable[[datetime.datetime], str] = (
            datetime_format.value  # ty: ignore[invalid-assignment]
        )

        self.format_string: Callable[[str], str] = format_string_backslash
        self.empty_sequence: str | None = None
        self.empty_dict: str | None = None
        self.set_open = "{"
        self.set_close = "}"
        self.empty_set: str | None = "set()"
        self.format_sequence_entry: Callable[[str], str] = (
            passthrough_sequence_entry
        )
        self.format_set_entry: Callable[[str], str] = passthrough_set_entry
        self.comment_prefix = "#"
        self.comment_suffix = ""
        self.omap_open = "OrderedDict(["
        self.omap_close = "])"
        self.format_omap_entry: Callable[[str, str], str] = (
            _format_python_omap_entry
        )
        self.multiline_close_indent = ""
        self.element_separator = ", "
        self.skip_null_dict_values = False
        self.format_variable_declaration: Callable[[str, str], str] = (
            _format_variable_declaration
        )
        self.format_variable_assignment: Callable[[str, str], str] = (
            _format_variable_assignment
        )
