"""Objective-C language specification."""

import datetime
import enum
from typing import TYPE_CHECKING

from beartype import beartype

from literalizer._formatters import (
    dict_entry_with_separator,
    fixed_dict_open,
    fixed_sequence_open,
    fixed_set_open,
    format_integer_hex,
    format_integer_octal_c_style,
    passthrough_sequence_entry,
    variable_formatter,
)
from literalizer._language import (
    CommentConfig,
    DateFormatConfig,
    DatetimeFormatConfig,
    DictFormatConfig,
    LanguageCls,
    OrderedMapFormatConfig,
    SequenceFormatConfig,
    SetFormatConfig,
    TrailingCommaConfig,
    body_preamble_from_scalars,
)
from literalizer._types import Value

if TYPE_CHECKING:
    from collections.abc import Callable, Sequence


@beartype
def _format_objc_entry(_original: Value, formatted: str) -> str:
    """Wrap a formatted entry for use inside an Objective-C collection.

    Only bare numeric values (``int`` / ``float``, but not ``bool``)
    need ``@(...)`` wrapping; everything else is already a valid
    Objective-C object expression.
    """
    if isinstance(_original, (int, float)) and not isinstance(_original, bool):
        return f"@({formatted})"
    return formatted


@beartype
def _format_objc_string(value: str) -> str:
    r"""Format a string as an Objective-C ``NSString`` literal.

    Escapes backslashes, double quotes, newlines, and tabs, then wraps
    the result in ``@"..."``.

    Example: ``hello "world"`` → ``@"hello \"world\""``.
    """
    escaped = (
        value.replace("\\", "\\\\")
        .replace('"', '\\"')
        .replace("\n", "\\n")
        .replace("\t", "\\t")
    )
    return f'@"{escaped}"'


@beartype
def _format_objc_bytes(value: bytes) -> str:
    """Format bytes as an Objective-C ``NSString`` hex literal.

    Example: ``b"Hi"`` → ``@"4869"``.
    """
    return f'@"{value.hex()}"'


@beartype
def _format_objc_date(value: datetime.date) -> str:
    """Format a date as an Objective-C ``NSString`` ISO 8601 literal.

    Example: ``datetime.date(2024, 1, 15)`` → ``@"2024-01-15"``.
    """
    return f'@"{value.isoformat()}"'


@beartype
def _format_objc_date_iso(value: datetime.date) -> str:
    """Format a date as an Objective-C ``NSString`` ISO 8601 literal.

    This is the ISO format variant, producing the same ``@"..."``
    ``NSString`` output as the native format.

    Example: ``datetime.date(2024, 1, 15)`` → ``@"2024-01-15"``.
    """
    return f'@"{value.isoformat()}"'


@beartype
def _format_objc_datetime(value: datetime.datetime) -> str:
    """Format a datetime as an Objective-C ``NSString`` ISO 8601
    literal.

    Example: ``datetime.datetime(2024, 1, 15, 12, 30)`` →
    ``@"2024-01-15T12:30:00"``.
    """
    return f'@"{value.isoformat()}"'


@beartype
def _format_objc_datetime_iso(value: datetime.datetime) -> str:
    """Format a datetime as an Objective-C ``NSString`` ISO 8601 literal.

    This is the ISO format variant, producing the same ``@"..."``
    ``NSString`` output as the native format.

    Example: ``datetime.datetime(2024, 1, 15, 12, 30)`` →
    ``@"2024-01-15T12:30:00"``.
    """
    return f'@"{value.isoformat()}"'


@beartype
class ObjectiveC(metaclass=LanguageCls):
    """Objective-C language specification."""

    extension = ".m"
    pygments_name = "objective-c"

    class DateFormats(enum.Enum):
        """Date format options for ObjectiveC."""

        OBJC = DateFormatConfig(formatter=_format_objc_date)
        ISO = DateFormatConfig(
            formatter=_format_objc_date_iso,
            type_produced=str,
        )

        def __call__(self, date_value: datetime.date, /) -> str:
            """Format a date."""
            return self.value.formatter(date_value)

    class DatetimeFormats(enum.Enum):
        """Datetime format options for ObjectiveC."""

        OBJC = DatetimeFormatConfig(formatter=_format_objc_datetime)
        ISO = DatetimeFormatConfig(
            formatter=_format_objc_datetime_iso,
            type_produced=str,
        )

        def __call__(self, dt_value: datetime.datetime, /) -> str:
            """Format a datetime."""
            return self.value.formatter(dt_value)

    class BytesFormats(enum.Enum):
        """Bytes formatting options."""

        HEX = enum.member(value=_format_objc_bytes)

        def __call__(self, data: bytes, /) -> str:
            """Format bytes."""
            return self.value(value=data)

    class SequenceFormats(enum.Enum):
        """Sequence type options for Objective-C."""

        ARRAY = SequenceFormatConfig(
            sequence_open=fixed_sequence_open(open_str="@["),
            close="]",
            empty_sequence="@[]",
            supports_heterogeneity=True,
            single_element_trailing_comma=False,
            supports_trailing_comma=True,
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
        """Set type options for Objective-C."""

        SET = SetFormatConfig(
            set_open=fixed_set_open(open_str="[NSSet setWithArray:@["),
            close="]]",
            empty_set="[NSSet set]",
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
            prefix="/*",
            suffix=" */",
        )

    class DeclarationStyles(enum.Enum):
        """Declaration style options."""

        TYPED = "typed"

    class DictFormats(enum.Enum):
        """Dict/map format options."""

        DEFAULT = "default"

    class IntegerFormats(enum.Enum):
        """Integer format options."""

        DECIMAL = enum.member(value=str)
        HEX = enum.member(value=format_integer_hex)
        OCTAL = enum.member(value=format_integer_octal_c_style)

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

        YES = TrailingCommaConfig(multiline_trailing_comma=True)
        NO = TrailingCommaConfig(multiline_trailing_comma=False)

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
        date_format: DateFormats = DateFormats.OBJC,
        datetime_format: DatetimeFormats = DatetimeFormats.OBJC,
        bytes_format: BytesFormats = BytesFormats.HEX,
        sequence_format: SequenceFormats = SequenceFormats.ARRAY,
        set_format: SetFormats = SetFormats.SET,
        variable_type_hints: VariableTypeHints = VariableTypeHints.NONE,
        comment_format: CommentFormats = CommentFormats.DOUBLE_SLASH,
        _variable_type_hints: VariableTypeHints = VariableTypeHints.NONE,
        declaration_style: DeclarationStyles = DeclarationStyles.TYPED,
        dict_format: DictFormats = DictFormats.DEFAULT,
        integer_format: IntegerFormats = IntegerFormats.DECIMAL,
        numeric_separator: NumericSeparators = NumericSeparators.NONE,
        string_format: StringFormats = StringFormats.DOUBLE,
        trailing_comma: TrailingCommas = TrailingCommas.YES,
        line_ending: LineEndings = LineEndings.SEMICOLON,
        indent: str = "    ",
    ) -> None:
        """Initialize Objective-C language specification."""
        self.variable_type_hints = variable_type_hints
        self.sequence_format = sequence_format
        self.null_literal = "[NSNull null]"
        self.true_literal = "@YES"
        self.false_literal = "@NO"
        fmt = sequence_format.value
        self.sequence_format_config: SequenceFormatConfig = fmt
        self.set_format = set_format
        self.set_format_config: SetFormatConfig = set_format.value
        self.sequence_open: Callable[[list[Value]], str] = fmt.sequence_open
        self.dict_format_config: DictFormatConfig = DictFormatConfig(
            open_fn=fixed_dict_open(open_str="@{"),
            close="}",
            format_entry=dict_entry_with_separator(
                separator=": ",
                format_value=_format_objc_entry,
            ),
            empty_dict="@{}",
            preamble_lines=(),
        )
        self.trailing_comma_config: TrailingCommaConfig = trailing_comma.value
        self.format_bytes: Callable[[bytes], str] = bytes_format
        self.format_date: Callable[[datetime.date], str] = date_format
        self.format_datetime: Callable[[datetime.datetime], str] = (
            datetime_format
        )
        self.format_string: Callable[[str], str] = _format_objc_string
        self.format_integer: Callable[[int], str] = integer_format
        self.format_sequence_entry: Callable[[Value, str], str] = (
            _format_objc_entry
        )
        self.format_set_entry: Callable[[Value, str], str] = _format_objc_entry
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
                open_str="@{",
                close="}",
                preamble_lines=(),
            )
        )
        self.format_ordered_map_entry: Callable[[str, Value, str], str] = (
            dict_entry_with_separator(
                separator=": ",
                format_value=_format_objc_entry,
            )
        )
        self.indent = indent
        self.multiline_close_indent = ""
        self.element_separator = ", "
        self.skip_null_dict_values = False
        self.supports_collection_comments = True
        self.format_variable_declaration: Callable[[str, str, Value], str] = (
            variable_formatter(template="id {name} = {value};")
        )
        self.format_variable_assignment: Callable[[str, str, Value], str] = (
            variable_formatter(template="{name} = {value};")
        )
        self.static_preamble: Sequence[str] = (
            "#import <Foundation/Foundation.h>",
        )
        self.static_body_preamble: Sequence[str] = ()
        self.scalar_preamble: dict[type, tuple[str, ...]] = {}
        self.scalar_body_preamble: dict[type, tuple[str, ...]] = {}
        self.compute_body_preamble: Callable[
            [frozenset[type]], tuple[str, ...]
        ] = body_preamble_from_scalars(
            scalar_body_preamble=self.scalar_body_preamble,
        )

        self.type_hint_collection_preamble_lines: tuple[str, ...] = ()
