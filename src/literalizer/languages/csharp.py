"""C# language specification."""

from __future__ import annotations

import enum
from typing import TYPE_CHECKING, Any

from beartype import beartype

from literalizer._formatters import (
    fixed_dict_open,
    format_bytes_hex,
    format_date_csharp,
    format_date_iso,
    format_datetime_csharp,
    format_datetime_iso,
    format_string_backslash,
    passthrough_sequence_entry,
    passthrough_set_entry,
    typed_sequence_open,
)

if TYPE_CHECKING:
    import datetime
    from collections.abc import Callable

    from literalizer._types import Value

_CSHARP_SCALAR_TYPES: dict[str, str] = {
    "string": "string",
    "boolean": "bool",
    "integer": "int",
    "number": "double",
}


@beartype
def _csharp_schema_to_type(item_schema: dict[str, Any]) -> str | None:
    """Map a JSON Schema item type to a C# type name, recursively."""
    schema_type = item_schema.get("type")
    if isinstance(schema_type, str):
        if schema_type in _CSHARP_SCALAR_TYPES:
            return _CSHARP_SCALAR_TYPES[schema_type]
        if schema_type == "array":
            nested = item_schema.get("items", {})
            inner = _csharp_schema_to_type(item_schema=nested)
            return f"{inner}[]" if inner is not None else None
        return None
    if (
        isinstance(schema_type, list)
        and set(schema_type) == {"integer", "number"}  # pyright: ignore[reportUnknownArgumentType]
    ):
        return "double"
    return None


@beartype
def _csharp_schema_to_opener(item_schema: dict[str, Any]) -> str | None:
    """Map a JSON Schema item type to a C# array opener."""
    type_name = _csharp_schema_to_type(item_schema=item_schema)
    if type_name is None:
        return None
    return f"new {type_name}[] {{"


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


class CSharp:
    """C# language specification.

    Args:
        date_format: How to format :class:`datetime.date` values.

            * :attr:`DateFormat.ISO` (default) — ISO 8601 string,
              e.g. ``"2024-01-15"``.
            * :attr:`DateFormat.CSHARP` — ``new DateOnly(...)`` call,
              e.g. ``new DateOnly(2024, 1, 15)``.

        datetime_format: How to format :class:`datetime.datetime` values.

            * :attr:`DatetimeFormat.ISO` (default) — ISO 8601 string,
              e.g. ``"2024-01-15T12:30:00"``.
            * :attr:`DatetimeFormat.CSHARP` — ``new DateTime(...)`` call,
              e.g. ``new DateTime(2024, 1, 15, 12, 30, 0)``.
    """

    class DateFormat(enum.Enum):
        """Date format options for C#."""

        ISO = "iso"
        CSHARP = "csharp"

    class DatetimeFormat(enum.Enum):
        """Datetime format options for C#."""

        ISO = "iso"
        CSHARP = "csharp"

    @beartype
    def __init__(
        self,
        *,
        date_format: DateFormat = DateFormat.ISO,
        datetime_format: DatetimeFormat = DatetimeFormat.ISO,
    ) -> None:
        """Initialize CSharp language specification."""
        self.null_literal = "(object?)null"
        self.true_literal = "true"
        self.false_literal = "false"
        self.sequence_open: Callable[[list[Value]], str] = typed_sequence_open(
            schema_to_opener=_csharp_schema_to_opener,
            fallback="new object[] {",
        )
        self.sequence_close = "}"
        self.dict_open: Callable[[dict[str, Value]], str] = fixed_dict_open(
            open_str="new Dictionary<string, object> {"
        )
        self.dict_close = "}"
        self.format_dict_entry: Callable[[str, str], str] = (
            _format_csharp_dict_entry
        )
        self.multiline_trailing_comma = False
        self.single_element_trailing_comma = False
        self.format_bytes: Callable[[bytes], str] = format_bytes_hex
        if date_format is CSharp.DateFormat.CSHARP:
            self.format_date: Callable[[datetime.date], str] = (
                format_date_csharp
            )
        else:
            self.format_date = format_date_iso

        if datetime_format is CSharp.DatetimeFormat.CSHARP:
            self.format_datetime: Callable[[datetime.datetime], str] = (
                format_datetime_csharp
            )
        else:
            self.format_datetime = format_datetime_iso

        self.format_string: Callable[[str], str] = format_string_backslash
        self.empty_sequence: str | None = "Array.Empty<object>()"
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
