"""Lua language specification."""

from __future__ import annotations

import enum
from typing import TYPE_CHECKING

from beartype import beartype

from literalizer._formatters import (
    fixed_dict_open,
    fixed_sequence_open,
    format_bytes_hex,
    format_date_iso,
    format_datetime_iso,
    format_string_backslash,
    passthrough_sequence_entry,
)
from literalizer._language import FormatEnum

if TYPE_CHECKING:
    import datetime
    from collections.abc import Callable

    from literalizer._types import Value


@beartype
def _format_lua_dict_entry(key: str, value: str) -> str:
    """Format a Lua table entry with a string key.

    Example: ``'"name"'`` and ``'"Alice"'`` → ``'["name"] = "Alice"'``.
    """
    return f"[{key}] = {value}"


@beartype
def _format_lua_set_entry(item: str) -> str:
    """Format a Lua set entry as a table key with a ``true`` value.

    Example: ``'"apple"'`` → ``'["apple"] = true'``.
    """
    return f"[{item}] = true"


@beartype
def _format_variable_declaration(name: str, value: str) -> str:
    """Format a Lua variable declaration."""
    return f"local {name} = {value}"


@beartype
def _format_variable_assignment(name: str, value: str) -> str:
    """Format a Lua variable assignment."""
    return f"{name} = {value}"


_string_format: Callable[[str], str] = format_string_backslash


@beartype
class Lua:
    """Lua language specification."""

    class DateFormat(enum.Enum):
        """Date format options for Lua."""

        ISO = enum.member(value=format_date_iso)

    class DatetimeFormat(enum.Enum):
        """Datetime format options for Lua."""

        ISO = enum.member(value=format_datetime_iso)

    class BytesFormat(enum.Enum):
        """Bytes formatting options."""

        HEX = enum.member(value=format_bytes_hex)

    class SequenceFormat(enum.Enum):
        """Sequence type options for Lua."""

        TABLE = "table"

    class SetFormat(enum.Enum):
        """Set type options for Lua."""

        SET = "set"

    bytes_formats = FormatEnum(name="BytesFormat")

    set_formats = FormatEnum(name="SetFormat")

    date_formats = FormatEnum(name="DateFormat")

    datetime_formats = FormatEnum(name="DatetimeFormat")

    sequence_formats = FormatEnum(name="SequenceFormat")

    def __init__(
        self,
        *,
        date_format: DateFormat,
        datetime_format: DatetimeFormat,
        bytes_format: BytesFormat,
        sequence_format: SequenceFormat,
    ) -> None:
        """Initialize Lua language specification."""
        self.sequence_format = sequence_format
        self.null_literal = "nil"
        self.true_literal = "true"
        self.false_literal = "false"
        self.sequence_open: Callable[[list[Value]], str] = fixed_sequence_open(
            open_str="{"
        )
        self.sequence_close = "}"
        self.dict_open: Callable[[dict[str, Value]], str] = fixed_dict_open(
            open_str="{"
        )
        self.dict_close = "}"
        self.format_dict_entry: Callable[[str, str], str] = (
            _format_lua_dict_entry
        )
        self.multiline_trailing_comma = True
        self.single_element_trailing_comma = False
        self.format_bytes: Callable[[bytes], str] = bytes_format.value  # ty: ignore[invalid-assignment]  # pyrefly: ignore[bad-assignment]
        self.format_date: Callable[[datetime.date], str] = date_format.value  # ty: ignore[invalid-assignment]  # pyrefly: ignore[bad-assignment]
        self.format_datetime: Callable[[datetime.datetime], str] = (
            datetime_format.value  # ty: ignore[invalid-assignment]  # pyrefly: ignore[bad-assignment]
        )
        self.format_string: Callable[[str], str] = _string_format
        self.empty_sequence: str | None = None
        self.empty_dict: str | None = None
        self.set_open = "{"
        self.set_close = "}"
        self.empty_set: str | None = None
        self.format_sequence_entry: Callable[[str], str] = (
            passthrough_sequence_entry
        )
        self.format_set_entry: Callable[[str], str] = _format_lua_set_entry
        self.comment_prefix = "--"
        self.comment_suffix = ""
        self.omap_open = "{"
        self.omap_close = "}"
        self.format_omap_entry: Callable[[str, str], str] = (
            _format_lua_dict_entry
        )
        self.multiline_close_indent = ""
        self.element_separator = ", "
        self.skip_null_dict_values = True
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
