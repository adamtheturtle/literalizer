"""Dart language specification."""

import datetime
import enum
from typing import TYPE_CHECKING

from beartype import beartype

from literalizer._formatters import (
    MixedNumeric,
    TypedOpenerConfig,
    dict_entry_with_separator,
    fixed_sequence_open,
    fixed_set_open,
    format_bytes_hex,
    format_date_iso,
    format_datetime_iso,
    format_string_backslash_dollar,
    passthrough_sequence_entry,
    passthrough_set_entry,
    typed_dict_open,
    typed_sequence_open,
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

_dart_opener_config = TypedOpenerConfig(
    scalar_types=_DART_SCALAR_TYPES,
    list_template="List<{inner}>",
    seq_opener_template="<{type_name}>[",
    dict_opener_template="<String, {type_name}>{{",
    set_opener_template="<{type_name}>{{",
)


@beartype
def _format_dart_ordered_map_entry(key: str, value: str) -> str:
    """Format a Dart map entry."""
    return f"{key}: {value}"


@beartype
def _format_variable_declaration_final(
    name: str, value: str, _data: Value
) -> str:
    """Format a Dart ``final`` variable declaration."""
    return f"final {name} = {value};"


@beartype
def _format_variable_declaration_var(
    name: str, value: str, _data: Value
) -> str:
    """Format a Dart ``var`` variable declaration."""
    return f"var {name} = {value};"


@beartype
def _format_variable_declaration_const(
    name: str, value: str, _data: Value
) -> str:
    """Format a Dart ``const`` variable declaration."""
    return f"const {name} = {value};"


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
            * ``date_formats.ISO`` — ISO 8601 quoted string,
              e.g. ``"2024-01-15"``.

        datetime_format: How to format :class:`datetime.datetime` values.

            * ``datetime_formats.DART`` — ``DateTime.parse(...)`` call,
              e.g. ``DateTime.parse("2024-01-15T12:30:00")``.
            * ``datetime_formats.ISO`` — ISO 8601 quoted string,
              e.g. ``"2024-01-15T12:30:00"``.
    """

    extension = ".dart"
    pygments_name = "dart"

    class DateFormats(enum.Enum):
        """Date formatting options for Dart."""

        DART = DateFormatConfig(formatter=_format_date_dart)
        ISO = DateFormatConfig(formatter=format_date_iso, type_produced=str)

        def __call__(self, date_value: datetime.date, /) -> str:
            """Format a date."""
            return self.value.formatter(date_value)

    class DatetimeFormats(enum.Enum):
        """Datetime formatting options for Dart."""

        DART = DatetimeFormatConfig(formatter=_format_datetime_dart)
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
        """Sequence type options for Dart."""

        LIST = SequenceFormatConfig(
            sequence_open=typed_sequence_open(
                type_to_opener=_dart_opener_config.build(
                    scalar_type_overrides={},
                ).seq,
                fallback="[",
            ),
            close="]",
            supports_heterogeneity=True,
            single_element_trailing_comma=False,
            empty_sequence=None,
            preamble_lines=(),
            format_entry=passthrough_sequence_entry,
        )
        TUPLE = SequenceFormatConfig(
            sequence_open=fixed_sequence_open(open_str="("),
            close=")",
            supports_heterogeneity=True,
            single_element_trailing_comma=True,
            empty_sequence="()",
            preamble_lines=(),
            format_entry=passthrough_sequence_entry,
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
            set_open=fixed_set_open(open_str="{"),
            close="}",
            empty_set="<dynamic>{}",
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

        FINAL = DeclarationStyleConfig(
            formatter=_format_variable_declaration_final,
        )
        VAR = DeclarationStyleConfig(
            formatter=_format_variable_declaration_var,
        )
        CONST = DeclarationStyleConfig(
            formatter=_format_variable_declaration_const,
        )

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

    class Semicolons(enum.Enum):
        """Semicolon options."""

        YES = "yes"

    semicolons = Semicolons

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
        declaration_style: DeclarationStyles = DeclarationStyles.FINAL,
        dict_format: DictFormats = DictFormats.DEFAULT,
        integer_format: IntegerFormats = IntegerFormats.DECIMAL,
        numeric_separator: NumericSeparators = NumericSeparators.NONE,
        string_format: StringFormats = StringFormats.DOUBLE,
        trailing_comma: TrailingCommas = TrailingCommas.YES,
        semicolon: Semicolons = Semicolons.YES,
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

        date_tp = date_format.value.type_produced
        dt_tp = datetime_format.value.type_produced
        openers = _dart_opener_config.build(
            scalar_type_overrides={
                datetime.date: _DART_SCALAR_TYPES[date_tp],
                datetime.datetime: _DART_SCALAR_TYPES[dt_tp],
            },
        )
        if sequence_format is self.sequence_formats.LIST:
            self.sequence_open: Callable[[list[Value]], str] = (
                typed_sequence_open(
                    type_to_opener=openers.seq,
                    fallback="[",
                )
            )
        else:
            self.sequence_open = fmt.sequence_open
        self.dict_format_config: DictFormatConfig = DictFormatConfig(
            open_fn=typed_dict_open(
                type_to_opener=openers.dict,
                fallback="{",
            ),
            close="}",
            format_entry=dict_entry_with_separator(separator=": "),
            empty_dict=None,
            preamble_lines=(),
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
        self.semicolon = semicolon
        self.comment_config: CommentConfig = comment_format.value
        self.ordered_map_format_config: OrderedMapFormatConfig = (
            OrderedMapFormatConfig(
                open_str="{",
                close="}",
                preamble_lines=(),
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
            declaration_style.value.formatter
        )
        self.format_variable_assignment: Callable[[str, str, Value], str] = (
            _format_variable_assignment
        )
        self.static_preamble: Sequence[str] = ()
        self.scalar_preamble: dict[type, tuple[str, ...]] = {}
        self.scalar_body_preamble: dict[type, tuple[str, ...]] = {}
        self.type_hint_collection_preamble_lines: tuple[str, ...] = ()
