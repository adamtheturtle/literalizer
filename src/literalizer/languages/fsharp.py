"""F# language specification."""

import datetime
import enum
from collections.abc import Callable, Sequence

from beartype import beartype

from literalizer._formatters import (
    fixed_dict_open,
    fixed_sequence_open,
    format_bytes_hex,
    format_date_iso,
    format_datetime_iso,
    format_string_backslash,
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


@beartype
def _format_date_fsharp(value: datetime.date) -> str:
    """Format a date as an F# ``System.DateTime(...)`` call."""
    return f"System.DateTime({value.year}, {value.month}, {value.day})"


@beartype
def _format_datetime_fsharp(value: datetime.datetime) -> str:
    """Format a datetime as an F# ``System.DateTime(...)`` call."""
    return (
        f"System.DateTime({value.year}, {value.month}, {value.day}, "
        f"{value.hour}, {value.minute}, {value.second})"
    )


@beartype
def _to_val(value: str) -> str:
    """Convert a value to an F# union type expression."""
    _val_prefixes = (
        "FNull",
        "FBool",
        "FList",
        "FMap",
        "FSet",
        "FStr",
        "FInt",
        "FFloat",
        "System.DateTime",
    )
    if any(value.startswith(p) for p in _val_prefixes):
        return value
    if value.startswith('"') and value.endswith('"'):
        return f"FStr {value}"
    negative = value.startswith("-")
    rest = value[1:] if negative else value
    int_result = None
    try:
        int(rest)
        int_result = f"FInt({value}L)" if negative else f"FInt {value}L"
    except ValueError:
        pass
    if int_result is not None:
        return int_result
    float(rest)
    return f"FFloat({value})" if negative else f"FFloat {value}"


@beartype
def _format_fsharp_dict_entry(key: str, value: str) -> str:
    """Format an F# dict entry as a ``(key, FVal value)`` tuple."""
    return f"({key}, {_to_val(value=value)})"


@beartype
def _format_fsharp_ordered_map_entry(key: str, value: str) -> str:
    """Format an F# ordered-map entry as a ``(key, FVal value)`` tuple."""
    return f"({key}, {_to_val(value=value)})"


@beartype
def _format_fsharp_set_entry(item: str) -> str:
    """Format an F# set entry with the appropriate ``Val`` constructor."""
    return _to_val(value=item)


@beartype
def _format_fsharp_sequence_entry(item: str) -> str:
    """Format an F# sequence entry with the appropriate ``Val``
    constructor.
    """
    return _to_val(value=item)


@beartype
def _format_variable_declaration(name: str, value: str, _data: Value) -> str:
    """Format an F# variable declaration."""
    return f"let {name}: Val = {_to_val(value=value)}"


@beartype
def _format_variable_assignment(name: str, value: str, _data: Value) -> str:
    """Format an F# variable assignment."""
    return f"let {name}: Val = {_to_val(value=value)}"


_string_format: Callable[[str], str] = format_string_backslash


@beartype
def _preamble(_code: str) -> Sequence[str]:
    """Return preamble lines for the generated code.

    The ``Val`` discriminated union used by the generated output is
    user-defined and must appear after the ``module`` declaration, so
    it is not part of the preamble.
    """
    return ()


@beartype
class FSharp(metaclass=LanguageCls):
    """F# language specification.

    Args:
        date_format: How to format :class:`datetime.date` values.

            * ``date_formats.FSHARP`` — ``System.DateTime(...)`` call,
              e.g. ``System.DateTime(2024, 1, 15)``.
            * ``date_formats.ISO`` — ISO 8601 quoted string,
              e.g. ``"2024-01-15"``.

        datetime_format: How to format :class:`datetime.datetime` values.

            * ``datetime_formats.FSHARP`` — ``System.DateTime(...)`` call,
              e.g. ``System.DateTime(2024, 1, 15, 12, 30, 0)``.
            * ``datetime_formats.ISO`` — ISO 8601 quoted string,
              e.g. ``"2024-01-15T12:30:00"``.
    """

    extension = ".fs"
    pygments_name = "fsharp"

    class DateFormats(enum.Enum):
        """Date format options for FSharp."""

        FSHARP = enum.member(value=_format_date_fsharp)
        ISO = enum.member(value=format_date_iso)

        def __call__(self, date_value: datetime.date, /) -> str:
            """Format a date."""
            return self.value(value=date_value)

    class DatetimeFormats(enum.Enum):
        """Datetime format options for FSharp."""

        FSHARP = enum.member(value=_format_datetime_fsharp)
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
        """Sequence type options for F#."""

        LIST = SequenceFormatConfig(
            sequence_open=fixed_sequence_open(open_str="FList ["),
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
        """Set type options for F#."""

        SET = SetFormatConfig(
            open_str="FSet [",
            close="]",
            empty_set=None,
        )

    class CommentFormats(enum.Enum):
        """Comment style options."""

        DOUBLE_SLASH = CommentConfig(
            prefix="//",
            suffix="",
        )
        BLOCK = CommentConfig(
            prefix="(*",
            suffix=" *)",
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
        date_format: DateFormats = DateFormats.ISO,
        datetime_format: DatetimeFormats = DatetimeFormats.ISO,
        bytes_format: BytesFormats = BytesFormats.HEX,
        sequence_format: SequenceFormats = SequenceFormats.LIST,
        set_format: SetFormats = SetFormats.SET,
        variable_type_hints: VariableTypeHints = VariableTypeHints.NONE,
        comment_format: CommentFormats = CommentFormats.DOUBLE_SLASH,
        _variable_type_hints: VariableTypeHints = VariableTypeHints.NONE,
    ) -> None:
        """Initialize FSharp language specification."""
        self.variable_type_hints = variable_type_hints
        self.sequence_format = sequence_format
        self.null_literal = "FNull"
        self.true_literal = "FBool true"
        self.false_literal = "FBool false"
        fmt = sequence_format.value
        self.sequence_format_config: SequenceFormatConfig = fmt
        self.set_format = set_format
        self.set_format_config: SetFormatConfig = set_format.value
        self.sequence_open: Callable[[list[Value]], str] = fmt.sequence_open
        self.dict_format_config: DictFormatConfig = DictFormatConfig(
            open_fn=fixed_dict_open(open_str="FMap ["),
            close="]",
            format_entry=_format_fsharp_dict_entry,
            empty_dict=None,
        )
        self.multiline_trailing_comma = False
        self.format_bytes: Callable[[bytes], str] = bytes_format
        self.format_date: Callable[[datetime.date], str] = date_format
        self.format_datetime: Callable[[datetime.datetime], str] = (
            datetime_format
        )
        self.format_string: Callable[[str], str] = _string_format
        self.format_set_entry: Callable[[str], str] = _format_fsharp_set_entry
        self.comment_format = comment_format
        self.comment_config: CommentConfig = comment_format.value
        self.ordered_map_format_config: OrderedMapFormatConfig = (
            OrderedMapFormatConfig(
                open_str="FMap [",
                close="]",
            )
        )
        self.format_ordered_map_entry: Callable[[str, str], str] = (
            _format_fsharp_ordered_map_entry
        )
        self.multiline_close_indent = ""
        self.skip_null_dict_values = False
        self.supports_collection_comments = True
        self.format_variable_declaration: Callable[[str, str, Value], str] = (
            _format_variable_declaration
        )
        self.format_variable_assignment: Callable[[str, str, Value], str] = (
            _format_variable_assignment
        )
        self.element_separator = "; "
        self.format_sequence_entry: Callable[[str], str] = (
            _format_fsharp_sequence_entry
        )
        self.preamble: Callable[[str], Sequence[str]] = _preamble
