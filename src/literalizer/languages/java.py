"""Java language specification."""

from __future__ import annotations

import enum
from typing import TYPE_CHECKING, Any

from beartype import beartype

from literalizer._formatters import (
    fixed_dict_open,
    format_bytes_hex,
    format_date_iso,
    format_date_java,
    format_datetime_iso,
    format_datetime_java_instant,
    format_datetime_java_zoned,
    format_string_backslash,
    passthrough_sequence_entry,
    passthrough_set_entry,
    typed_sequence_open,
)

if TYPE_CHECKING:
    import datetime
    from collections.abc import Callable

    from literalizer._types import Value


@beartype
def _format_java_dict_entry(key: str, value: str) -> str:
    """Format a Java ``Map.entry(key, value)`` call."""
    return f"Map.entry({key}, {value})"


_JAVA_SCALAR_TYPES: dict[str, str] = {
    "string": "String",
    "boolean": "boolean",
    "integer": "int",
    "number": "double",
}


@beartype
def _java_schema_to_type(item_schema: dict[str, Any]) -> str | None:
    """Map a JSON Schema item type to a Java type name, recursively."""
    schema_type = item_schema.get("type")
    if isinstance(schema_type, str):
        if schema_type in _JAVA_SCALAR_TYPES:
            return _JAVA_SCALAR_TYPES[schema_type]
        if schema_type == "array":
            nested = item_schema.get("items", {})
            inner = _java_schema_to_type(item_schema=nested)
            return f"{inner}[]" if inner is not None else None
        return None
    if (
        isinstance(schema_type, list)
        and set(schema_type) == {"integer", "number"}  # pyright: ignore[reportUnknownArgumentType]
    ):
        return "double"
    return None


@beartype
def _java_schema_to_opener(item_schema: dict[str, Any]) -> str | None:
    """Map a JSON Schema item type to a Java array opener."""
    type_name = _java_schema_to_type(item_schema=item_schema)
    if type_name is None:
        return None
    return f"new {type_name}[]{{"


@beartype
def _format_variable_declaration(name: str, value: str) -> str:
    """Format a Java variable declaration."""
    return f"var {name} = {value};"


@beartype
def _format_variable_assignment(name: str, value: str) -> str:
    """Format a Java variable assignment."""
    return f"{name} = {value};"


@beartype
class Java:
    """Java language specification.

    Args:
        date_format: How to format :class:`datetime.date` values.

            * ``DateFormat.ISO`` — ISO 8601 string,
              e.g. ``"2024-01-15"``.
            * ``DateFormat.JAVA`` — ``LocalDate.of(...)`` call,
              e.g. ``LocalDate.of(2024, 1, 15)``.

        datetime_format: How to format :class:`datetime.datetime` values.

            * ``DatetimeFormat.ISO`` — ISO 8601 string,
              e.g. ``"2024-01-15T12:30:00"``.
            * ``DatetimeFormat.INSTANT`` — ``Instant.parse(...)`` call,
              e.g. ``Instant.parse("2024-01-15T12:30:00")``.
            * ``DatetimeFormat.ZONED`` — ``ZonedDateTime.of(...)`` call,
              e.g. ``ZonedDateTime.of(2024, 1, 15, 12, 30, 0, 0,
              ZoneId.of("UTC"))``.
    """

    class DateFormat(enum.Enum):
        """Date formatting options for Java."""

        ISO = enum.member(value=format_date_iso)
        JAVA = enum.member(value=format_date_java)

    class DatetimeFormat(enum.Enum):
        """Datetime formatting options for Java."""

        ISO = enum.member(value=format_datetime_iso)
        INSTANT = enum.member(value=format_datetime_java_instant)
        ZONED = enum.member(value=format_datetime_java_zoned)

    class BytesFormat(enum.Enum):
        """Bytes formatting options."""

        HEX = enum.member(value=format_bytes_hex)

    class SequenceFormat(enum.Enum):
        """Sequence type options for Java."""

        ARRAY = "array"

    class SetFormat(enum.Enum):
        """Set type options for Java."""

        SET = "set"

    @property
    def bytes_formats(self) -> type[BytesFormat]:
        """Enum class whose members list the available bytes formats."""
        return type(self).BytesFormat

    @property
    def set_formats(self) -> type[SetFormat]:
        """Enum class whose members list the available set formats."""
        return type(self).SetFormat

    @property
    def date_formats(self) -> type[DateFormat]:
        """Enum class whose members list the available date formats."""
        return type(self).DateFormat

    @property
    def datetime_formats(self) -> type[DatetimeFormat]:
        """Enum class whose members list the available datetime
        formats.
        """
        return type(self).DatetimeFormat

    @property
    def sequence_formats(self) -> type[SequenceFormat]:
        """Enum class whose members list the available sequence
        formats.
        """
        return type(self).SequenceFormat

    def __init__(
        self,
        *,
        date_format: DateFormat,
        datetime_format: DatetimeFormat,
        bytes_format: BytesFormat,
        sequence_format: SequenceFormat,
    ) -> None:
        """Initialize Java language specification."""
        self.sequence_format = sequence_format
        self.null_literal = "null"
        self.true_literal = "true"
        self.false_literal = "false"
        self.sequence_open: Callable[[list[Value]], str] = typed_sequence_open(
            schema_to_opener=_java_schema_to_opener,
            fallback="new Object[]{",
        )
        self.sequence_close = "}"
        self.dict_open: Callable[[dict[str, Value]], str] = fixed_dict_open(
            open_str="Map.ofEntries("
        )
        self.dict_close = ")"
        self.format_dict_entry: Callable[[str, str], str] = (
            _format_java_dict_entry
        )
        self.multiline_trailing_comma = False
        self.single_element_trailing_comma = False
        self.format_bytes: Callable[[bytes], str] = bytes_format.value  # ty: ignore[invalid-assignment]  # pyrefly: ignore[bad-assignment]
        self.format_date: Callable[[datetime.date], str] = date_format.value  # ty: ignore[invalid-assignment]  # pyrefly: ignore[bad-assignment]
        self.format_datetime: Callable[[datetime.datetime], str] = (
            datetime_format.value  # ty: ignore[invalid-assignment]  # pyrefly: ignore[bad-assignment]
        )
        self.format_string: Callable[[str], str] = format_string_backslash
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
