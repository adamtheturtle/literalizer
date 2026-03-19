"""Kotlin language specification."""

import datetime
from collections.abc import Callable
from typing import Any, Literal

from beartype import beartype

from literalizer._formatters import (
    dict_entry_with_separator,
    format_bytes_hex,
    format_date_iso,
    format_date_kotlin,
    format_datetime_iso,
    format_datetime_kotlin,
    format_string_backslash_dollar,
    passthrough_sequence_entry,
    passthrough_set_entry,
    typed_sequence_open,
)
from literalizer._types import Value  # noqa: TC001

_KOTLIN_SCALAR_OPENERS: dict[str, str] = {
    "string": "arrayOf(",
    "boolean": "booleanArrayOf(",
    "integer": "intArrayOf(",
    "number": "doubleArrayOf(",
}


@beartype
def _kotlin_schema_to_opener(item_schema: dict[str, Any]) -> str | None:
    """Map a JSON Schema item type to a Kotlin collection opener."""
    schema_type = item_schema.get("type")
    if isinstance(schema_type, str):
        if schema_type in _KOTLIN_SCALAR_OPENERS:
            return _KOTLIN_SCALAR_OPENERS[schema_type]
        if schema_type == "array":
            nested = item_schema.get("items", {})
            inner = _kotlin_schema_to_opener(item_schema=nested)
            return "arrayOf(" if inner is not None else None
        return None
    if (
        isinstance(schema_type, list)
        and set(schema_type) == {"integer", "number"}  # pyright: ignore[reportUnknownArgumentType]
    ):
        return "listOf<Any?>("
    return None


@beartype
def _format_kotlin_omap_entry(key: str, value: str) -> str:
    """Format a Kotlin ordered-map entry."""
    return f"{key} to {value}"


@beartype
def _format_variable_declaration(name: str, value: str) -> str:
    """Format a Kotlin variable declaration."""
    return f"val {name} = {value}"


@beartype
def _format_variable_assignment(name: str, value: str) -> str:
    """Format a Kotlin variable assignment."""
    return f"{name} = {value}"


_date_formats: dict[str, Callable[[datetime.date], str]] = {
    "iso": format_date_iso,
    "kotlin": format_date_kotlin,
}

_datetime_formats: dict[str, Callable[[datetime.datetime], str]] = {
    "iso": format_datetime_iso,
    "kotlin": format_datetime_kotlin,
}
_string_format: Callable[[str], str] = format_string_backslash_dollar


class Kotlin:
    """Kotlin language specification.

    Args:
        date_format: How to format :class:`datetime.date` values.

            * ``"iso"`` (default) — ISO 8601 string, e.g. ``"2024-01-15"``.
            * ``"kotlin"`` — ``LocalDate.of(...)`` call,
              e.g. ``LocalDate.of(2024, 1, 15)``.

        datetime_format: How to format :class:`datetime.datetime` values.

            * ``"iso"`` (default) — ISO 8601 string,
              e.g. ``"2024-01-15T12:30:00"``.
            * ``"kotlin"`` — ``LocalDateTime.of(...)`` call,
              e.g. ``LocalDateTime.of(2024, 1, 15, 12, 30, 0)``.
    """

    @beartype
    def __init__(
        self,
        *,
        date_format: Literal["iso", "kotlin"] = "iso",
        datetime_format: Literal["iso", "kotlin"] = "iso",
    ) -> None:
        """Initialize Kotlin language specification."""
        self.null_literal = "null"
        self.true_literal = "true"
        self.false_literal = "false"
        self.sequence_open: Callable[[list[Value]], str] = typed_sequence_open(
            schema_to_opener=_kotlin_schema_to_opener,
            fallback="listOf<Any?>(",
        )
        self.sequence_close = ")"
        self.dict_open = "mapOf<String, Any?>("
        self.dict_close = ")"
        self.format_dict_entry: Callable[[str, str], str] = (
            dict_entry_with_separator(separator=" to ")
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
        self.set_open = "setOf<Any?>("
        self.set_close = ")"
        self.empty_set: str | None = None
        self.format_sequence_entry: Callable[[str], str] = (
            passthrough_sequence_entry
        )
        self.format_set_entry: Callable[[str], str] = passthrough_set_entry
        self.comment_prefix = "//"
        self.comment_suffix = ""
        self.omap_open = "linkedMapOf<String, Any?>("
        self.omap_close = ")"
        self.format_omap_entry: Callable[[str, str], str] = (
            _format_kotlin_omap_entry
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
