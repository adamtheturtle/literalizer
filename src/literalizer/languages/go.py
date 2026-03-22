"""Go language specification."""

import datetime
import enum
from collections.abc import Callable, Sequence

from beartype import beartype

from literalizer._formatters import (
    ListType,
    MixedNumeric,
    dict_entry_with_separator,
    format_bytes_hex,
    format_date_go,
    format_datetime_go,
    format_string_backslash,
    passthrough_sequence_entry,
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

_GO_SCALAR_TYPES: dict[type, str] = {
    str: "string",
    bool: "bool",
    int: "int",
    float: "float64",
    MixedNumeric: "float64",
    bytes: "string",
    datetime.date: "time.Time",
    datetime.datetime: "time.Time",
}


@beartype
def _go_element_to_type(element_type: type | ListType) -> str | None:
    """Map a Python element type to a Go type name, recursively."""
    if isinstance(element_type, ListType):
        inner = _go_element_to_type(element_type=element_type.inner)
        return f"[]{inner}" if inner is not None else None
    return _GO_SCALAR_TYPES.get(element_type)


@beartype
def _go_type_to_opener(element_type: type | ListType) -> str | None:
    """Map a Python element type to a Go slice opener."""
    type_name = _go_element_to_type(element_type=element_type)
    if type_name is None:
        return None
    return f"[]{type_name}{{"


@beartype
def _go_dict_type_to_opener(
    element_type: type | ListType,
) -> str | None:
    """Map a Python element type to a Go map opener."""
    type_name = _go_element_to_type(element_type=element_type)
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
def _format_go_ordered_map_entry(key: str, value: str) -> str:
    """Format a Go ordered-map entry as a ``{key, value}`` pair."""
    return f"{{{key}, {value}}}"


@beartype
def _preamble(code: str) -> Sequence[str]:
    """Return preamble lines for the generated code."""
    lines: list[str] = ["package main"]
    if "time." in code:
        lines.append('import "time"')
    return lines


@beartype
def _format_variable_declaration(name: str, value: str, _data: Value) -> str:
    """Format a Go variable declaration."""
    return f"{name} := {value}"


@beartype
def _format_variable_assignment(name: str, value: str, _data: Value) -> str:
    """Format a Go variable assignment."""
    return f"{name} = {value}"


@beartype
class Go(metaclass=LanguageCls):
    """Go language specification.

    Args:
        date_format: How to format :class:`datetime.date` values.

            * ``date_formats.GO`` — ``time.Date`` call,
              e.g. ``time.Date(2024, time.January, 15, 0, 0, 0, 0,
              time.UTC)``.

        datetime_format: How to format :class:`datetime.datetime` values.

            * ``datetime_formats.GO`` — ``time.Date`` call,
              e.g. ``time.Date(2024, time.January, 15, 12, 30, 0, 0,
              time.UTC)``.
    """

    extension = ".go"
    pygments_name = "go"

    class DateFormats(enum.Enum):
        """Date format options for Go."""

        GO = enum.member(value=format_date_go)

        def __call__(self, date_value: datetime.date, /) -> str:
            """Format a date."""
            return self.value(value=date_value)

    class DatetimeFormats(enum.Enum):
        """Datetime format options for Go."""

        GO = enum.member(value=format_datetime_go)

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
        """Sequence type options for Go."""

        SLICE = SequenceFormatConfig(
            sequence_open=typed_sequence_open(
                type_to_opener=_go_type_to_opener,
                fallback="[]any{",
            ),
            close="}",
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
        """Set type options for Go."""

        SET = SetFormatConfig(
            open_str="map[any]struct{}{",
            close="}",
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
        date_format: DateFormats = DateFormats.GO,
        datetime_format: DatetimeFormats = DatetimeFormats.GO,
        bytes_format: BytesFormats = BytesFormats.HEX,
        sequence_format: SequenceFormats = SequenceFormats.SLICE,
        set_format: SetFormats = SetFormats.SET,
        variable_type_hints: VariableTypeHints = VariableTypeHints.NONE,
        comment_format: CommentFormats = CommentFormats.DOUBLE_SLASH,
        _variable_type_hints: VariableTypeHints = VariableTypeHints.NONE,
    ) -> None:
        """Initialize Go language specification."""
        self.variable_type_hints = variable_type_hints
        self.sequence_format = sequence_format
        self.null_literal = "nil"
        self.true_literal = "true"
        self.false_literal = "false"
        fmt = sequence_format.value
        self.sequence_format_config: SequenceFormatConfig = fmt
        self.set_format = set_format
        self.set_format_config: SetFormatConfig = set_format.value
        self.sequence_open: Callable[[list[Value]], str] = fmt.sequence_open
        self.dict_format_config: DictFormatConfig = DictFormatConfig(
            open_fn=typed_dict_open(
                type_to_opener=_go_dict_type_to_opener,
                fallback="map[string]any{",
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

        self.format_string: Callable[[str], str] = format_string_backslash
        self.format_sequence_entry: Callable[[str], str] = (
            passthrough_sequence_entry
        )
        self.format_set_entry: Callable[[str], str] = _format_go_set_entry
        self.comment_format = comment_format
        self.comment_config: CommentConfig = comment_format.value
        self.ordered_map_format_config: OrderedMapFormatConfig = (
            OrderedMapFormatConfig(
                open_str="[][2]any{",
                close="}",
            )
        )
        self.format_ordered_map_entry: Callable[[str, str], str] = (
            _format_go_ordered_map_entry
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
        self.preamble: Callable[[str], Sequence[str]] = _preamble
