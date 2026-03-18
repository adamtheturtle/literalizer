"""Java language specification."""

from __future__ import annotations

import datetime  # noqa: TC003
from typing import TYPE_CHECKING, Any, Literal

from beartype import beartype

from literalizer._formatters import (
    format_bytes_hex,
    format_date_iso,
    format_date_java,
    format_datetime_iso,
    format_datetime_java_instant,
    format_datetime_java_zoned,
    format_string_backslash,
    passthrough_sequence_entry,
    passthrough_set_entry,
)

if TYPE_CHECKING:
    from collections.abc import Callable

    from literalizer._types import Value


@beartype
def _format_java_dict_entry(key: str, value: str) -> str:
    """Format a Java ``Map.entry(key, value)`` call."""
    return f"Map.entry({key}, {value})"


@beartype
def _format_java_collection_open(values: list[Any]) -> str:
    """Return a typed Java array opener inferred from element types.

    Returns ``"new String[]{"`` when all elements are strings,
    ``"new int[]{"`` when all elements are non-boolean integers, and
    ``"new Object[]{"`` otherwise.
    """
    if values and all(isinstance(v, str) for v in values):
        return "new String[]{"
    if values and all(
        isinstance(v, int) and not isinstance(v, bool) for v in values
    ):
        return "new int[]{"
    return "new Object[]{"


@beartype
def _format_variable_declaration(name: str, value: str) -> str:
    """Format a Java variable declaration."""
    return f"var {name} = {value};"


@beartype
def _format_variable_assignment(name: str, value: str) -> str:
    """Format a Java variable assignment."""
    return f"{name} = {value};"


_date_formats: dict[str, Callable[[datetime.date], str]] = {
    "iso": format_date_iso,
    "java": format_date_java,
}

_datetime_formats: dict[str, Callable[[datetime.datetime], str]] = {
    "iso": format_datetime_iso,
    "instant": format_datetime_java_instant,
    "zoned": format_datetime_java_zoned,
}
_string_format: Callable[[str], str] = format_string_backslash


class Java:
    """Java language specification."""

    def __init__(
        self,
        *,
        date_format: Literal["iso", "java"] = "iso",
        datetime_format: Literal["iso", "instant", "zoned"] = "iso",
    ) -> None:
        """Initialize Java language specification."""
        self.null_literal = "null"
        self.true_literal = "true"
        self.false_literal = "false"
        self.sequence_open = "new Object[]{"
        self.sequence_close = "}"
        self.dict_open = "Map.ofEntries("
        self.dict_close = ")"
        self.format_dict_entry: Callable[[str, str], str] = (
            _format_java_dict_entry
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
        self.empty_sequence: str | None = None
        self.empty_dict: str | None = None
        self.set_open = "Set.of("
        self.set_close = ")"
        self.empty_set: str | None = None
        self.format_sequence_entry: Callable[[str], str] = (
            passthrough_sequence_entry
        )
        self.format_set_entry: Callable[[str], str] = passthrough_set_entry
        self.comment_prefix = "//"
        self.comment_suffix = ""
        self.omap_open = "new java.util.ArrayList<>(java.util.Arrays.asList("
        self.omap_close = "))"
        self.format_omap_entry: Callable[[str, str], str] = (
            _format_java_dict_entry
        )
        self.multiline_close_indent = ""
        self.element_separator = ", "
        self.skip_null_dict_values = True
        self.format_variable_declaration: Callable[[str, str], str] = (
            _format_variable_declaration
        )
        self.format_variable_assignment: Callable[[str, str], str] = (
            _format_variable_assignment
        )
        self.format_collection_open: Callable[[list[Value]], str] | None = (
            _format_java_collection_open
        )
