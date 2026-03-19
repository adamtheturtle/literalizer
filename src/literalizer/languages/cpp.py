"""C++ language specification."""

from __future__ import annotations

import enum
from typing import TYPE_CHECKING, Any

from beartype import beartype

from literalizer._formatters import (
    format_bytes_hex,
    format_date_cpp,
    format_date_iso,
    format_datetime_cpp,
    format_datetime_iso,
    format_string_backslash,
    passthrough_sequence_entry,
    passthrough_set_entry,
    typed_dict_open,
    typed_sequence_open,
)

if TYPE_CHECKING:
    import datetime
    from collections.abc import Callable

    from literalizer._types import Value

_CPP_SCALAR_TYPES: dict[str, str] = {
    "string": "std::string",
    "boolean": "bool",
    "integer": "int",
    "number": "double",
}


@beartype
def _cpp_schema_to_type(item_schema: dict[str, Any]) -> str | None:
    """Map a JSON Schema item type to a C++ type name, recursively."""
    schema_type = item_schema.get("type")
    if isinstance(schema_type, str):
        if schema_type in _CPP_SCALAR_TYPES:
            return _CPP_SCALAR_TYPES[schema_type]
        if schema_type == "array":
            nested = item_schema.get("items", {})
            inner = _cpp_schema_to_type(item_schema=nested)
            return f"std::vector<{inner}>" if inner is not None else None
        return None
    if (
        isinstance(schema_type, list)
        and set(schema_type) == {"integer", "number"}  # pyright: ignore[reportUnknownArgumentType]
    ):
        return "double"
    return None


@beartype
def _cpp_schema_to_opener(item_schema: dict[str, Any]) -> str | None:
    """Map a JSON Schema item type to a C++ initializer-list opener."""
    type_name = _cpp_schema_to_type(item_schema=item_schema)
    if type_name is None:
        return None
    return f"std::vector<{type_name}>{{"


@beartype
def _cpp_dict_schema_to_opener(value_schema: dict[str, Any]) -> str | None:
    """Map a JSON Schema value type to a C++ map opener."""
    type_name = _cpp_schema_to_type(item_schema=value_schema)
    if type_name is None:
        return None
    return f"std::map<std::string, {type_name}>{{"


@beartype
def _format_cpp_dict_entry(key: str, value: str) -> str:
    """Format a C++ dict entry as a brace-enclosed pair."""
    return f"{{{key}, {value}}}"


@beartype
def _format_variable_declaration(name: str, value: str) -> str:
    """Format a C++ variable declaration."""
    return f"auto {name} = {value};"


@beartype
def _format_variable_assignment(name: str, value: str) -> str:
    """Format a C++ variable assignment."""
    return f"{name} = {value};"


class Cpp:
    """C++ language specification.

    Args:
        date_format: How to format :class:`datetime.date` values.

            * ``DateFormat.ISO`` (default) — ISO 8601 string,
              e.g. ``"2024-01-15"``.
            * ``DateFormat.CPP`` — ``std::chrono::year_month_day`` literal,
              e.g. ``std::chrono::year_month_day{std::chrono::year{2024},
              std::chrono::month{1}, std::chrono::day{15}}``.

        datetime_format: How to format :class:`datetime.datetime` values.

            * ``DatetimeFormat.ISO`` (default) — ISO 8601 string,
              e.g. ``"2024-01-15T12:30:00"``.
            * ``DatetimeFormat.CPP`` — ``std::chrono::sys_days`` with
              time-of-day durations,
              e.g. ``std::chrono::sys_days{...} + std::chrono::hours{12}
              + std::chrono::minutes{30}``.
    """

    class DateFormat(enum.Enum):
        """Date format options for C++."""

        ISO = enum.member(value=format_date_iso)
        CPP = enum.member(value=format_date_cpp)

    class DatetimeFormat(enum.Enum):
        """Datetime format options for C++."""

        ISO = enum.member(value=format_datetime_iso)
        CPP = enum.member(value=format_datetime_cpp)

    @beartype
    def __init__(
        self,
        *,
        date_format: DateFormat = DateFormat.ISO,
        datetime_format: DatetimeFormat = DatetimeFormat.ISO,
    ) -> None:
        """Initialize Cpp language specification."""
        self.null_literal = "nullptr"
        self.true_literal = "true"
        self.false_literal = "false"
        self.sequence_open: Callable[[list[Value]], str] = typed_sequence_open(
            schema_to_opener=_cpp_schema_to_opener,
            fallback="{",
        )
        self.sequence_close = "}"
        self.dict_open: Callable[[dict[str, Value]], str] = typed_dict_open(
            schema_to_opener=_cpp_dict_schema_to_opener,
            fallback="{",
        )
        self.dict_close = "}"
        self.format_dict_entry: Callable[[str, str], str] = (
            _format_cpp_dict_entry
        )
        self.multiline_trailing_comma = True
        self.single_element_trailing_comma = False
        self.format_bytes: Callable[[bytes], str] = format_bytes_hex
        self.format_date: Callable[[datetime.date], str] = date_format.value  # ty: ignore[invalid-assignment]
        self.format_datetime: Callable[[datetime.datetime], str] = (
            datetime_format.value  # ty: ignore[invalid-assignment]
        )

        self.format_string: Callable[[str], str] = format_string_backslash
        self.empty_sequence: str | None = None
        self.empty_dict: str | None = None
        self.set_open = "{"
        self.set_close = "}"
        self.empty_set: str | None = None
        self.format_sequence_entry: Callable[[str], str] = (
            passthrough_sequence_entry
        )
        self.format_set_entry: Callable[[str], str] = passthrough_set_entry
        self.comment_prefix = "//"
        self.comment_suffix = ""
        self.omap_open = "{"
        self.omap_close = "}"
        self.format_omap_entry: Callable[[str, str], str] = (
            _format_cpp_dict_entry
        )
        self.multiline_close_indent = ""
        self.element_separator = ", "
        self.skip_null_dict_values = False
        self.supports_collection_comments = True
        self.format_variable_declaration: Callable[[str, str], str] = (
            _format_variable_declaration
        )
        self.format_variable_assignment: Callable[[str, str], str] = (
            _format_variable_assignment
        )
