"""Objective-C language specification."""

import datetime
import enum
from collections.abc import Callable, Sequence

from beartype import beartype

from literalizer._formatters import (
    fixed_dict_open,
    fixed_sequence_open,
    fixed_set_open,
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
)
from literalizer._types import Value

_OBJC_PREFIXES = (
    "@",
    "[NSNull null]",
    "[NSSet setWithArray:",
)


@beartype
def _to_objc_val(value: str) -> str:
    """Convert a pre-formatted value string to an Objective-C NSObject
    expression.

    Strings, booleans, null, and nested collections already start with
    ``@`` or ``[`` and are returned unchanged.  Bare numeric strings are
    wrapped in ``@(...)`` to produce an ``NSNumber`` literal.
    """
    if any(value.startswith(p) for p in _OBJC_PREFIXES):
        return value
    return f"@({value})"


@beartype
def _format_objc_dict_entry(key: str, value: str) -> str:
    """Format an Objective-C NSDictionary literal entry."""
    return f"{key}: {_to_objc_val(value=value)}"


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
def _format_variable_declaration(name: str, value: str, _data: Value) -> str:
    """Format an Objective-C ``id`` variable declaration.

    Example: ``"x"`` and ``@[@YES, @NO]`` →
    ``"id x = @[@YES, @NO];"``.
    """
    return f"id {name} = {value};"


@beartype
def _format_variable_assignment(name: str, value: str, _data: Value) -> str:
    """Format an Objective-C variable assignment.

    Example: ``"x"`` and ``@[@YES, @NO]`` → ``"x = @[@YES, @NO];"``
    """
    return f"{name} = {value};"


_string_format: Callable[[str], str] = _format_objc_string


@beartype
class ObjectiveC(metaclass=LanguageCls):
    """Objective-C language specification."""

    extension = ".m"
    pygments_name = "objective-c"

    class DateFormats(enum.Enum):
        """Date format options for ObjectiveC."""

        OBJC = DateFormatConfig(formatter=_format_objc_date)
        ISO = DateFormatConfig(formatter=_format_objc_date_iso)

        def __call__(self, date_value: datetime.date, /) -> str:
            """Format a date."""
            return self.value.formatter(date_value)

    class DatetimeFormats(enum.Enum):
        """Datetime format options for ObjectiveC."""

        OBJC = DatetimeFormatConfig(formatter=_format_objc_datetime)
        ISO = DatetimeFormatConfig(formatter=_format_objc_datetime_iso)

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
            preamble_lines=(),
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

        DECIMAL = "decimal"

    class NumericSeparators(enum.Enum):
        """Numeric separator options."""

        NONE = "none"

    class StringFormats(enum.Enum):
        """String format options."""

        DOUBLE = "double"

    class TrailingCommas(enum.Enum):
        """Trailing comma options."""

        YES = "yes"

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
            format_entry=_format_objc_dict_entry,
            empty_dict="@{}",
            preamble_lines=(),
        )
        self.multiline_trailing_comma = True
        self.format_bytes: Callable[[bytes], str] = bytes_format
        self.format_date: Callable[[datetime.date], str] = date_format
        self.format_datetime: Callable[[datetime.datetime], str] = (
            datetime_format
        )
        self.format_string: Callable[[str], str] = _string_format
        self.format_integer: Callable[[int], str] = str
        self.format_sequence_entry: Callable[[str], str] = _to_objc_val
        self.format_set_entry: Callable[[str], str] = _to_objc_val
        self.comment_format = comment_format
        self.declaration_style = declaration_style
        self.dict_format = dict_format
        self.integer_format = integer_format
        self.numeric_separator = numeric_separator
        self.string_format = string_format
        self.trailing_comma = trailing_comma
        self.comment_config: CommentConfig = comment_format.value
        self.ordered_map_format_config: OrderedMapFormatConfig = (
            OrderedMapFormatConfig(
                open_str="@{",
                close="}",
                preamble_lines=(),
            )
        )
        self.format_ordered_map_entry: Callable[[str, str], str] = (
            _format_objc_dict_entry
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
        self.static_preamble: Sequence[str] = (
            "#import <Foundation/Foundation.h>",
        )
        self.scalar_preamble: dict[type, tuple[str, ...]] = {}
        self.type_hint_collection_preamble_lines: tuple[str, ...] = ()
