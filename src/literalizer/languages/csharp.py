"""C# language specification."""

import datetime
from collections.abc import Callable
from typing import Any, Literal

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
    typed_dict_open,
    typed_sequence_open,
)
from literalizer._types import Value  # noqa: TC001

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
def _csharp_dict_schema_to_opener(value_schema: dict[str, Any]) -> str | None:
    """Map a JSON Schema value type to a C# dictionary opener."""
    type_name = _csharp_schema_to_type(item_schema=value_schema)
    if type_name is None:
        return None
    return f"new Dictionary<string, {type_name}> {{"


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
        self.sequence_open: Callable[[list[Value]], str] = typed_sequence_open(
            schema_to_opener=_csharp_schema_to_opener,
            fallback="new object[] {",
        )
        self.sequence_close = "}"
        self.dict_open: Callable[[dict[str, Value]], str] = typed_dict_open(
            schema_to_opener=_csharp_dict_schema_to_opener,
            fallback="new Dictionary<string, object> {",
        )
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
        self.coerce_heterogeneous_to_strings = False
        self.format_variable_declaration: Callable[[str, str], str] = (
            _format_variable_declaration
        )
        self.format_variable_assignment: Callable[[str, str], str] = (
            _format_variable_assignment
        )
