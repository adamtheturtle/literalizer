"""Java language specification."""

import datetime
import enum
from typing import TYPE_CHECKING, Any

from beartype import beartype

from literalizer._formatters import (
    ListType,
    MixedNumeric,
    fixed_dict_open,
    format_bytes_hex,
    format_string_backslash,
    passthrough_sequence_entry,
    passthrough_set_entry,
    typed_sequence_open,
)
from literalizer._language import (
    CommentConfig,
    DictFormatConfig,
    LanguageCls,
    OrderedMapFormatConfig,
    SequenceFormatConfig,
    SetFormatConfig,
)
from literalizer._types import Value
from literalizer.exceptions import NullInCollectionError

if TYPE_CHECKING:
    from collections.abc import Callable, Sequence


@beartype
def _format_date_java(value: datetime.date) -> str:
    """Format a date as a Java ``LocalDate.of(...)`` call."""
    return f"LocalDate.of({value.year}, {value.month}, {value.day})"


@beartype
def _format_datetime_java_instant(value: datetime.datetime) -> str:
    """Format a datetime as a Java ``Instant.parse(...)`` call."""
    return f'Instant.parse("{value.isoformat()}")'


@beartype
def _format_datetime_java_zoned(value: datetime.datetime) -> str:
    """Format a datetime as a Java ``ZonedDateTime.of(...)`` call."""
    tz = value.tzname() or "UTC"
    nanos = value.microsecond * 1000
    return (
        f"ZonedDateTime.of({value.year}, {value.month}, {value.day}, "
        f"{value.hour}, {value.minute}, {value.second}, "
        f'{nanos}, ZoneId.of("{tz}"))'
    )


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


_JAVA_SCALAR_TYPES: dict[type, str] = {
    str: "String",
    bool: "boolean",
    int: "int",
    float: "double",
    MixedNumeric: "double",
    bytes: "String",
    datetime.date: "LocalDate",
}


@beartype
def _java_element_to_type(element_type: type | ListType) -> str | None:
    """Map a Python element type to a Java type name, recursively."""
    if isinstance(element_type, ListType):
        inner = _java_element_to_type(element_type=element_type.inner)
        return f"{inner}[]" if inner is not None else None
    return _JAVA_SCALAR_TYPES.get(element_type)


@beartype
def _java_type_to_opener(element_type: type | ListType) -> str | None:
    """Map a Python element type to a Java array opener."""
    type_name = _java_element_to_type(element_type=element_type)
    if type_name is None:
        return None
    return f"new {type_name}[]{{"


@beartype
def _format_variable_declaration(name: str, value: str, _data: Value) -> str:
    """Format a Java variable declaration."""
    return f"var {name} = {value};"


@beartype
def _format_variable_assignment(name: str, value: str, _data: Value) -> str:
    """Format a Java variable assignment."""
    return f"{name} = {value};"


@beartype
class Java(metaclass=LanguageCls):
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
    pygments_name = "java"

    class DateFormats(enum.Enum):
        """Date formatting options for Java."""

        JAVA = enum.member(value=_format_date_java)

        def __call__(self, date_value: datetime.date, /) -> str:
            """Format a date."""
            return self.value(value=date_value)

    class DatetimeFormats(enum.Enum):
        """Datetime formatting options for Java."""

        INSTANT = enum.member(value=_format_datetime_java_instant)
        ZONED = enum.member(value=_format_datetime_java_zoned)

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
            sequence_open=typed_sequence_open(
                type_to_opener=_java_type_to_opener,
                fallback="new Object[]{",
            ),
            close="}",
            supports_heterogeneity=True,
            single_element_trailing_comma=False,
            empty_sequence=None,
        )
        LIST = SequenceFormatConfig(
            sequence_open=_list_of_open,
            close=")",
            supports_heterogeneity=True,
            single_element_trailing_comma=False,
            empty_sequence="List.of()",
            preamble_lines=("import java.util.List;",),
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
            preamble_lines=("import java.util.Set;",),
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
        variable_type_hints: VariableTypeHints = VariableTypeHints.NONE,
        comment_format: CommentFormats = CommentFormats.DOUBLE_SLASH,
        _variable_type_hints: VariableTypeHints = VariableTypeHints.NONE,
    ) -> None:
        """Initialize Java language specification."""
        self.variable_type_hints = variable_type_hints
        self.sequence_format = sequence_format
        self.null_literal = "null"
        self.true_literal = "true"
        self.false_literal = "false"
        fmt = sequence_format.value
        self.sequence_format_config: SequenceFormatConfig = fmt
        self.set_format = set_format
        self.set_format_config: SetFormatConfig = set_format.value
        self.sequence_open: Callable[[list[Value]], str] = fmt.sequence_open
        self.dict_format_config: DictFormatConfig = DictFormatConfig(
            open_fn=fixed_dict_open(open_str="Map.ofEntries("),
            close=")",
            format_entry=_format_java_dict_entry,
            empty_dict=None,
            preamble_lines=("import java.util.Map;",),
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
        self.comment_format = comment_format
        self.comment_config: CommentConfig = comment_format.value
        self.ordered_map_format_config: OrderedMapFormatConfig = (
            OrderedMapFormatConfig(
                open_str="new java.util.ArrayList<>(java.util.Arrays.asList(",
                close="))",
                preamble_lines=("import java.util.Map;",),
            )
        )
        self.format_ordered_map_entry: Callable[[str, str], str] = (
            _format_java_dict_entry
        )
        self.multiline_close_indent = ""
        self.element_separator = ", "
        self.skip_null_dict_values = True
        self.supports_collection_comments = True
        self.format_variable_declaration: Callable[[str, str, Value], str] = (
            _format_variable_declaration
        )
        self.format_variable_assignment: Callable[[str, str, Value], str] = (
            _format_variable_assignment
        )
        self.static_preamble: Sequence[str] = ()
        date_preamble: tuple[str, ...] = ()
        if date_format is Java.DateFormats.JAVA:
            date_preamble = ("import java.time.LocalDate;",)
        datetime_preamble: tuple[str, ...] = ()
        if datetime_format is Java.DatetimeFormats.INSTANT:
            datetime_preamble = ("import java.time.Instant;",)
        elif datetime_format is Java.DatetimeFormats.ZONED:
            datetime_preamble = (
                "import java.time.ZoneId;",
                "import java.time.ZonedDateTime;",
            )
        scalar_preamble_dict: dict[type, tuple[str, ...]] = {}
        if date_preamble:
            scalar_preamble_dict[datetime.date] = date_preamble
        if datetime_preamble:
            scalar_preamble_dict[datetime.datetime] = datetime_preamble
        self.scalar_preamble: dict[type, tuple[str, ...]] = (
            scalar_preamble_dict
        )
        self.type_hint_collection_preamble_lines: tuple[str, ...] = ()
