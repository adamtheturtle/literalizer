"""Norg language specification."""

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
    """Format a named Norg code block.

    Uses a heading for the variable name followed by a ranged
    verbatim tag (``@code json`` / ``@end``) for the value.
    """
    return f"* {name}\n@code json\n{value}\n@end"


@beartype
def _format_variable_assignment(name: str, value: str) -> str:
    """Format a named Norg code block.

    Norg has no distinction between declaration and re-assignment;
    this produces the same output as
    :func:`_format_variable_declaration`.
    """
    return f"* {name}\n@code json\n{value}\n@end"


@beartype
class Norg:
    """Norg markup language specification.

    Produces data literals using Norg-compatible syntax — square
    brackets for sequences and sets, curly braces for mappings,
    and ``key: value`` for dict entries.

    Norg comments use the null attached modifier: ``% comment %``.

    Variable declarations use a heading followed by a ranged
    verbatim tag: ``* name`` then ``@code json`` / ``@end``.
    """

    class BytesFormat(enum.Enum):
        """Bytes formatting options."""

        HEX = enum.member(value=format_bytes_hex)

    class SequenceFormat(enum.Enum):
        """Sequence type options for Norg."""

        ARRAY = "array"

    class SetFormat(enum.Enum):
        """Set type options for Norg."""

        SET = "set"

    def __init__(
        self,
        *,
        bytes_format: BytesFormat,
        sequence_format: SequenceFormat,
    ) -> None:
        """Initialize Norg language specification."""
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
        self.multiline_trailing_comma = False
        self.single_element_trailing_comma = False
        self.format_bytes: Callable[[bytes], str] = bytes_format.value  # ty: ignore[invalid-assignment]  # pyrefly: ignore[bad-assignment]
        self.format_date: Callable[[datetime.date], str] = format_date_iso
        self.format_datetime: Callable[[datetime.datetime], str] = (
            format_datetime_iso
        )
        self.format_string: Callable[[str], str] = format_string_backslash
        self.empty_sequence: str | None = None
        self.empty_dict: str | None = None
        self.set_open = "["
        self.set_close = "]"
        self.empty_set: str | None = None
        self.format_sequence_entry: Callable[[str], str] = (
            passthrough_sequence_entry
        )
        self.format_set_entry: Callable[[str], str] = passthrough_set_entry
        self.comment_prefix = "%"
        self.comment_suffix = "%"
        self.omap_open = "{"
        self.omap_close = "}"
        self.format_omap_entry: Callable[[str, str], str] = (
            dict_entry_with_separator(separator=": ")
        )
        self.multiline_close_indent = ""
        self.element_separator = ", "
        self.skip_null_dict_values = False
        self.coerce_heterogeneous_scalars_to_strings = False
        self.coerce_heterogeneous_sibling_lists_to_strings = False
        self.supports_collection_comments = True
        self.format_variable_declaration: Callable[[str, str], str] = (
            _format_variable_declaration
        )
        self.format_variable_assignment: Callable[[str, str], str] = (
            _format_variable_assignment
        )
