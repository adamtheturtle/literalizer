"""C# language specification."""

from __future__ import annotations

import datetime  # noqa: TC003
from typing import TYPE_CHECKING, Literal

from beartype import beartype

from literalizer._formatters import (
    format_bytes_hex,
    format_date_csharp,
    format_date_iso,
    format_datetime_csharp,
    format_datetime_iso,
    format_string_backslash,
    passthrough_sequence_entry,
    passthrough_set_entry,
)

if TYPE_CHECKING:
    from collections.abc import Callable


@beartype
def _format_csharp_dict_entry(key: str, value: str) -> str:
    """Format a C# dictionary indexer entry."""
    return f"[{key}] = {value}"


@beartype
def _format_variable_declaration(name: str, value: str) -> str:
    """Format a C# variable declaration."""
    return f"var {name} = {value};"


@beartype
def _format_variable_assignment(name: str, value: str) -> str:
    """Format a C# variable assignment."""
    return f"{name} = {value};"


_date_formats: dict[str, Callable[[datetime.date], str]] = {
    "iso": format_date_iso,
    "csharp": format_date_csharp,
}

_datetime_formats: dict[str, Callable[[datetime.datetime], str]] = {
    "iso": format_datetime_iso,
    "csharp": format_datetime_csharp,
}
_string_format: Callable[[str], str] = format_string_backslash


class CSharp:
    """C# language specification.

    Args:
        date_format: How to format :class:`datetime.date` values.

            * ``"iso"`` (default) — ISO 8601 string, e.g. ``"2024-01-15"``.
            * ``"csharp"`` — ``new DateOnly(...)`` call,
              e.g. ``new DateOnly(2024, 1, 15)``.

        datetime_format: How to format :class:`datetime.datetime` values.

            * ``"iso"`` (default) — ISO 8601 string,
              e.g. ``"2024-01-15T12:30:00"``.
            * ``"csharp"`` — ``new DateTime(...)`` call,
              e.g. ``new DateTime(2024, 1, 15, 12, 30, 0)``.
    """

    @beartype
    def __init__(
        self,
        *,
        date_format: Literal["iso", "csharp"] = "iso",
        datetime_format: Literal["iso", "csharp"] = "iso",
    ) -> None:
        """Initialize CSharp language specification."""
        self.null_literal = "(object?)null"
        self.true_literal = "true"
        self.false_literal = "false"
        self.sequence_open = "("
        self.sequence_close = ")"
        self.dict_open = "new Dictionary<string, object> {"
        self.dict_close = "}"
        self.format_dict_entry: Callable[[str, str], str] = (
            _format_csharp_dict_entry
        )
        self.multiline_trailing_comma = False
        self.single_element_trailing_comma = False
        self.format_bytes: Callable[[bytes], str] = format_bytes_hex
        self.format_date: Callable[[datetime.date], str] = _date_formats[
            date_format
        ]
        self.format_datetime: Callable[[datetime.datetime], str] = (
            _datetime_formats[datetime_format]
        )
        self.format_string: Callable[[str], str] = _string_format
        self.empty_sequence: str | None = "ValueTuple.Create()"
        self.empty_dict: str | None = None
        self.set_open = "new HashSet<object> {"
        self.set_close = "}"
        self.empty_set: str | None = "new HashSet<object>()"
        self.format_sequence_entry: Callable[[str], str] = (
            passthrough_sequence_entry
        )
        self.format_set_entry: Callable[[str], str] = passthrough_set_entry
        self.comment_prefix = "//"
        self.comment_suffix = ""
        self.omap_open = "new Dictionary<string, object> {"
        self.omap_close = "}"
        self.format_omap_entry: Callable[[str, str], str] = (
            _format_csharp_dict_entry
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
