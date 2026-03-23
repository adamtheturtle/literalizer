"""Kotlin language specification."""

import dataclasses
import datetime
import enum
from typing import TYPE_CHECKING

from beartype import beartype

from literalizer._formatters import (
    ListType,
    TypedOpenerConfig,
    dict_entry_with_separator,
    fixed_sequence_open,
    format_bytes_hex,
    format_date_iso,
    format_datetime_iso,
    format_string_backslash_dollar,
    make_element_to_type,
    make_type_to_opener,
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
    from collections.abc import Callable, Sequence


@beartype
def _format_date_kotlin(value: datetime.date) -> str:
    """Format a date as a Kotlin ``LocalDate.of(...)`` call."""
    return f"LocalDate.of({value.year}, {value.month}, {value.day})"


@beartype
def _format_datetime_kotlin(value: datetime.datetime) -> str:
    """Format a datetime as a Kotlin ``LocalDateTime.of(...)`` call."""
    return (
        f"LocalDateTime.of({value.year}, {value.month}, {value.day}, "
        f"{value.hour}, {value.minute}, {value.second})"
    )


_KOTLIN_SCALAR_OPENERS: dict[type, str] = {
    str: "arrayOf(",
    bool: "booleanArrayOf(",
    int: "intArrayOf(",
    float: "doubleArrayOf(",
    bytes: "arrayOf(",
    datetime.date: "arrayOf(",
    datetime.datetime: "arrayOf(",
}


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
    return _KOTLIN_SCALAR_OPENERS.get(element_type)


_KOTLIN_SCALAR_TYPES: dict[type, str] = {
    str: "String",
    bool: "Boolean",
    int: "Int",
    float: "Double",
    bytes: "String",
    datetime.date: "LocalDate",
    datetime.datetime: "LocalDateTime",
}

_kotlin_opener_config = TypedOpenerConfig(
    scalar_types=_KOTLIN_SCALAR_TYPES,
    list_template="Array<{inner}>",
    seq_opener_template="arrayOf(",
    dict_opener_template="mapOf<String, {type_name}>(",
    set_opener_template="setOf<{type_name}>(",
)

_KOTLIN_SET_OPENER_TEMPLATES: dict[str, tuple[str, str]] = {
    "SET": ("setOf<{type_name}>(", "setOf<Any?>("),
    "SORTED_SET": ("sortedSetOf<{type_name}>(", "sortedSetOf<Any?>("),
}

_kotlin_element_to_type_default = make_element_to_type(
    scalar_types=_KOTLIN_SCALAR_TYPES,
    list_template="Array<{inner}>",
)


@beartype
def _format_kotlin_ordered_map_entry(key: str, value: str) -> str:
    """Format a Kotlin ordered-map entry."""
    return f"{key} to {value}"


@beartype
def _format_variable_declaration_val(
    name: str, value: str, _data: Value
) -> str:
    """Format a Kotlin ``val`` variable declaration."""
    return f"val {name} = {value}"


@beartype
def _format_variable_declaration_var(
    name: str, value: str, _data: Value
) -> str:
    """Format a Kotlin ``var`` variable declaration."""
    return f"var {name} = {value}"


@beartype
def _format_variable_assignment(name: str, value: str, _data: Value) -> str:
    """Format a Kotlin variable assignment."""
    return f"{name} = {value}"


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
            formatter=_format_date_kotlin,
            preamble_lines=("import java.time.LocalDate",),
        )
        ISO = DateFormatConfig(formatter=format_date_iso, type_produced=str)

        def __call__(self, date_value: datetime.date, /) -> str:
            """Format a date."""
            return self.value.formatter(date_value)

    class DatetimeFormats(enum.Enum):
        """Datetime format options for Kotlin."""

        KOTLIN = DatetimeFormatConfig(
            formatter=_format_datetime_kotlin,
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
        )
        ARRAY = SequenceFormatConfig(
            sequence_open=fixed_sequence_open(open_str="arrayOf<Any?>("),
            close=")",
            supports_heterogeneity=True,
            single_element_trailing_comma=False,
            empty_sequence=None,
            preamble_lines=(),
            format_entry=passthrough_sequence_entry,
        )
        TUPLE = SequenceFormatConfig(
            sequence_open=_kotlin_tuple_open,
            format_entry=passthrough_sequence_entry,
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
                type_to_opener=make_type_to_opener(
                    element_to_type=_kotlin_element_to_type_default,
                    opener_template=_KOTLIN_SET_OPENER_TEMPLATES["SET"][0],
                ),
                fallback=_KOTLIN_SET_OPENER_TEMPLATES["SET"][1],
            ),
            close=")",
            empty_set=None,
            preamble_lines=(),
        )
        SORTED_SET = SetFormatConfig(
            set_open=typed_set_open(
                type_to_opener=make_type_to_opener(
                    element_to_type=_kotlin_element_to_type_default,
                    opener_template=_KOTLIN_SET_OPENER_TEMPLATES["SORTED_SET"][
                        0
                    ],
                ),
                fallback=_KOTLIN_SET_OPENER_TEMPLATES["SORTED_SET"][1],
            ),
            close=")",
            empty_set=None,
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

        VAL = DeclarationStyleConfig(
            formatter=_format_variable_declaration_val,
        )
        VAR = DeclarationStyleConfig(
            formatter=_format_variable_declaration_var,
        )

    class DictFormats(enum.Enum):
        """Dict/map format options."""

        MAP = "map"

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
            scalar_type_overrides={
                datetime.date: _KOTLIN_SCALAR_TYPES[date_tp],
                datetime.datetime: _KOTLIN_SCALAR_TYPES[dt_tp],
            },
        )
        _set_template, _set_fallback = _KOTLIN_SET_OPENER_TEMPLATES[
            set_format.name
        ]
        _set_eto = make_element_to_type(
            scalar_types={
                **_KOTLIN_SCALAR_TYPES,
                datetime.date: _KOTLIN_SCALAR_TYPES[date_tp],
                datetime.datetime: _KOTLIN_SCALAR_TYPES[dt_tp],
            },
            list_template="Array<{inner}>",
        )
        self.set_format_config: SetFormatConfig = dataclasses.replace(
            set_format.value,
            set_open=typed_set_open(
                type_to_opener=make_type_to_opener(
                    element_to_type=_set_eto,
                    opener_template=_set_template,
                ),
                fallback=_set_fallback,
            ),
        )
        self.dict_format_config: DictFormatConfig = DictFormatConfig(
            open_fn=typed_dict_open(
                type_to_opener=openers.dict,
                fallback="mapOf<String, Any?>(",
            ),
            close=")",
            format_entry=dict_entry_with_separator(separator=" to "),
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
        self.line_ending = line_ending
        self.comment_config: CommentConfig = comment_format.value
        self.ordered_map_format_config: OrderedMapFormatConfig = (
            OrderedMapFormatConfig(
                open_str="linkedMapOf<String, Any?>(",
                close=")",
                preamble_lines=(),
            )
        )
        self.format_ordered_map_entry: Callable[[str, str], str] = (
            _format_kotlin_ordered_map_entry
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
        self.scalar_preamble: dict[type, tuple[str, ...]] = (
            date_scalar_preamble(
                date_format=date_format,
                datetime_format=datetime_format,
            )
        )
        self.scalar_body_preamble: dict[type, tuple[str, ...]] = {}
        self.type_hint_collection_preamble_lines: tuple[str, ...] = ()
