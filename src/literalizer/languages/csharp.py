"""C# language specification."""

import datetime
import enum
from typing import TYPE_CHECKING

from beartype import beartype

from literalizer._formatters import (
    MixedNumeric,
    TypedOpenerConfig,
    format_bytes_hex,
    format_date_iso,
    format_datetime_iso,
    format_string_backslash,
    passthrough_sequence_entry,
    passthrough_set_entry,
    typed_dict_open,
    typed_sequence_open,
    typed_set_open,
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

if TYPE_CHECKING:
    from collections.abc import Callable, Sequence


@beartype
def _format_date_csharp(value: datetime.date) -> str:
    """Format a date as a C# ``new DateOnly(...)`` call."""
    return f"new DateOnly({value.year}, {value.month}, {value.day})"


@beartype
def _format_datetime_csharp(value: datetime.datetime) -> str:
    """Format a datetime as a C# ``new DateTime(...)`` call."""
    return (
        f"new DateTime({value.year}, {value.month}, {value.day}, "
        f"{value.hour}, {value.minute}, {value.second})"
    )


_CSHARP_SCALAR_TYPES: dict[type, str] = {
    str: "string",
    bool: "bool",
    int: "int",
    float: "double",
    MixedNumeric: "double",
    bytes: "string",
    datetime.date: "DateOnly",
    datetime.datetime: "DateTime",
}

_csharp_opener_config = TypedOpenerConfig(
    scalar_types=_CSHARP_SCALAR_TYPES,
    list_template="{inner}[]",
    seq_opener_template="new {type_name}[] {{",
    dict_opener_template="new Dictionary<string, {type_name}> {{",
    set_opener_template="new HashSet<{type_name}> {{",
)


@beartype
def _format_csharp_dict_entry(key: str, value: str) -> str:
    """Format a C# dictionary indexer entry."""
    return f"[{key}] = {value}"


@beartype
def _format_variable_declaration(name: str, value: str, _data: Value) -> str:
    """Format a C# variable declaration."""
    return f"var {name} = {value};"


@beartype
def _format_variable_assignment(name: str, value: str, _data: Value) -> str:
    """Format a C# variable assignment."""
    return f"{name} = {value};"


@beartype
class CSharp(metaclass=LanguageCls):
    """C# language specification.

    Args:
        date_format: How to format :class:`datetime.date` values.

            * ``date_formats.CSHARP`` — ``new DateOnly(...)`` call,
              e.g. ``new DateOnly(2024, 1, 15)``.
            * ``date_formats.ISO`` — ISO 8601 quoted string,
              e.g. ``"2024-01-15"``.

        datetime_format: How to format :class:`datetime.datetime` values.

            * ``datetime_formats.CSHARP`` — ``new DateTime(...)`` call,
              e.g. ``new DateTime(2024, 1, 15, 12, 30, 0)``.
            * ``datetime_formats.ISO`` — ISO 8601 quoted string,
              e.g. ``"2024-01-15T12:30:00"``.
    """

    extension = ".cs"
    pygments_name = "csharp"

    class DateFormats(enum.Enum):
        """Date format options for C#."""

        CSHARP = DateFormatConfig(
            formatter=_format_date_csharp,
            preamble_lines=("using System;",),
        )
        ISO = DateFormatConfig(formatter=format_date_iso, type_produced=str)

        def __call__(self, date_value: datetime.date, /) -> str:
            """Format a date."""
            return self.value.formatter(date_value)

    class DatetimeFormats(enum.Enum):
        """Datetime format options for C#."""

        CSHARP = DatetimeFormatConfig(
            formatter=_format_datetime_csharp,
            preamble_lines=("using System;",),
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
        """Sequence type options for C#."""

        ARRAY = SequenceFormatConfig(
            sequence_open=typed_sequence_open(
                type_to_opener=_csharp_opener_config.build().seq,
                fallback="new object[] {",
            ),
            close="}",
            supports_heterogeneity=True,
            single_element_trailing_comma=False,
            empty_sequence="Array.Empty<object>()",
            preamble_lines=("using System.Collections.Generic;",),
        )

        @property
        def supports_heterogeneity(self) -> bool:
            """Whether this sequence format supports mixed-type
            elements.
            """
            return self.value.supports_heterogeneity

    class SetFormats(enum.Enum):
        """Set type options for C#."""

        HASH_SET = SetFormatConfig(
            set_open=typed_set_open(
                type_to_opener=_csharp_opener_config.build().set,
                fallback="new HashSet<object> {",
            ),
            close="}",
            empty_set="new HashSet<object>()",
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

        VAR = "var"

    class DictFormats(enum.Enum):
        """Dict/map format options."""

        DICTIONARY = "dictionary"

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

    def __init__(
        self,
        *,
        date_format: DateFormats = DateFormats.CSHARP,
        datetime_format: DatetimeFormats = DatetimeFormats.CSHARP,
        bytes_format: BytesFormats = BytesFormats.HEX,
        sequence_format: SequenceFormats = SequenceFormats.ARRAY,
        set_format: SetFormats = SetFormats.HASH_SET,
        variable_type_hints: VariableTypeHints = VariableTypeHints.NONE,
        comment_format: CommentFormats = CommentFormats.DOUBLE_SLASH,
        _variable_type_hints: VariableTypeHints = VariableTypeHints.NONE,
        declaration_style: DeclarationStyles = DeclarationStyles.VAR,
        dict_format: DictFormats = DictFormats.DICTIONARY,
        integer_format: IntegerFormats = IntegerFormats.DECIMAL,
        numeric_separator: NumericSeparators = NumericSeparators.NONE,
        string_format: StringFormats = StringFormats.DOUBLE,
        trailing_comma: TrailingCommas = TrailingCommas.NO,
    ) -> None:
        """Initialize CSharp language specification."""
        self.variable_type_hints = variable_type_hints
        self.sequence_format = sequence_format
        self.null_literal = "(object?)null"
        self.true_literal = "true"
        self.false_literal = "false"
        fmt = sequence_format.value
        self.sequence_format_config: SequenceFormatConfig = fmt
        self.set_format = set_format
        self.set_format_config: SetFormatConfig = set_format.value

        date_tp = date_format.value.type_produced
        dt_tp = datetime_format.value.type_produced
        openers = _csharp_opener_config.build(
            scalar_types={
                **_CSHARP_SCALAR_TYPES,
                datetime.date: _CSHARP_SCALAR_TYPES[date_tp],
                datetime.datetime: _CSHARP_SCALAR_TYPES[dt_tp],
            },
        )
        self.sequence_open: Callable[[list[Value]], str] = typed_sequence_open(
            type_to_opener=openers.seq,
            fallback="new object[] {",
        )
        self.dict_format_config: DictFormatConfig = DictFormatConfig(
            open_fn=typed_dict_open(
                type_to_opener=openers.dict,
                fallback="new Dictionary<string, object> {",
            ),
            close="}",
            format_entry=_format_csharp_dict_entry,
            empty_dict=None,
            preamble_lines=("using System.Collections.Generic;",),
        )
        self.multiline_trailing_comma = False
        self.format_bytes: Callable[[bytes], str] = bytes_format
        self.format_date: Callable[[datetime.date], str] = date_format
        self.format_datetime: Callable[[datetime.datetime], str] = (
            datetime_format
        )

        self.format_string: Callable[[str], str] = format_string_backslash
        self.format_integer: Callable[[int], str] = str
        self.format_sequence_entry: Callable[[str], str] = (
            passthrough_sequence_entry
        )
        self.format_set_entry: Callable[[str], str] = passthrough_set_entry
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
                open_str="new Dictionary<string, object> {",
                close="}",
                preamble_lines=(),
            )
        )
        self.format_ordered_map_entry: Callable[[str, str], str] = (
            _format_csharp_dict_entry
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
        self.scalar_preamble: dict[type, tuple[str, ...]] = {
            t: p
            for t, p in (
                (datetime.date, date_format.value.preamble_lines),
                (datetime.datetime, datetime_format.value.preamble_lines),
            )
            if p
        }
        self.type_hint_collection_preamble_lines: tuple[str, ...] = ()
