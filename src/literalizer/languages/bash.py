"""Bash language specification."""

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
    passthrough_set_entry,
)
from literalizer._language import HasFormatEnums

if TYPE_CHECKING:
    import datetime
    from collections.abc import Callable

    from literalizer._types import Value


@beartype
def _to_bash_value(item: str) -> str:
    """Quote an item if it is a nested array or dict expression.

    Bash does not support nested array literals, so any value that is
    itself an array or associative-array expression (starting with
    ``(``) is double-quoted with special characters escaped.
    """
    if item.startswith("("):
        escaped = (
            item.replace("\\", "\\\\")
            .replace('"', '\\"')
            .replace("$", "\\$")
            .replace("`", "\\`")
        )
        return f'"{escaped}"'
    return item


@beartype
def _format_bash_sequence_entry(item: str) -> str:
    """Format a Bash indexed-array element, quoting nested collections."""
    return _to_bash_value(item=item)


@beartype
def _format_bash_dict_entry(key: str, value: str) -> str:
    """Format a Bash associative-array entry as ``[key]=value``."""
    return f"[{key}]={_to_bash_value(item=value)}"


@beartype
def _format_variable_declaration(name: str, value: str) -> str:
    """Format a Bash ``declare`` variable declaration."""
    flag = (
        " -A"
        if any(line.lstrip().startswith("[") for line in value.splitlines())
        else ""
    )
    return f"declare{flag} {name}={value}"


@beartype
def _format_variable_assignment(name: str, value: str) -> str:
    """Format a Bash variable assignment."""
    return f"{name}={value}"


_string_format: Callable[[str], str] = format_string_backslash


@beartype
class Bash(metaclass=HasFormatEnums):
    """Bash language specification."""

    class DateFormats(enum.Enum):
        """Date format options for Bash."""

        ISO = enum.member(value=format_date_iso)

        def __call__(self, date_value: datetime.date, /) -> str:
            """Format a date."""
            return self.value(value=date_value)

    class DatetimeFormats(enum.Enum):
        """Datetime format options for Bash."""

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
        """Sequence type options for Bash."""

        ARRAY = "array"

    class SetFormats(enum.Enum):
        """Set type options for Bash."""

        SET = "set"

    date_formats = DateFormats
    datetime_formats = DatetimeFormats
    bytes_formats = BytesFormats
    sequence_formats = SequenceFormats
    set_formats = SetFormats

    def __init__(
        self,
        *,
        date_format: DateFormats,
        datetime_format: DatetimeFormats,
        bytes_format: BytesFormats,
        sequence_format: SequenceFormats,
    ) -> None:
        """Initialize Bash language specification."""
        self.sequence_format = sequence_format
        self.null_literal = '""'
        self.true_literal = "true"
        self.false_literal = "false"
        self.sequence_open: Callable[[list[Value]], str] = fixed_sequence_open(
            open_str="("
        )
        self.sequence_close = ")"
        self.dict_open: Callable[[dict[str, Value]], str] = fixed_dict_open(
            open_str="("
        )
        self.dict_close = ")"
        self.format_dict_entry: Callable[[str, str], str] = (
            _format_bash_dict_entry
        )
        self.multiline_trailing_comma = False
        self.single_element_trailing_comma = False
        self.format_bytes: Callable[[bytes], str] = bytes_format
        self.format_date: Callable[[datetime.date], str] = date_format
        self.format_datetime: Callable[[datetime.datetime], str] = (
            datetime_format
        )
        self.format_string: Callable[[str], str] = _string_format
        self.empty_sequence: str | None = None
        self.empty_dict: str | None = None
        self.set_open = "("
        self.set_close = ")"
        self.empty_set: str | None = None
        self.format_sequence_entry: Callable[[str], str] = (
            _format_bash_sequence_entry
        )
        self.format_set_entry: Callable[[str], str] = passthrough_set_entry
        self.comment_prefix = "#"
        self.comment_suffix = ""
        self.omap_open = "("
        self.omap_close = ")"
        self.format_omap_entry: Callable[[str, str], str] = (
            _format_bash_dict_entry
        )
        self.multiline_close_indent = ""
        self.element_separator = " "
        self.skip_null_dict_values = False
        self.coerce_heterogeneous_scalars_to_strings = False
        self.coerce_heterogeneous_collection_values_to_strings = False
        self.supports_collection_comments = True
        self.format_variable_declaration: Callable[[str, str], str] = (
            _format_variable_declaration
        )
        self.format_variable_assignment: Callable[[str, str], str] = (
            _format_variable_assignment
        )
