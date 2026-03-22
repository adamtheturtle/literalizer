"""Dart language specification."""

import datetime
import enum
from typing import TYPE_CHECKING

from beartype import beartype

from literalizer._formatters import (
    ListType,
    MixedNumeric,
    dict_entry_with_separator,
    format_bytes_hex,
    format_string_backslash_dollar,
    passthrough_sequence_entry,
    passthrough_set_entry,
    typed_dict_open,
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

if TYPE_CHECKING:
    from collections.abc import Callable, Sequence


@beartype
def _format_date_dart(value: datetime.date) -> str:
    """Format a date as a Dart ``DateTime.parse(...)`` call."""
    return f'DateTime.parse("{value.isoformat()}")'


@beartype
def _format_datetime_dart(value: datetime.datetime) -> str:
    """Format a datetime as a Dart ``DateTime.parse(...)`` call."""
    return f'DateTime.parse("{value.isoformat()}")'


_DART_SCALAR_TYPES: dict[type, str] = {
    str: "String",
    bool: "bool",
    int: "int",
    float: "double",
    MixedNumeric: "double",
    bytes: "String",
    datetime.date: "DateTime",
    datetime.datetime: "DateTime",
}


@beartype
def _dart_element_to_type(element_type: type | ListType) -> str | None:
    """Map a Python element type to a Dart type name, recursively."""
    if isinstance(element_type, ListType):
        inner = _dart_element_to_type(element_type=element_type.inner)
        return f"List<{inner}>" if inner is not None else None
    return _DART_SCALAR_TYPES.get(element_type)


@beartype
def _dart_type_to_opener(element_type: type | ListType) -> str | None:
    """Map a Python element type to a Dart list opener."""
    type_name = _dart_element_to_type(element_type=element_type)
    if type_name is None:
        return None
    return f"<{type_name}>["


@beartype
def _dart_dict_type_to_opener(
    element_type: type | ListType,
) -> str | None:
    """Map a Python element type to a Dart map opener."""
    type_name = _dart_element_to_type(element_type=element_type)
    if type_name is None:
        return None
    return f"<String, {type_name}>{{"


@beartype
def _format_dart_ordered_map_entry(key: str, value: str) -> str:
    """Format a Dart map entry."""
    return f"{key}: {value}"


@beartype
def _format_variable_declaration(name: str, value: str, _data: Value) -> str:
    """Format a Dart variable declaration."""
    return f"final {name} = {value};"


@beartype
def _format_variable_assignment(name: str, value: str, _data: Value) -> str:
    """Format a Dart variable assignment."""
    return f"{name} = {value};"


@beartype
class Dart(metaclass=LanguageCls):
    """Dart language specification.

    Args:
        date_format: How to format :class:`datetime.date` values.

            * ``date_formats.DART`` — ``DateTime.parse(...)`` call,
              e.g. ``DateTime.parse("2024-01-15")``.

        datetime_format: How to format :class:`datetime.datetime` values.

            * ``datetime_formats.DART`` — ``DateTime.parse(...)`` call,
              e.g. ``DateTime.parse("2024-01-15T12:30:00")``.
    """

    extension = ".dart"
    pygments_name = "dart"

    class DateFormats(enum.Enum):
        """Date formatting options for Dart."""

        DART = enum.member(value=_format_date_dart)

        def __call__(self, date_value: datetime.date, /) -> str:
            """Format a date."""
            return self.value(value=date_value)

    class DatetimeFormats(enum.Enum):
        """Datetime formatting options for Dart."""

        DART = enum.member(value=_format_datetime_dart)

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
        """Sequence type options for Dart."""

        LIST = SequenceFormatConfig(
            sequence_open=typed_sequence_open(
                type_to_opener=_dart_type_to_opener,
                fallback="[",
            ),
            close="]",
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
        """Set type options for Dart."""

        SET = SetFormatConfig(
            open_str="{",
            close="}",
            empty_set="<dynamic>{}",
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
        date_format: DateFormats = DateFormats.DART,
        datetime_format: DatetimeFormats = DatetimeFormats.DART,
        bytes_format: BytesFormats = BytesFormats.HEX,
        sequence_format: SequenceFormats = SequenceFormats.LIST,
        set_format: SetFormats = SetFormats.SET,
        variable_type_hints: VariableTypeHints = VariableTypeHints.NONE,
        comment_format: CommentFormats = CommentFormats.DOUBLE_SLASH,
        _variable_type_hints: VariableTypeHints = VariableTypeHints.NONE,
    ) -> None:
        """Initialize Dart language specification."""
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
            open_fn=typed_dict_open(
                type_to_opener=_dart_dict_type_to_opener,
                fallback="{",
            ),
            close="}",
            format_entry=dict_entry_with_separator(separator=": "),
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
        self.comment_format = comment_format
        self.comment_config: CommentConfig = comment_format.value
        self.ordered_map_format_config: OrderedMapFormatConfig = (
            OrderedMapFormatConfig(
                open_str="{",
                close="}",
            )
        )
        self.format_ordered_map_entry: Callable[[str, str], str] = (
            _format_dart_ordered_map_entry
        )
        self.multiline_close_indent = ""
        self.element_separator = ", "
        self.skip_null_dict_values = False
        self.supports_collection_comments = True
        self.format_variable_declaration: Callable[[str, str, Value], str] = (
            _format_variable_declaration
        )
        self.format_variable_assignment: Callable[[str, str, Value], str] = (
            _format_variable_assignment
        )
        self.static_preamble: Sequence[str] = ()
        self.scalar_preamble: dict[type, tuple[str, ...]] = {}
        self.type_hint_collection_preamble_lines: tuple[str, ...] = ()
