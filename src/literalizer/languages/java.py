"""Java language specification."""

import datetime
import enum
from typing import TYPE_CHECKING, Any

from beartype import beartype

from literalizer._formatters import (
    fixed_dict_open,
    format_bytes_hex,
    format_date_java,
    format_datetime_java_instant,
    format_datetime_java_zoned,
    format_string_backslash,
    passthrough_sequence_entry,
    passthrough_set_entry,
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
from literalizer.exceptions import NullInCollectionError

if TYPE_CHECKING:
    from collections.abc import Callable

    from literalizer._types import Value


_LIST_OF_OPEN = "List.of("


@beartype
def _list_of_open(items: list[Any]) -> str:
    """Return ``List.of(`` after checking for null elements.

    Java's ``List.of()`` throws ``NullPointerException`` on null elements.
    """
    if any(item is None for item in items):
        msg = (
            "Java's List.of() does not accept null elements. "
            "Use sequence_format=ARRAY instead."
        )
        raise NullInCollectionError(msg)
    return _LIST_OF_OPEN


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
class Java(metaclass=HasFormatEnums):
    """Java language specification.

    Args:
        date_format: How to format :class:`datetime.date` values.

            * ``date_formats.JAVA`` — ``LocalDate.of(...)`` call,
              e.g. ``LocalDate.of(2024, 1, 15)``.

        datetime_format: How to format :class:`datetime.datetime` values.

            * ``datetime_formats.INSTANT`` — ``Instant.parse(...)`` call,
              e.g. ``Instant.parse("2024-01-15T12:30:00")``.
            * ``datetime_formats.ZONED`` — ``ZonedDateTime.of(...)`` call,
              e.g. ``ZonedDateTime.of(2024, 1, 15, 12, 30, 0, 0,
              ZoneId.of("UTC"))``.

        sequence_format: How to format sequences.

            * ``sequence_formats.ARRAY`` — Java array literal,
              e.g. ``new Object[]{1, 2, 3}``.
            * ``sequence_formats.LIST`` — ``List.of(...)`` call,
              e.g. ``List.of(1, 2, 3)``.
    """

    extension = ".java"

    class DateFormats(enum.Enum):
        """Date formatting options for Java."""

        JAVA = enum.member(value=format_date_java)

        def __call__(self, date_value: datetime.date, /) -> str:
            """Format a date."""
            return self.value(value=date_value)

    class DatetimeFormats(enum.Enum):
        """Datetime formatting options for Java."""

        INSTANT = enum.member(value=format_datetime_java_instant)
        ZONED = enum.member(value=format_datetime_java_zoned)

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
        """Sequence type options for Java."""

        ARRAY = SequenceFormatConfig(
            open_str="new Object[]{",
            close="}",
            supports_heterogeneity=True,
            single_element_trailing_comma=False,
            empty_sequence=None,
            schema_to_opener=_java_schema_to_opener,
        )
        LIST = SequenceFormatConfig(
            open_str="List.of(",
            close=")",
            supports_heterogeneity=True,
            single_element_trailing_comma=False,
            empty_sequence="List.of()",
            schema_to_opener=None,
        )

        @property
        def supports_heterogeneity(self) -> bool:
            """Whether this sequence format supports mixed-type
            elements.
            """
            return self.value.supports_heterogeneity

    class SetFormats(enum.Enum):
        """Set type options for Java."""

        SET = SetFormatConfig(
            open_str="Set.of(",
            close=")",
            empty_set=None,
        )

    class CommentFormats(enum.Enum):
        """Comment style options."""

        DOUBLE_SLASH = CommentConfig(
            prefix="//",
            suffix="",
        )
        BLOCK = CommentConfig(
            prefix="/*",
            suffix=" */",
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

    variable_type_hints_formats = VariableTypeHints

    def __init__(
        self,
        *,
        date_format: DateFormats = DateFormats.JAVA,
        datetime_format: DatetimeFormats = DatetimeFormats.INSTANT,
        bytes_format: BytesFormats = BytesFormats.HEX,
        sequence_format: SequenceFormats = SequenceFormats.ARRAY,
        set_format: SetFormats = SetFormats.SET,
        comment_format: CommentFormats = CommentFormats.DOUBLE_SLASH,
    ) -> None:
        """Initialize Java language specification."""
        self.sequence_format = sequence_format
        self.null_literal = "null"
        self.true_literal = "true"
        self.false_literal = "false"
        fmt = sequence_format.value
        self.sequence_format_config: SequenceFormatConfig = fmt
        self.set_format_config: SetFormatConfig = set_format.value
        if sequence_format is Java.SequenceFormats.LIST:  # pyright: ignore[reportUnknownMemberType,reportAttributeAccessIssue]
            self.sequence_open: Callable[[list[Value]], str] = _list_of_open
        else:
            schema_to_opener = fmt.schema_to_opener
            if schema_to_opener is None:  # pragma: no cover
                msg = "ARRAY format must have schema_to_opener"
                raise TypeError(msg)
            self.sequence_open = typed_sequence_open(
                schema_to_opener=schema_to_opener,
                fallback=fmt.open_str,
            )
        self.dict_format_config: DictFormatConfig = DictFormatConfig(
            open_fn=fixed_dict_open(open_str="Map.ofEntries("),
            close=")",
            format_entry=_format_java_dict_entry,
            empty_dict=None,
        )
        self.multiline_trailing_comma = False
        self.format_bytes: Callable[[bytes], str] = bytes_format
        self.format_date: Callable[[datetime.date], str] = date_format
        self.format_datetime: Callable[[datetime.datetime], str] = (
            datetime_format
        )
        self.format_string: Callable[[str], str] = format_string_backslash
        self.format_sequence_entry: Callable[[str], str] = (
            passthrough_sequence_entry
        )
        self.format_set_entry: Callable[[str], str] = passthrough_set_entry
        self.comment_config: CommentConfig = comment_format.value
        self.ordered_map_format_config: OrderedMapFormatConfig = (
            OrderedMapFormatConfig(
                open_str="new java.util.ArrayList<>(java.util.Arrays.asList(",
                close="))",
            )
        )
        self.format_ordered_map_entry: Callable[[str, str], str] = (
            _format_java_dict_entry
        )
        self.multiline_close_indent = ""
        self.element_separator = ", "
        self.skip_null_dict_values = True
        self.supports_collection_comments = True
        self.format_variable_declaration: Callable[[str, str], str] = (
            _format_variable_declaration
        )
        self.format_variable_assignment: Callable[[str, str], str] = (
            _format_variable_assignment
        )
