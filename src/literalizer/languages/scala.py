"""Scala language specification."""

from __future__ import annotations

import enum
from typing import TYPE_CHECKING, Any

from beartype import beartype

from literalizer._formatters import (
    dict_entry_with_separator,
    format_bytes_hex,
    format_date_iso,
    format_datetime_iso,
    format_string_backslash,
    passthrough_sequence_entry,
    passthrough_set_entry,
    typed_dict_open,
    typed_sequence_open,
)
from literalizer._language import HasFormatEnums
from literalizer._types import Value  # noqa: TC001

if TYPE_CHECKING:
    import datetime
    from collections.abc import Callable

_SCALA_SCALAR_TYPES: dict[str, str] = {
    "string": "String",
    "boolean": "Boolean",
    "integer": "Int",
    "number": "Double",
}


@beartype
def _scala_schema_to_type(item_schema: dict[str, Any]) -> str | None:
    """Map a JSON Schema item type to a Scala type name, recursively."""
    schema_type = item_schema.get("type")
    if isinstance(schema_type, str):
        if schema_type in _SCALA_SCALAR_TYPES:
            return _SCALA_SCALAR_TYPES[schema_type]
        if schema_type == "array":
            nested = item_schema.get("items", {})
            inner = _scala_schema_to_type(item_schema=nested)
            return f"Array[{inner}]" if inner is not None else None
        return None
    if (
        isinstance(schema_type, list)
        and set(schema_type) == {"integer", "number"}  # pyright: ignore[reportUnknownArgumentType]
    ):
        return "Double"
    return None


@beartype
def _scala_schema_to_opener(item_schema: dict[str, Any]) -> str | None:
    """Map a JSON Schema item type to a Scala collection opener."""
    type_name = _scala_schema_to_type(item_schema=item_schema)
    if type_name is None:
        return None
    return f"Array[{type_name}]("


@beartype
def _scala_dict_schema_to_opener(value_schema: dict[str, Any]) -> str | None:
    """Map a JSON Schema value type to a Scala map opener."""
    type_name = _scala_schema_to_type(item_schema=value_schema)
    if type_name is None:
        return None
    return f"Map[String, {type_name}]("


@beartype
def _format_scala_omap_entry(key: str, value: str) -> str:
    """Format a Scala ``ListMap`` entry as a ``key -> value`` pair."""
    return f"{key} -> {value}"


@beartype
def _format_variable_declaration(name: str, value: str) -> str:
    """Format a Scala variable declaration."""
    return f"val {name} = {value}"


@beartype
def _format_variable_assignment(name: str, value: str) -> str:
    """Format a Scala variable assignment."""
    return f"{name} = {value}"


_string_format: Callable[[str], str] = format_string_backslash


@beartype
class Scala(metaclass=HasFormatEnums):
    """Scala language specification."""

    class DateFormats(enum.Enum):
        """Date format options for Scala."""

        ISO = enum.member(value=format_date_iso)

        def __call__(self, date_value: datetime.date, /) -> str:
            """Format a date."""
            return self.value(value=date_value)

    class DatetimeFormats(enum.Enum):
        """Datetime format options for Scala."""

        ISO = enum.member(value=format_datetime_iso)

        def __call__(self, dt_value: datetime.datetime, /) -> str:
            """Format a datetime."""
            return self.value(value=dt_value)

    class BytesFormats(enum.Enum):
        """Bytes formatting options."""

        HEX = enum.member(value=format_bytes_hex)

        def __call__(self, data: bytes, /) -> str:
            """Format bytes."""
            return self.value(value=data)

    class SequenceFormats(enum.Enum):
        """Sequence type options for Scala."""

        LIST = "list"

    class SetFormats(enum.Enum):
        """Set type options for Scala."""

        SET = "set"

    date_formats = DateFormats
    datetime_formats = DatetimeFormats
    bytes_formats = BytesFormats
    sequence_formats = SequenceFormats
    set_formats = SetFormats

    def __init__(
        self,
        *,
        date_format: DateFormats,
        datetime_format: DatetimeFormats,
        bytes_format: BytesFormats,
        sequence_format: SequenceFormats,
    ) -> None:
        """Initialize Scala language specification."""
        self.sequence_format = sequence_format
        self.null_literal = "null"
        self.true_literal = "true"
        self.false_literal = "false"
        self.sequence_open: Callable[[list[Value]], str] = typed_sequence_open(
            schema_to_opener=_scala_schema_to_opener,
            fallback="List(",
        )
        self.sequence_close = ")"
        self.dict_open: Callable[[dict[str, Value]], str] = typed_dict_open(
            schema_to_opener=_scala_dict_schema_to_opener,
            fallback="Map(",
        )
        self.dict_close = ")"
        self.format_dict_entry: Callable[[str, str], str] = (
            dict_entry_with_separator(separator=" -> ")
        )
        self.multiline_trailing_comma = True
        self.single_element_trailing_comma = False
        self.format_bytes: Callable[[bytes], str] = bytes_format
        self.format_date: Callable[[datetime.date], str] = date_format
        self.format_datetime: Callable[[datetime.datetime], str] = (
            datetime_format
        )
        self.format_string: Callable[[str], str] = _string_format
        self.empty_sequence: str | None = None
        self.empty_dict: str | None = None
        self.set_open = "Set("
        self.set_close = ")"
        self.empty_set: str | None = None
        self.format_sequence_entry: Callable[[str], str] = (
            passthrough_sequence_entry
        )
        self.format_set_entry: Callable[[str], str] = passthrough_set_entry
        self.comment_prefix = "//"
        self.comment_suffix = ""
        self.omap_open = "scala.collection.immutable.ListMap("
        self.omap_close = ")"
        self.format_omap_entry: Callable[[str, str], str] = (
            _format_scala_omap_entry
        )
        self.multiline_close_indent = ""
        self.element_separator = ", "
        self.skip_null_dict_values = False
        self.coerce_heterogeneous_scalars_to_strings = False
        self.coerce_heterogeneous_sibling_lists_to_strings = False
        self.coerce_heterogeneous_dict_values_to_strings = False
        self.coerce_heterogeneous_list_values_to_strings = False
        self.supports_collection_comments = True
        self.format_variable_declaration: Callable[[str, str], str] = (
            _format_variable_declaration
        )
        self.format_variable_assignment: Callable[[str, str], str] = (
            _format_variable_assignment
        )
