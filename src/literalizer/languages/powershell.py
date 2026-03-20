"""PowerShell language specification."""

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
    passthrough_set_entry,
)

if TYPE_CHECKING:
    from literalizer._types import Value


@beartype
def _format_sequence_entry(item: str) -> str:
    """Prevent nested array flattening with a unary comma prefix.

    In PowerShell ``@()`` collects pipeline output and arrays written to the
    pipeline are automatically unrolled.  Prefixing a nested ``@(…)`` with
    the unary comma operator keeps it as a single array element.

    Example: ``"@(1; 2)"`` → ``",@(1; 2)"``; ``"42"`` → ``"42"``.
    """
    if item.startswith("@("):
        return f",{item}"
    return item


@beartype
def _format_string(value: str) -> str:
    """Format a string using PowerShell back-tick escaping."""
    escaped = (
        value.replace("`", "``")
        .replace("$", "`$")
        .replace('"', '`"')
        .replace("\n", "`n")
        .replace("\t", "`t")
    )
    return f'"{escaped}"'


@beartype
def _format_variable_declaration(name: str, value: str) -> str:
    """Format a PowerShell variable declaration."""
    return f"${name} = {value}"


@beartype
def _format_variable_assignment(name: str, value: str) -> str:
    """Format a PowerShell variable assignment."""
    return f"${name} = {value}"


_date_format: Callable[[datetime.date], str] = format_date_iso
_datetime_format: Callable[[datetime.datetime], str] = format_datetime_iso
_string_format: Callable[[str], str] = _format_string


@beartype
class PowerShell:
    """PowerShell language specification."""

    class BytesFormat(enum.Enum):
        """Bytes formatting options."""

        HEX = enum.member(value=format_bytes_hex)

    class SequenceFormat(enum.Enum):
        """Sequence type options for PowerShell."""

        ARRAY = "array"

    class SetFormat(enum.Enum):
        """Set type options for PowerShell."""

        SET = "set"

    def __init__(
        self,
        *,
        bytes_format: BytesFormat,
        sequence_format: SequenceFormat,
    ) -> None:
        """Initialize PowerShell language specification."""
        self.sequence_format = sequence_format
        self.null_literal = "$null"
        self.true_literal = "$true"
        self.false_literal = "$false"
        self.sequence_open: Callable[[list[Value]], str] = fixed_sequence_open(
            open_str="@("
        )
        self.sequence_close = ")"
        self.dict_open: Callable[[dict[str, Value]], str] = fixed_dict_open(
            open_str="@{"
        )
        self.dict_close = "}"
        self.format_dict_entry: Callable[[str, str], str] = (
            dict_entry_with_separator(separator=" = ")
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
        self.set_open = "@("
        self.set_close = ")"
        self.empty_set: str | None = None
        self.format_sequence_entry: Callable[[str], str] = (
            _format_sequence_entry
        )
        self.format_set_entry: Callable[[str], str] = passthrough_set_entry
        self.comment_prefix = "#"
        self.comment_suffix = ""
        self.omap_open = "[ordered]@{"
        self.omap_close = "}"
        self.format_omap_entry: Callable[[str, str], str] = (
            dict_entry_with_separator(separator=" = ")
        )
        self.multiline_close_indent = ""
        self.element_separator = "; "
        self.skip_null_dict_values = False
        self.coerce_heterogeneous_to_strings = False
        self.coerce_heterogeneous_lists_to_strings = False
        self.supports_collection_comments = True
        self.format_variable_declaration: Callable[[str, str], str] = (
            _format_variable_declaration
        )
        self.format_variable_assignment: Callable[[str, str], str] = (
            _format_variable_assignment
        )
