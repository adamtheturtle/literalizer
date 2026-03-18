"""Dart language specification."""

import datetime
from collections.abc import Callable
from typing import Any, Literal

from beartype import beartype

from literalizer._formatters import (
    dict_entry_with_separator,
    format_bytes_hex,
    format_date_dart,
    format_date_iso,
    format_datetime_dart,
    format_datetime_iso,
    format_string_backslash_dollar,
    passthrough_sequence_entry,
    passthrough_set_entry,
    typed_sequence_open,
)
from literalizer._types import Value  # noqa: TC001


@beartype
def _dart_schema_to_opener(item_schema: dict[str, Any]) -> str | None:
    """Map a JSON Schema item type to a Dart list opener."""
    match item_schema.get("type"):
        case "string":
            return "<String>["
        case "boolean":
            return "<bool>["
        case "integer":
            return "<int>["
        case "number":
            return "<double>["
        case list() as types if set(types) == {"integer", "number"}:  # pyright: ignore[reportUnknownVariableType,reportUnknownArgumentType]
            return "<double>["
        case _:
            return None


@beartype
def _format_dart_omap_entry(key: str, value: str) -> str:
    """Format a Dart map entry."""
    return f"{key}: {value}"


@beartype
def _format_variable_declaration(name: str, value: str) -> str:
    """Format a Dart variable declaration."""
    return f"final {name} = {value};"


@beartype
def _format_variable_assignment(name: str, value: str) -> str:
    """Format a Dart variable assignment."""
    return f"{name} = {value};"


_date_formats: dict[str, Callable[[datetime.date], str]] = {
    "iso": format_date_iso,
    "dart": format_date_dart,
}

_datetime_formats: dict[str, Callable[[datetime.datetime], str]] = {
    "iso": format_datetime_iso,
    "dart": format_datetime_dart,
}
_string_format: Callable[[str], str] = format_string_backslash_dollar


class Dart:
    """Dart language specification.

    Args:
        date_format: How to format :class:`datetime.date` values.

            * ``"iso"`` (default) — ISO 8601 string, e.g. ``"2024-01-15"``.
            * ``"dart"`` — ``DateTime.parse(...)`` call,
              e.g. ``DateTime.parse("2024-01-15")``.

        datetime_format: How to format :class:`datetime.datetime` values.

            * ``"iso"`` (default) — ISO 8601 string,
              e.g. ``"2024-01-15T12:30:00"``.
            * ``"dart"`` — ``DateTime.parse(...)`` call,
              e.g. ``DateTime.parse("2024-01-15T12:30:00")``.
    """

    @beartype
    def __init__(
        self,
        *,
        date_format: Literal["iso", "dart"] = "iso",
        datetime_format: Literal["iso", "dart"] = "iso",
    ) -> None:
        """Initialize Dart language specification."""
        self.null_literal = "null"
        self.true_literal = "true"
        self.false_literal = "false"
        self.sequence_open: Callable[[list[Value]], str] = typed_sequence_open(
            schema_to_opener=_dart_schema_to_opener,
            fallback="[",
        )
        self.sequence_close = "]"
        self.dict_open = "{"
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
        self.set_open = "{"
        self.set_close = "}"
        self.empty_set: str | None = "<dynamic>{}"
        self.format_sequence_entry: Callable[[str], str] = (
            passthrough_sequence_entry
        )
        self.format_set_entry: Callable[[str], str] = passthrough_set_entry
        self.comment_prefix = "//"
        self.comment_suffix = ""
        self.omap_open = "{"
        self.omap_close = "}"
        self.format_omap_entry: Callable[[str, str], str] = (
            _format_dart_omap_entry
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
