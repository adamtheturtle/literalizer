"""Kotlin language specification."""

from __future__ import annotations

import enum
from typing import TYPE_CHECKING, Any

from beartype import beartype

from literalizer._formatters import (
    dict_entry_with_separator,
    format_bytes_hex,
    format_date_kotlin,
    format_datetime_kotlin,
    format_string_backslash_dollar,
    passthrough_sequence_entry,
    passthrough_set_entry,
    typed_dict_open,
    typed_sequence_open,
)

if TYPE_CHECKING:
    import datetime
    from collections.abc import Callable

    from literalizer._types import Value

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


_KOTLIN_SCALAR_TYPES: dict[str, str] = {
    "string": "String",
    "boolean": "Boolean",
    "integer": "Int",
    "number": "Double",
}


@beartype
def _kotlin_schema_to_type(item_schema: dict[str, Any]) -> str | None:
    """Map a JSON Schema item type to a Kotlin type name, recursively."""
    schema_type = item_schema.get("type")
    if isinstance(schema_type, str):
        if schema_type in _KOTLIN_SCALAR_TYPES:
            return _KOTLIN_SCALAR_TYPES[schema_type]
        if schema_type == "array":
            nested = item_schema.get("items", {})
            inner = _kotlin_schema_to_type(item_schema=nested)
            return f"Array<{inner}>" if inner is not None else None
        return None
    return None


@beartype
def _kotlin_dict_schema_to_opener(
    value_schema: dict[str, Any],
) -> str | None:
    """Map a JSON Schema value type to a Kotlin map opener."""
    type_name = _kotlin_schema_to_type(item_schema=value_schema)
    if type_name is None:
        return None
    return f"mapOf<String, {type_name}>("


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


@beartype
class Kotlin:
    """Kotlin language specification.

    Args:
        date_format: How to format :class:`datetime.date` values.

            * ``DateFormat.KOTLIN`` — ``LocalDate.of(...)`` call,
              e.g. ``LocalDate.of(2024, 1, 15)``.

        datetime_format: How to format :class:`datetime.datetime` values.

            * ``DatetimeFormat.KOTLIN`` — ``LocalDateTime.of(...)`` call,
              e.g. ``LocalDateTime.of(2024, 1, 15, 12, 30, 0)``.
    """

    class DateFormat(enum.Enum):
        """Date format options for Kotlin."""

        KOTLIN = enum.member(value=format_date_kotlin)

        def __call__(self, date_value: datetime.date, /) -> str:
            """Format a date."""
            return self.value(value=date_value)

    class DatetimeFormat(enum.Enum):
        """Datetime format options for Kotlin."""

        KOTLIN = enum.member(value=format_datetime_kotlin)

        def __call__(self, dt_value: datetime.datetime, /) -> str:
            """Format a datetime."""
            return self.value(value=dt_value)

    class BytesFormat(enum.Enum):
        """Bytes formatting options."""

        HEX = enum.member(value=format_bytes_hex)

        def __call__(self, data: bytes, /) -> str:
            """Format bytes."""
            return self.value(value=data)

    class SequenceFormat(enum.Enum):
        """Sequence type options for Kotlin."""

        LIST = "list"

    class SetFormat(enum.Enum):
        """Set type options for Kotlin."""

        SET = "set"

    def __init__(
        self,
        *,
        date_format: DateFormat,
        datetime_format: DatetimeFormat,
        bytes_format: BytesFormat,
        sequence_format: SequenceFormat,
    ) -> None:
        """Initialize Kotlin language specification."""
        self.sequence_format = sequence_format
        self.null_literal = "null"
        self.true_literal = "true"
        self.false_literal = "false"
        self.sequence_open: Callable[[list[Value]], str] = typed_sequence_open(
            schema_to_opener=_kotlin_schema_to_opener,
            fallback="listOf<Any?>(",
        )
        self.sequence_close = ")"
        self.dict_open: Callable[[dict[str, Value]], str] = typed_dict_open(
            schema_to_opener=_kotlin_dict_schema_to_opener,
            fallback="mapOf<String, Any?>(",
        )
        self.dict_close = ")"
        self.format_dict_entry: Callable[[str, str], str] = (
            dict_entry_with_separator(separator=" to ")
        )
        self.multiline_trailing_comma = True
        self.single_element_trailing_comma = False
        self.format_bytes: Callable[[bytes], str] = bytes_format
        self.format_date: Callable[[datetime.date], str] = date_format
        self.format_datetime: Callable[[datetime.datetime], str] = (
            datetime_format
        )

        self.format_string: Callable[[str], str] = (
            format_string_backslash_dollar
        )
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
