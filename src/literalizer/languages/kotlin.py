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
from literalizer._language import (
    CommentConfig,
    DictFormatConfig,
    HasFormatEnums,
    OrderedMapFormatConfig,
    SequenceFormatConfig,
    SetFormatConfig,
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
def _format_kotlin_ordered_map_entry(key: str, value: str) -> str:
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
class Kotlin(metaclass=HasFormatEnums):
    """Kotlin language specification.

    Args:
        date_format: How to format :class:`datetime.date` values.

            * ``date_formats.KOTLIN`` — ``LocalDate.of(...)`` call,
              e.g. ``LocalDate.of(2024, 1, 15)``.

        datetime_format: How to format :class:`datetime.datetime` values.

            * ``datetime_formats.KOTLIN`` — ``LocalDateTime.of(...)`` call,
              e.g. ``LocalDateTime.of(2024, 1, 15, 12, 30, 0)``.
    """

    class DateFormats(enum.Enum):
        """Date format options for Kotlin."""

        KOTLIN = enum.member(value=format_date_kotlin)

        def __call__(self, date_value: datetime.date, /) -> str:
            """Format a date."""
            return self.value(value=date_value)

    class DatetimeFormats(enum.Enum):
        """Datetime format options for Kotlin."""

        KOTLIN = enum.member(value=format_datetime_kotlin)

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
        """Sequence type options for Kotlin."""

        LIST = SequenceFormatConfig(
            open_str="listOf<Any?>(",
            close=")",
            supports_heterogeneity=True,
            single_element_trailing_comma=False,
            empty_sequence=None,
        )

        @property
        def supports_heterogeneity(self) -> bool:
            """Whether this sequence format supports mixed-type
            elements.
            """
            return self.value.supports_heterogeneity

    class SetFormats(enum.Enum):
        """Set type options for Kotlin."""

        SET = SetFormatConfig(
            open_str="setOf<Any?>(",
            close=")",
            empty_set=None,
        )

    class CommentFormats(enum.Enum):
        """Comment style options."""

        DOUBLE_SLASH = CommentConfig(
            prefix="//",
            suffix="",
        )

    date_formats = DateFormats
    datetime_formats = DatetimeFormats
    bytes_formats = BytesFormats
    sequence_formats = SequenceFormats
    set_formats = SetFormats
    comment_formats = CommentFormats

    class VariableTypeHints(enum.Enum):
        """Variable type hint options."""

        NONE = "none"

    def __init__(
        self,
        *,
        date_format: DateFormats = DateFormats.KOTLIN,
        datetime_format: DatetimeFormats = DatetimeFormats.KOTLIN,
        bytes_format: BytesFormats = BytesFormats.HEX,
        sequence_format: SequenceFormats = SequenceFormats.LIST,
        set_format: SetFormats = SetFormats.SET,
        comment_format: CommentFormats = CommentFormats.DOUBLE_SLASH,
    ) -> None:
        """Initialize Kotlin language specification."""
        self.sequence_format = sequence_format
        self.null_literal = "null"
        self.true_literal = "true"
        self.false_literal = "false"
        fmt = sequence_format.value
        self.sequence_format_config: SequenceFormatConfig = fmt
        self.set_format_config: SetFormatConfig = set_format.value
        self.sequence_open: Callable[[list[Value]], str] = typed_sequence_open(
            schema_to_opener=_kotlin_schema_to_opener,
            fallback=fmt.open_str,
        )
        self.dict_format_config: DictFormatConfig = DictFormatConfig(
            open_fn=typed_dict_open(
                schema_to_opener=_kotlin_dict_schema_to_opener,
                fallback="mapOf<String, Any?>(",
            ),
            close=")",
            format_entry=dict_entry_with_separator(separator=" to "),
            empty_dict=None,
        )
        self.multiline_trailing_comma = True
        self.format_bytes: Callable[[bytes], str] = bytes_format
        self.format_date: Callable[[datetime.date], str] = date_format
        self.format_datetime: Callable[[datetime.datetime], str] = (
            datetime_format
        )

        self.format_string: Callable[[str], str] = (
            format_string_backslash_dollar
        )
        self.format_sequence_entry: Callable[[str], str] = (
            passthrough_sequence_entry
        )
        self.format_set_entry: Callable[[str], str] = passthrough_set_entry
        self.comment_config: CommentConfig = comment_format.value
        self.ordered_map_format_config: OrderedMapFormatConfig = (
            OrderedMapFormatConfig(
                open_str="linkedMapOf<String, Any?>(",
                close=")",
            )
        )
        self.format_ordered_map_entry: Callable[[str, str], str] = (
            _format_kotlin_ordered_map_entry
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
