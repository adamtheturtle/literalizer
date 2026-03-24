"""F# language specification."""

import datetime
import enum
from typing import TYPE_CHECKING

from beartype import beartype

from literalizer._formatters import (
    date_ymd_formatter,
    datetime_ymdhms_formatter,
    fixed_dict_open,
    fixed_sequence_open,
    fixed_set_open,
    format_bytes_hex,
    format_date_iso,
    format_datetime_iso,
    format_integer_binary,
    format_integer_hex,
    format_integer_octal,
    format_string_backslash,
    passthrough_sequence_entry,
    tuple_dict_entry,
)
from literalizer._language import (
    CommentConfig,
    DateFormatConfig,
    DatetimeFormatConfig,
    DeclarationStyleConfig,
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
def _format_fsharp_entry(original: Value, formatted: str) -> str:
    """Wrap a formatted entry in the appropriate F# ``Val``
    constructor.
    """
    match original:
        case bool():
            return formatted
        case int():
            negative = formatted.startswith("-")
            return f"FInt({formatted}L)" if negative else f"FInt {formatted}L"
        case float():
            negative = formatted.startswith("-")
            return (
                f"FFloat({formatted})" if negative else f"FFloat {formatted}"
            )
        case str() | bytes() | datetime.date():
            if formatted.startswith("System."):
                return f"FStr (string ({formatted}))"
            return f"FStr {formatted}"
        case _:
            return formatted


@beartype
def _format_variable_declaration_let(
    name: str, value: str, data: Value
) -> str:
    """Format an F# ``let`` variable declaration."""
    val_type = "Val array" if value.lstrip().startswith("[|") else "Val"
    wrapped = _format_fsharp_entry(original=data, formatted=value)
    return f"let {name}: {val_type} = {wrapped}"


@beartype
def _format_variable_declaration_let_mutable(
    name: str, value: str, data: Value
) -> str:
    """Format an F# ``let mutable`` variable declaration."""
    val_type = "Val array" if value.lstrip().startswith("[|") else "Val"
    wrapped = _format_fsharp_entry(original=data, formatted=value)
    return f"let mutable {name}: {val_type} = {wrapped}"


@beartype
def _format_variable_assignment(name: str, value: str, data: Value) -> str:
    """Format an F# variable assignment."""
    val_type = "Val array" if value.lstrip().startswith("[|") else "Val"
    wrapped = _format_fsharp_entry(original=data, formatted=value)
    return f"let {name}: {val_type} = {wrapped}"


@beartype
class FSharp(metaclass=LanguageCls):
    """F# language specification.

    Args:
        date_format: How to format :class:`datetime.date` values.

            * ``date_formats.FSHARP`` — ``System.DateOnly(...)`` call,
              e.g. ``System.DateOnly(2024, 1, 15)``.

        datetime_format: How to format :class:`datetime.datetime` values.

            * ``datetime_formats.FSHARP`` — ``System.DateTime(...)`` call,
              e.g. ``System.DateTime(2024, 1, 15, 12, 30, 0)``.
    """

    extension = ".fs"
    pygments_name = "fsharp"

    class DateFormats(enum.Enum):
        """Date format options for FSharp."""

        FSHARP = DateFormatConfig(
            formatter=date_ymd_formatter(
                template="System.DateOnly({year}, {month}, {day})",
            ),
        )
        ISO = DateFormatConfig(formatter=format_date_iso, type_produced=str)

        def __call__(self, date_value: datetime.date, /) -> str:
            """Format a date."""
            return self.value.formatter(date_value)

    class DatetimeFormats(enum.Enum):
        """Datetime format options for FSharp."""

        FSHARP = DatetimeFormatConfig(
            formatter=datetime_ymdhms_formatter(
                template="System.DateTime({year}, {month}, {day}, "
                "{hour}, {minute}, {second})",
            ),
        )
        ISO = DatetimeFormatConfig(
            formatter=format_datetime_iso,
            type_produced=str,
        )

        def __call__(self, dt_value: datetime.datetime, /) -> str:
            """Format a datetime."""
            return self.value.formatter(dt_value)

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
            preamble_lines=(),
            format_entry=passthrough_sequence_entry,
            typed_opener_fallback=None,
        )
        ARRAY = SequenceFormatConfig(
            sequence_open=fixed_sequence_open(open_str="[|"),
            close="|]",
            supports_heterogeneity=True,
            single_element_trailing_comma=False,
            empty_sequence=None,
            preamble_lines=(),
            format_entry=passthrough_sequence_entry,
            typed_opener_fallback=None,
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
            set_open=fixed_set_open(open_str="FSet ["),
            close="]",
            empty_set=None,
            preamble_lines=(),
            set_opener_template="",
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

    class DeclarationStyles(enum.Enum):
        """Declaration style options."""

        LET = DeclarationStyleConfig(
            formatter=_format_variable_declaration_let,
        )
        LET_MUTABLE = DeclarationStyleConfig(
            formatter=_format_variable_declaration_let_mutable,
        )

    class DictFormats(enum.Enum):
        """Dict/map format options."""

        DEFAULT = "default"

    class IntegerFormats(enum.Enum):
        """Integer format options."""

        DECIMAL = enum.member(value=str)
        HEX = enum.member(value=format_integer_hex)
        OCTAL = enum.member(value=format_integer_octal)
        BINARY = enum.member(value=format_integer_binary)

        def __call__(self, value: int, /) -> str:
            """Format an integer."""
            formatter: Callable[[int], str] = self.value
            return formatter(value)

    class NumericSeparators(enum.Enum):
        """Numeric separator options."""

        NONE = "none"

    class StringFormats(enum.Enum):
        """String format options."""

        DOUBLE = "double"

    class TrailingCommas(enum.Enum):
        """Trailing comma options."""

        NO = "no"

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
    declaration_styles = DeclarationStyles
    dict_formats = DictFormats
    integer_formats = IntegerFormats
    numeric_separators = NumericSeparators
    string_formats = StringFormats
    trailing_commas = TrailingCommas

    class LineEndings(enum.Enum):
        """Line ending options."""

        SEMICOLON = "semicolon"

    line_endings = LineEndings

    def __init__(
        self,
        *,
        date_format: DateFormats = DateFormats.FSHARP,
        datetime_format: DatetimeFormats = DatetimeFormats.FSHARP,
        bytes_format: BytesFormats = BytesFormats.HEX,
        sequence_format: SequenceFormats = SequenceFormats.LIST,
        set_format: SetFormats = SetFormats.SET,
        variable_type_hints: VariableTypeHints = VariableTypeHints.NONE,
        comment_format: CommentFormats = CommentFormats.DOUBLE_SLASH,
        _variable_type_hints: VariableTypeHints = VariableTypeHints.NONE,
        declaration_style: DeclarationStyles = DeclarationStyles.LET,
        dict_format: DictFormats = DictFormats.DEFAULT,
        integer_format: IntegerFormats = IntegerFormats.DECIMAL,
        numeric_separator: NumericSeparators = NumericSeparators.NONE,
        string_format: StringFormats = StringFormats.DOUBLE,
        trailing_comma: TrailingCommas = TrailingCommas.NO,
        line_ending: LineEndings = LineEndings.SEMICOLON,
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
            format_entry=tuple_dict_entry(
                format_value=_format_fsharp_entry,
            ),
            empty_dict=None,
            preamble_lines=(),
        )
        self.multiline_trailing_comma = False
        self.format_bytes: Callable[[bytes], str] = bytes_format
        self.format_date: Callable[[datetime.date], str] = date_format
        self.format_datetime: Callable[[datetime.datetime], str] = (
            datetime_format
        )
        self.format_string: Callable[[str], str] = format_string_backslash
        self.format_integer: Callable[[int], str] = integer_format
        self.format_set_entry: Callable[[Value, str], str] = (
            _format_fsharp_entry
        )
        self.comment_format = comment_format
        self.declaration_style = declaration_style
        self.dict_format = dict_format
        self.integer_format = integer_format
        self.numeric_separator = numeric_separator
        self.string_format = string_format
        self.trailing_comma = trailing_comma
        self.line_ending = line_ending
        self.comment_config: CommentConfig = comment_format.value
        self.ordered_map_format_config: OrderedMapFormatConfig = (
            OrderedMapFormatConfig(
                open_str="FMap [",
                close="]",
                preamble_lines=(),
            )
        )
        self.format_ordered_map_entry: Callable[[str, Value, str], str] = (
            tuple_dict_entry(format_value=_format_fsharp_entry)
        )
        self.multiline_close_indent = ""
        self.skip_null_dict_values = False
        self.supports_collection_comments = True
        self.format_variable_declaration: Callable[[str, str, Value], str] = (
            declaration_style.value.formatter
        )
        self.format_variable_assignment: Callable[[str, str, Value], str] = (
            _format_variable_assignment
        )
        self.element_separator = "; "
        self.format_sequence_entry: Callable[[Value, str], str] = (
            _format_fsharp_entry
        )
        self.static_preamble: Sequence[str] = ()
        self.static_body_preamble: Sequence[str] = ()
        self.static_code_preamble: Sequence[str] = (
            "type Val =\n"
            "    | FNull\n"
            "    | FBool of bool\n"
            "    | FInt of int64\n"
            "    | FFloat of float\n"
            "    | FStr of string\n"
            "    | FList of Val list\n"
            "    | FMap of (string * Val) list\n"
            "    | FSet of Val list\n"
            "    | FDate of System.DateTime\n"
            "    | FDatetime of System.DateTime",
        )
        self.scalar_preamble: dict[type, tuple[str, ...]] = {}
        self.scalar_body_preamble: dict[type, tuple[str, ...]] = {}
        self.type_hint_collection_preamble_lines: tuple[str, ...] = ()
