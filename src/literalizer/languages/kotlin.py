"""Kotlin language specification."""

import datetime
from collections.abc import Callable
from typing import TYPE_CHECKING, Any, Literal

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
)

if TYPE_CHECKING:
    from literalizer._types import Value


@beartype
def _infer_kotlin_element_type(values: list[Any]) -> str | None:
    """Recursively infer the Kotlin element type for a list of values.

    Returns a type string like ``"String"``, ``"Int"``, ``"Array"``,
    or ``None`` when the type cannot be inferred.
    """
    if not values:
        return None
    if all(isinstance(v, str) for v in values):
        return "String"
    if all(isinstance(v, bool) for v in values):
        return "Boolean"
    if all(isinstance(v, int) and not isinstance(v, bool) for v in values):
        return "Int"
    if all(
        isinstance(v, (int, float)) and not isinstance(v, bool) for v in values
    ) and any(isinstance(v, float) for v in values):
        return "Double"
    if all(isinstance(v, list) for v in values):
        inner_types = {_infer_kotlin_element_type(values=v) for v in values}
        if len(inner_types) == 1:
            inner_type = inner_types.pop()
            if inner_type is not None:
                return "Array"
    return None


@beartype
def _format_kotlin_collection_open(values: list[Any]) -> str:
    """Return a typed Kotlin collection opener inferred from element types.

    Returns ``"arrayOf("`` when all elements are strings or nested
    homogeneous arrays, ``"booleanArrayOf("`` when all elements are
    booleans, ``"intArrayOf("`` when all elements are non-boolean integers,
    ``"doubleArrayOf("`` when all elements are non-boolean numeric
    (float, or mixed int and float), and ``"listOf<Any?>("`` otherwise.
    """
    if values and all(isinstance(v, str) for v in values):
        return "arrayOf("
    if values and all(isinstance(v, bool) for v in values):
        return "booleanArrayOf("
    if values and all(
        isinstance(v, int) and not isinstance(v, bool) for v in values
    ):
        return "intArrayOf("
    if (
        values
        and all(
            isinstance(v, (int, float)) and not isinstance(v, bool)
            for v in values
        )
        and any(isinstance(v, float) for v in values)
    ):
        return "doubleArrayOf("
    if values and all(isinstance(v, list) for v in values):
        inner_types = {_infer_kotlin_element_type(values=v) for v in values}
        if len(inner_types) == 1:
            inner_type = inner_types.pop()
            if inner_type is not None:
                return "arrayOf("
    return "listOf<Any?>("


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
        self.sequence_open: Callable[[list[Value]], str] = (
            _format_kotlin_collection_open
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
