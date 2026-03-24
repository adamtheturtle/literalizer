"""Kotlin language specification."""

import dataclasses
import datetime
import enum
from collections.abc import Callable
from types import MappingProxyType
from typing import TYPE_CHECKING

from beartype import beartype

from literalizer._formatters import (
    ListType,
    TypedOpenerConfig,
    date_ymd_formatter,
    datetime_ymdhms_formatter,
    dict_entry_with_separator,
    fixed_sequence_open,
    format_bytes_hex,
    format_date_iso,
    format_datetime_iso,
    format_integer_binary,
    format_integer_hex,
    format_integer_underscore,
    format_string_backslash_dollar,
    passthrough_sequence_entry,
    passthrough_set_entry,
    typed_dict_open,
    typed_sequence_open,
    typed_set_open,
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
    date_scalar_preamble,
)
from literalizer._types import Value

if TYPE_CHECKING:
    from collections.abc import Sequence


@beartype
def _kotlin_tuple_open(items: list[Value]) -> str:
    """Return the Kotlin tuple opener based on element count."""
    openers: dict[int, str] = {
        2: "Pair(",
        3: "Triple(",
    }
    return openers.get(len(items), "listOf<Any?>(")


@beartype
def _kotlin_type_to_opener(
    element_type: type | ListType,
) -> str | None:
    """Map a Python element type to a Kotlin collection opener."""
    if isinstance(element_type, ListType):
        inner = _kotlin_type_to_opener(element_type=element_type.inner)
        return "arrayOf(" if inner is not None else None
    scalar_openers: dict[type, str] = {
        str: "arrayOf(",
        bool: "booleanArrayOf(",
        int: "intArrayOf(",
        float: "doubleArrayOf(",
        bytes: "arrayOf(",
        datetime.date: "arrayOf(",
        datetime.datetime: "arrayOf(",
    }
    return scalar_openers.get(element_type)


_kotlin_opener_config = TypedOpenerConfig(
    str_type="String",
    bool_type="Boolean",
    int_type="Int",
    float_type="Double",
    bytes_type="String",
    mixed_numeric_type=None,
    date_type="LocalDate",
    datetime_type="LocalDateTime",
    list_template="Array<{inner}>",
    sequence_opener_template="arrayOf(",
    dict_opener_template="mapOf<String, {type_name}>(",
    set_opener_template="setOf<{type_name}>(",
)


@beartype
class Kotlin(metaclass=LanguageCls):
    """Kotlin language specification.

    Args:
        date_format: How to format :class:`datetime.date` values.

            * ``date_formats.KOTLIN`` — ``LocalDate.of(...)`` call,
              e.g. ``LocalDate.of(2024, 1, 15)``.
            * ``date_formats.ISO`` — ISO 8601 quoted string,
              e.g. ``"2024-01-15"``.

        datetime_format: How to format :class:`datetime.datetime` values.

            * ``datetime_formats.KOTLIN`` — ``LocalDateTime.of(...)`` call,
              e.g. ``LocalDateTime.of(2024, 1, 15, 12, 30, 0)``.
            * ``datetime_formats.ISO`` — ISO 8601 quoted string,
              e.g. ``"2024-01-15T12:30:00"``.

        sequence_format: Which Kotlin sequence type to use.

            * ``sequence_formats.LIST`` — typed array calls
              (e.g. ``intArrayOf(1, 2, 3)``).  Heterogeneous
              sequences fall back to ``listOf<Any?>(…)``.
            * ``sequence_formats.TUPLE`` — ``Pair(…)`` for two-element
              sequences, ``Triple(…)`` for three-element sequences,
              e.g. ``Pair("a", 1)``.  Other sizes fall back to
              ``listOf<Any?>(…)``.
    """

    extension = ".kts"
    pygments_name = "kotlin"

    class DateFormats(enum.Enum):
        """Date format options for Kotlin."""

        KOTLIN = DateFormatConfig(
            formatter=date_ymd_formatter(
                template="LocalDate.of({year}, {month}, {day})",
            ),
            preamble_lines=("import java.time.LocalDate",),
        )
        ISO = DateFormatConfig(formatter=format_date_iso, type_produced=str)

        def __call__(self, date_value: datetime.date, /) -> str:
            """Format a date."""
            return self.value.formatter(date_value)

    class DatetimeFormats(enum.Enum):
        """Datetime format options for Kotlin."""

        KOTLIN = DatetimeFormatConfig(
            formatter=datetime_ymdhms_formatter(
                template="LocalDateTime.of({year}, {month}, {day}, "
                "{hour}, {minute}, {second})",
            ),
            preamble_lines=("import java.time.LocalDateTime",),
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
        """Sequence type options for Kotlin."""

        LIST = SequenceFormatConfig(
            sequence_open=typed_sequence_open(
                type_to_opener=_kotlin_type_to_opener,
                fallback="listOf<Any?>(",
            ),
            close=")",
            supports_heterogeneity=True,
            single_element_trailing_comma=False,
            empty_sequence=None,
            preamble_lines=(),
            format_entry=passthrough_sequence_entry,
            typed_opener_fallback=None,
        )
        ARRAY = SequenceFormatConfig(
            sequence_open=fixed_sequence_open(open_str="arrayOf<Any?>("),
            close=")",
            supports_heterogeneity=True,
            single_element_trailing_comma=False,
            empty_sequence=None,
            preamble_lines=(),
            format_entry=passthrough_sequence_entry,
            typed_opener_fallback=None,
        )
        TUPLE = SequenceFormatConfig(
            sequence_open=_kotlin_tuple_open,
            format_entry=passthrough_sequence_entry,
            typed_opener_fallback=None,
            close=")",
            supports_heterogeneity=True,
            single_element_trailing_comma=False,
            empty_sequence=None,
            preamble_lines=(),
        )

        @property
        def supports_heterogeneity(self) -> bool:
            """Whether this sequence format supports mixed-type
            elements.
            """
            return self.value.supports_heterogeneity

    class SetFormats(enum.Enum):
        """Set type options for Kotlin."""

        SET = SetFormatConfig(
            set_open=typed_set_open(
                type_to_opener=_kotlin_opener_config.build().set,
                fallback="setOf<Any?>(",
            ),
            close=")",
            empty_set=None,
            preamble_lines=(),
            set_opener_template="",
        )
        SORTED_SET = SetFormatConfig(
            set_open=typed_set_open(
                type_to_opener=_kotlin_opener_config.build(
                    set_opener_template="sortedSetOf<{type_name}>(",
                ).set,
                fallback="sortedSetOf<Any?>(",
            ),
            close=")",
            empty_set=None,
            preamble_lines=(),
            set_opener_template="sortedSetOf<{type_name}>(",
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

        VAL = DeclarationStyleConfig(
            formatter=variable_formatter(template="val {name} = {value}"),
            supports_redefinition=False,
        )
        VAR = DeclarationStyleConfig(
            formatter=variable_formatter(template="var {name} = {value}"),
            supports_redefinition=True,
        )

    class DictFormats(enum.Enum):
        """Dict/map format options."""

        MAP = "map"

    class IntegerFormats(enum.Enum):
        """Integer format options."""

        DECIMAL = MappingProxyType(
            mapping={
                "NONE": str,
                "UNDERSCORE": format_integer_underscore,
            }
        )
        HEX = MappingProxyType(
            mapping={
                "NONE": format_integer_hex,
                "UNDERSCORE": format_integer_hex,
            }
        )
        BINARY = MappingProxyType(
            mapping={
                "NONE": format_integer_binary,
                "UNDERSCORE": format_integer_binary,
            }
        )

        def get_formatter(
            self,
            numeric_separator: enum.Enum,
        ) -> Callable[[int], str]:
            """Return the integer formatter for the given separator."""
            formatter: Callable[[int], str] = self.value[
                numeric_separator.name
            ]
            return formatter

    class NumericSeparators(enum.Enum):
        """Numeric separator options."""

        NONE = "none"
        UNDERSCORE = "underscore"

    class StringFormats(enum.Enum):
        """String format options."""

        DOUBLE = "double"

    class TrailingCommas(enum.Enum):
        """Trailing comma options."""

        YES = "yes"
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
        date_format: DateFormats = DateFormats.KOTLIN,
        datetime_format: DatetimeFormats = DatetimeFormats.KOTLIN,
        bytes_format: BytesFormats = BytesFormats.HEX,
        sequence_format: SequenceFormats = SequenceFormats.LIST,
        set_format: SetFormats = SetFormats.SET,
        variable_type_hints: VariableTypeHints = VariableTypeHints.NONE,
        comment_format: CommentFormats = CommentFormats.DOUBLE_SLASH,
        _variable_type_hints: VariableTypeHints = VariableTypeHints.NONE,
        declaration_style: DeclarationStyles = DeclarationStyles.VAL,
        dict_format: DictFormats = DictFormats.MAP,
        integer_format: IntegerFormats = IntegerFormats.DECIMAL,
        numeric_separator: NumericSeparators = NumericSeparators.NONE,
        string_format: StringFormats = StringFormats.DOUBLE,
        trailing_comma: TrailingCommas = TrailingCommas.YES,
        line_ending: LineEndings = LineEndings.SEMICOLON,
    ) -> None:
        """Initialize Kotlin language specification."""
        self.variable_type_hints = variable_type_hints
        self.sequence_format = sequence_format
        self.null_literal = "null"
        self.true_literal = "true"
        self.false_literal = "false"
        fmt = sequence_format.value
        self.sequence_format_config: SequenceFormatConfig = fmt
        self.set_format = set_format
        self.sequence_open: Callable[[list[Value]], str] = fmt.sequence_open

        date_tp = date_format.value.type_produced
        dt_tp = datetime_format.value.type_produced
        openers = _kotlin_opener_config.build(
            date_type=_kotlin_opener_config.type_name(py_type=date_tp),
            datetime_type=_kotlin_opener_config.type_name(py_type=dt_tp),
            set_opener_template=set_format.value.set_opener_template or None,
        )
        self.set_format_config: SetFormatConfig = dataclasses.replace(
            set_format.value,
            set_open=typed_set_open(
                type_to_opener=openers.set,
                fallback=set_format.value.set_open([]),
            ),
        )
        self.dict_format_config: DictFormatConfig = DictFormatConfig(
            open_fn=typed_dict_open(
                type_to_opener=openers.dict,
                fallback="mapOf<String, Any?>(",
            ),
            close=")",
            format_entry=dict_entry_with_separator(
                separator=" to ",
                format_value=passthrough_sequence_entry,
            ),
            empty_dict=None,
            preamble_lines=(),
        )
        self.multiline_trailing_comma: bool = trailing_comma.name == "YES"
        self.format_bytes: Callable[[bytes], str] = bytes_format
        self.format_date: Callable[[datetime.date], str] = date_format
        self.format_datetime: Callable[[datetime.datetime], str] = (
            datetime_format
        )

        self.format_string: Callable[[str], str] = (
            format_string_backslash_dollar
        )
        self.format_integer: Callable[[int], str] = (
            integer_format.get_formatter(
                numeric_separator=numeric_separator,
            )
        )
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
                open_str="linkedMapOf<String, Any?>(",
                close=")",
                preamble_lines=(),
            )
        )
        self.format_ordered_map_entry: Callable[[str, Value, str], str] = (
            dict_entry_with_separator(
                separator=" to ",
                format_value=passthrough_sequence_entry,
            )
        )
        self.multiline_close_indent = ""
        self.element_separator = ", "
        self.skip_null_dict_values = False
        self.supports_collection_comments = True
        self.format_variable_declaration: Callable[[str, str, Value], str] = (
            declaration_style.value.formatter
        )
        self.format_variable_assignment: Callable[[str, str, Value], str] = (
            variable_formatter(template="{name} = {value}")
        )
        self.static_preamble: Sequence[str] = ()
        self.static_body_preamble: Sequence[str] = ()
        self.scalar_preamble: dict[type, tuple[str, ...]] = (
            date_scalar_preamble(
                date_format=date_format,
                datetime_format=datetime_format,
            )
        )
        self.scalar_body_preamble: dict[type, tuple[str, ...]] = {}
        self.type_hint_collection_preamble_lines: tuple[str, ...] = ()
