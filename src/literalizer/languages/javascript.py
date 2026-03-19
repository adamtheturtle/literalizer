"""JavaScript language specification."""

import datetime
from collections.abc import Callable
from typing import TYPE_CHECKING, Literal

from beartype import beartype

from literalizer._formatters import (
    dict_entry_with_separator,
    fixed_dict_open,
    fixed_sequence_open,
    format_bytes_hex,
    format_date_iso,
    format_date_js,
    format_datetime_iso,
    format_datetime_js,
    format_string_backslash,
    passthrough_sequence_entry,
    passthrough_set_entry,
)

if TYPE_CHECKING:
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


_date_formats: dict[str, Callable[[datetime.date], str]] = {
    "iso": format_date_iso,
    "js": format_date_js,
}

_datetime_formats: dict[str, Callable[[datetime.datetime], str]] = {
    "iso": format_datetime_iso,
    "js": format_datetime_js,
}
_string_format: Callable[[str], str] = format_string_backslash


class JavaScript:
    """JavaScript language specification.

    Args:
        date_format: How to format :class:`datetime.date` values.

            * ``"iso"`` (default) — ISO 8601 string, e.g. ``"2024-01-15"``.
            * ``"js"`` — ``new Date(...)`` call,
              e.g. ``new Date("2024-01-15")``.

        datetime_format: How to format :class:`datetime.datetime` values.

            * ``"iso"`` (default) — ISO 8601 string,
              e.g. ``"2024-01-15T12:30:00"``.
            * ``"js"`` — ``new Date(...)`` call,
              e.g. ``new Date("2024-01-15T12:30:00")``.
    """

    @beartype
    def __init__(
        self,
        *,
        date_format: Literal["iso", "js"] = "iso",
        datetime_format: Literal["iso", "js"] = "iso",
    ) -> None:
        """Initialize JavaScript language specification."""
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
        self.format_bytes: Callable[[bytes], str] = format_bytes_hex
        self.format_date: Callable[[datetime.date], str] = _date_formats[
            date_format
        ]
        self.format_datetime: Callable[[datetime.datetime], str] = (
            _datetime_formats[datetime_format]
        )
        self.format_string: Callable[[str], str] = _string_format
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
        self.format_variable_declaration: Callable[[str, str], str] = (
            _format_variable_declaration
        )
        self.format_variable_assignment: Callable[[str, str], str] = (
            _format_variable_assignment
        )
