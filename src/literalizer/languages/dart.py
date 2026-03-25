"""Dart language specification."""

import datetime
import enum
from typing import TYPE_CHECKING

from beartype import beartype

from literalizer._formatters import (
    TypedOpenerConfig,
    date_iso_formatter,
    datetime_iso_formatter,
    dict_entry_with_separator,
    fixed_sequence_open,
    fixed_set_open,
    format_bytes_hex,
    format_date_iso,
    format_datetime_iso,
    format_integer_hex,
    format_string_backslash_dollar,
    format_string_backslash_dollar_single,
    make_element_to_type,
    make_type_to_opener,
    passthrough_sequence_entry,
    passthrough_set_entry,
    typed_dict_open,
    typed_sequence_open,
    variable_formatter,
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
    TrailingCommaConfig,
    body_preamble_from_scalars,
)

if TYPE_CHECKING:
    from collections.abc import Callable, Sequence

    from literalizer._types import Value


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

        DART = DateFormatConfig(
            formatter=date_iso_formatter(
                template='DateTime.parse("{iso}")',
            ),
        )
        ISO = DateFormatConfig(formatter=format_date_iso, type_produced=str)

        def __call__(self, date_value: datetime.date, /) -> str:
            """Format a date."""
            return self.value.formatter(date_value)

    class DatetimeFormats(enum.Enum):
        """Datetime formatting options for Dart."""

        DART = DatetimeFormatConfig(
            formatter=datetime_iso_formatter(
                template='DateTime.parse("{iso}")',
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
        """Sequence type options for Dart."""

        LIST = SequenceFormatConfig(
            sequence_open=typed_sequence_open(
                type_to_opener=make_type_to_opener(
                    element_to_type=make_element_to_type(
                        str_type="String",
                        bool_type="bool",
                        int_type="int",
                        float_type="double",
                        mixed_numeric_type="double",
                        bytes_type="String",
                        date_type="DateTime",
                        datetime_type="DateTime",
                        list_template="List<{inner}>",
                    ),
                    opener_template="<{type_name}>[",
                ),
                fallback="[",
            ),
            close="]",
            supports_heterogeneity=True,
            single_element_trailing_comma=False,
            supports_trailing_comma=True,
            empty_sequence=None,
            preamble_lines=(),
            format_entry=passthrough_sequence_entry,
            typed_opener_fallback="[",
        )
        TUPLE = SequenceFormatConfig(
            sequence_open=fixed_sequence_open(open_str="("),
            close=")",
            supports_heterogeneity=True,
            single_element_trailing_comma=True,
            supports_trailing_comma=True,
            empty_sequence="()",
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
        """Set type options for Dart."""

        SET = SetFormatConfig(
            set_open=fixed_set_open(open_str="{"),
            close="}",
            empty_set="<dynamic>{}",
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

        FINAL = DeclarationStyleConfig(
            formatter=variable_formatter(template="final {name} = {value};"),
            supports_redefinition=False,
        )
        VAR = DeclarationStyleConfig(
            formatter=variable_formatter(template="var {name} = {value};"),
            supports_redefinition=False,
        )
        CONST = DeclarationStyleConfig(
            formatter=variable_formatter(template="const {name} = {value};"),
            supports_redefinition=False,
        )

    class DictFormats(enum.Enum):
        """Dict/map format options."""

        DEFAULT = "default"

    class IntegerFormats(enum.Enum):
        """Integer format options."""

        DECIMAL = enum.member(value=str)
        HEX = enum.member(value=format_integer_hex)

        def __call__(self, value: int, /) -> str:
            """Format an integer."""
            formatter: Callable[[int], str] = self.value
            return formatter(value)

    class NumericSeparators(enum.Enum):
        """Numeric separator options."""

        NONE = "none"

    class StringFormats(enum.Enum):
        """String format options."""

        DOUBLE = enum.member(value=format_string_backslash_dollar)
        SINGLE = enum.member(value=format_string_backslash_dollar_single)

        def __call__(self, value: str, /) -> str:
            """Format a string."""
            return self.value(value=value)

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
        line_ending: LineEndings = LineEndings.SEMICOLON,
        indent: str = "    ",
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
        opener_config = TypedOpenerConfig(
            str_type="String",
            bool_type="bool",
            int_type="int",
            float_type="double",
            mixed_numeric_type="double",
            bytes_type="String",
            date_type="DateTime",
            datetime_type="DateTime",
            list_template="List<{inner}>",
            sequence_opener_template="<{type_name}>[",
            dict_opener_template="<String, {type_name}>{{",
            set_opener_template="<{type_name}>{{",
        )
        openers = opener_config.build(
            date_type=opener_config.type_name(py_type=date_tp),
            datetime_type=opener_config.type_name(py_type=dt_tp),
        )
        self.sequence_open: Callable[[list[Value]], str] = (
            typed_sequence_open(
                type_to_opener=openers.seq,
                fallback=fmt.typed_opener_fallback,
            )
            if fmt.typed_opener_fallback is not None
            else fmt.sequence_open
        )
        self.dict_format_config: DictFormatConfig = DictFormatConfig(
            open_fn=typed_dict_open(
                type_to_opener=openers.dict,
                fallback="{",
            ),
            close="}",
            format_entry=dict_entry_with_separator(
                separator=": ",
                format_value=passthrough_sequence_entry,
            ),
            empty_dict=None,
            preamble_lines=(),
        )
        self.trailing_comma_config: TrailingCommaConfig = trailing_comma.value
        self.format_bytes: Callable[[bytes], str] = bytes_format
        self.format_date: Callable[[datetime.date], str] = date_format
        self.format_datetime: Callable[[datetime.datetime], str] = (
            datetime_format
        )
        self.format_string: Callable[[str], str] = string_format
        self.format_integer: Callable[[int], str] = integer_format
        self.format_sequence_entry: Callable[[Value, str], str] = (
            passthrough_sequence_entry
        )
        self.format_set_entry: Callable[[Value, str], str] = (
            passthrough_set_entry
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
                open_str="{",
                close="}",
                preamble_lines=(),
            )
        )
        self.format_ordered_map_entry: Callable[[str, Value, str], str] = (
            dict_entry_with_separator(
                separator=": ",
                format_value=passthrough_sequence_entry,
            )
        )
        self.indent = indent
        self.indent_closing_delimiter = False
        self.element_separator = ", "
        self.skip_null_dict_values = False
        self.supports_collection_comments = True
        self.format_variable_declaration: Callable[[str, str, Value], str] = (
            declaration_style.value.formatter
        )
        self.format_variable_assignment: Callable[[str, str, Value], str] = (
            variable_formatter(template="{name} = {value};")
        )
        self.static_preamble: Sequence[str] = ()
        self.static_body_preamble: Sequence[str] = ()
        self.scalar_preamble: dict[type, tuple[str, ...]] = {}
        self.scalar_body_preamble: dict[type, tuple[str, ...]] = {}
        self.compute_body_preamble: Callable[
            [frozenset[type], Value], tuple[str, ...]
        ] = body_preamble_from_scalars(
            scalar_body_preamble=self.scalar_body_preamble,
        )

        self.type_hint_collection_preamble_lines: tuple[str, ...] = ()
