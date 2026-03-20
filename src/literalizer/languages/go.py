"""Go language specification."""

from __future__ import annotations

import enum
from typing import TYPE_CHECKING, Any

from beartype import beartype

from literalizer._formatters import (
    dict_entry_with_separator,
    format_bytes_hex,
    format_date_go,
    format_date_iso,
    format_datetime_go,
    format_datetime_iso,
    format_string_backslash,
    passthrough_sequence_entry,
    typed_dict_open,
    typed_sequence_open,
)

if TYPE_CHECKING:
    import datetime
    from collections.abc import Callable

    from literalizer._types import Value

_GO_SCALAR_TYPES: dict[str, str] = {
    "string": "string",
    "boolean": "bool",
    "integer": "int",
    "number": "float64",
}


@beartype
def _go_schema_to_type(item_schema: dict[str, Any]) -> str | None:
    """Map a JSON Schema item type to a Go type name, recursively."""
    schema_type = item_schema.get("type")
    if isinstance(schema_type, str):
        if schema_type in _GO_SCALAR_TYPES:
            return _GO_SCALAR_TYPES[schema_type]
        if schema_type == "array":
            nested = item_schema.get("items", {})
            inner = _go_schema_to_type(item_schema=nested)
            return f"[]{inner}" if inner is not None else None
        return None
    if (
        isinstance(schema_type, list)
        and set(schema_type) == {"integer", "number"}  # pyright: ignore[reportUnknownArgumentType]
    ):
        return "float64"
    return None


@beartype
def _go_schema_to_opener(item_schema: dict[str, Any]) -> str | None:
    """Map a JSON Schema item type to a Go slice opener."""
    type_name = _go_schema_to_type(item_schema=item_schema)
    if type_name is None:
        return None
    return f"[]{type_name}{{"


@beartype
def _go_dict_schema_to_opener(value_schema: dict[str, Any]) -> str | None:
    """Map a JSON Schema value type to a Go map opener."""
    type_name = _go_schema_to_type(item_schema=value_schema)
    if type_name is None:
        return None
    return f"map[string]{type_name}{{"


@beartype
def _format_go_set_entry(item: str) -> str:
    """Format a Go set entry as a map entry with empty struct value.

    Example: ``"apple"`` → ``"apple": struct{}{}``.
    """
    return f"{item}: struct{{}}{{}}"


@beartype
def _format_go_omap_entry(key: str, value: str) -> str:
    """Format a Go ordered-map entry as a ``{key, value}`` pair."""
    return f"{{{key}, {value}}}"


@beartype
def _format_variable_declaration(name: str, value: str) -> str:
    """Format a Go variable declaration."""
    return f"{name} := {value}"


@beartype
def _format_variable_assignment(name: str, value: str) -> str:
    """Format a Go variable assignment."""
    return f"{name} = {value}"


@beartype
class Go:
    """Go language specification.

    Args:
        date_format: How to format :class:`datetime.date` values.

            * ``DateFormat.ISO`` (default) — ISO 8601 string,
              e.g. ``"2024-01-15"``.
            * ``DateFormat.GO`` — ``time.Date`` call,
              e.g. ``time.Date(2024, time.January, 15, 0, 0, 0, 0,
              time.UTC)``.

        datetime_format: How to format :class:`datetime.datetime` values.

            * ``DatetimeFormat.ISO`` (default) — ISO 8601 string,
              e.g. ``"2024-01-15T12:30:00"``.
            * ``DatetimeFormat.GO`` — ``time.Date`` call,
              e.g. ``time.Date(2024, time.January, 15, 12, 30, 0, 0,
              time.UTC)``.
    """

    class DateFormat(enum.Enum):
        """Date format options for Go."""

        ISO = enum.member(value=format_date_iso)
        GO = enum.member(value=format_date_go)

    class DatetimeFormat(enum.Enum):
        """Datetime format options for Go."""

        ISO = enum.member(value=format_datetime_iso)
        GO = enum.member(value=format_datetime_go)

    class BytesFormat(enum.Enum):
        """Bytes formatting options."""

        HEX = enum.member(value=format_bytes_hex)

    class SequenceFormat(enum.Enum):
        """Sequence type options for Go."""

        SLICE = "slice"

    def __init__(
        self,
        *,
        date_format: DateFormat,
        datetime_format: DatetimeFormat,
        bytes_format: BytesFormat,
        sequence_format: SequenceFormat,
    ) -> None:
        """Initialize Go language specification."""
        self.sequence_format = sequence_format
        self.null_literal = "nil"
        self.true_literal = "true"
        self.false_literal = "false"
        self.sequence_open: Callable[[list[Value]], str] = typed_sequence_open(
            schema_to_opener=_go_schema_to_opener,
            fallback="[]any{",
        )
        self.sequence_close = "}"
        self.dict_open: Callable[[dict[str, Value]], str] = typed_dict_open(
            schema_to_opener=_go_dict_schema_to_opener,
            fallback="map[string]any{",
        )
        self.dict_close = "}"
        self.format_dict_entry: Callable[[str, str], str] = (
            dict_entry_with_separator(separator=": ")
        )
        self.multiline_trailing_comma = True
        self.single_element_trailing_comma = False
        self.format_bytes: Callable[[bytes], str] = bytes_format.value  # ty: ignore[invalid-assignment]  # pyrefly: ignore[bad-assignment]
        self.format_date: Callable[[datetime.date], str] = date_format.value  # ty: ignore[invalid-assignment]  # pyrefly: ignore[bad-assignment]
        self.format_datetime: Callable[[datetime.datetime], str] = (
            datetime_format.value  # ty: ignore[invalid-assignment]  # pyrefly: ignore[bad-assignment]
        )

        self.format_string: Callable[[str], str] = format_string_backslash
        self.empty_sequence: str | None = None
        self.empty_dict: str | None = None
        self.set_open = "map[any]struct{}{"
        self.set_close = "}"
        self.empty_set: str | None = None
        self.format_sequence_entry: Callable[[str], str] = (
            passthrough_sequence_entry
        )
        self.format_set_entry: Callable[[str], str] = _format_go_set_entry
        self.comment_prefix = "//"
        self.comment_suffix = ""
        self.omap_open = "[][2]any{"
        self.omap_close = "}"
        self.format_omap_entry: Callable[[str, str], str] = (
            _format_go_omap_entry
        )
        self.multiline_close_indent = ""
        self.element_separator = ", "
        self.skip_null_dict_values = False
        self.coerce_heterogeneous_to_strings = False
        self.supports_collection_comments = True
        self.format_variable_declaration: Callable[[str, str], str] = (
            _format_variable_declaration
        )
        self.format_variable_assignment: Callable[[str, str], str] = (
            _format_variable_assignment
        )
