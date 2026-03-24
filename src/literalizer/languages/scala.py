"""Scala language specification."""

import dataclasses
import datetime
import enum
from collections.abc import Callable, Sequence

from beartype import beartype

from literalizer._formatters import (
    MixedNumeric,
    TypedOpenerConfig,
    dict_entry_with_separator,
    fixed_sequence_open,
    format_bytes_hex,
    format_date_iso,
    format_datetime_iso,
    format_string_backslash,
    make_element_to_type,
    make_type_to_opener,
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


@beartype
def _format_date_scala(value: datetime.date) -> str:
    """Format a date as a Scala ``LocalDate.of(...)`` call."""
    return f"LocalDate.of({value.year}, {value.month}, {value.day})"


@beartype
def _format_datetime_scala(value: datetime.datetime) -> str:
    """Format a datetime as a Scala ``ZonedDateTime.of(...)`` call."""
    tz = value.tzname() or "UTC"
    nanos = value.microsecond * 1000
    return (
        f"ZonedDateTime.of({value.year}, {value.month}, {value.day}, "
        f"{value.hour}, {value.minute}, {value.second}, "
        f'{nanos}, ZoneId.of("{tz}"))'
    )


_SCALA_SCALAR_TYPES: dict[type, str] = {
    str: "String",
    bool: "Boolean",
    int: "Int",
    float: "Double",
    MixedNumeric: "Double",
    bytes: "String",
    datetime.date: "LocalDate",
    datetime.datetime: "ZonedDateTime",
}

_scala_opener_config = TypedOpenerConfig(
    scalar_types=_SCALA_SCALAR_TYPES,
    list_template="Array[{inner}]",
    seq_opener_template="Array[{type_name}](",
    dict_opener_template="Map[String, {type_name}](",
    set_opener_template="Set[{type_name}](",
)


# The LIST format needs List[…] for nested type names, not Array[…].
_scala_list_element_to_type = make_element_to_type(
    scalar_types=_SCALA_SCALAR_TYPES,
    list_template="List[{inner}]",
)

_scala_list_type_to_opener = make_type_to_opener(
    element_to_type=_scala_list_element_to_type,
    opener_template="List[{type_name}](",
)


@beartype
def _list_sequence_open(
    *,
    date_type: str,
    datetime_type: str,
) -> Callable[[list[Value]], str]:
    """Build a typed sequence opener for the List format."""
    scalar_types = dict(_SCALA_SCALAR_TYPES)
    scalar_types[datetime.date] = date_type
    scalar_types[datetime.datetime] = datetime_type
    list_eto = make_element_to_type(
        scalar_types=scalar_types,
        list_template="List[{inner}]",
    )
    return typed_sequence_open(
        type_to_opener=make_type_to_opener(
            element_to_type=list_eto,
            opener_template="List[{type_name}](",
        ),
        fallback="List(",
    )


_string_format: Callable[[str], str] = format_string_backslash


@beartype
class Scala(metaclass=LanguageCls):
    """Scala language specification."""

    extension = ".scala"
    pygments_name = "scala"

    class DateFormats(enum.Enum):
        """Date format options for Scala."""

        SCALA = DateFormatConfig(
            formatter=_format_date_scala,
            preamble_lines=("import java.time.LocalDate",),
        )
        ISO = DateFormatConfig(formatter=format_date_iso, type_produced=str)

        def __call__(self, date_value: datetime.date, /) -> str:
            """Format a date."""
            return self.value.formatter(date_value)

    class DatetimeFormats(enum.Enum):
        """Datetime format options for Scala."""

        SCALA = DatetimeFormatConfig(
            formatter=_format_datetime_scala,
            preamble_lines=(
                "import java.time.ZoneId",
                "import java.time.ZonedDateTime",
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
        """Sequence type options for Scala."""

        LIST = SequenceFormatConfig(
            sequence_open=typed_sequence_open(
                type_to_opener=_scala_list_type_to_opener,
                fallback="List(",
            ),
            close=")",
            supports_heterogeneity=True,
            single_element_trailing_comma=False,
            empty_sequence=None,
            preamble_lines=(),
            format_entry=passthrough_sequence_entry,
        )
        SEQ = SequenceFormatConfig(
            sequence_open=fixed_sequence_open(open_str="Seq("),
            close=")",
            supports_heterogeneity=True,
            single_element_trailing_comma=False,
            empty_sequence=None,
            preamble_lines=(),
            format_entry=passthrough_sequence_entry,
        )
        ARRAY = SequenceFormatConfig(
            sequence_open=typed_sequence_open(
                type_to_opener=_scala_opener_config.build(
                    scalar_type_overrides={},
                    set_opener_template=None,
                ).seq,
                fallback="Array(",
            ),
            close=")",
            supports_heterogeneity=True,
            single_element_trailing_comma=False,
            empty_sequence=None,
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
        """Set type options for Scala."""

        SET = SetFormatConfig(
            set_open=typed_set_open(
                type_to_opener=_scala_opener_config.build(
                    scalar_type_overrides={},
                    set_opener_template=None,
                ).set,
                fallback="Set(",
            ),
            close=")",
            empty_set=None,
            preamble_lines=(),
            set_opener_template="",
        )
        TREE_SET = SetFormatConfig(
            set_open=typed_set_open(
                type_to_opener=_scala_opener_config.build(
                    scalar_type_overrides={},
                    set_opener_template="TreeSet[{type_name}](",
                ).set,
                fallback="TreeSet(",
            ),
            close=")",
            empty_set=None,
            preamble_lines=("import scala.collection.immutable.TreeSet",),
            set_opener_template="TreeSet[{type_name}](",
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
        )
        VAR = DeclarationStyleConfig(
            formatter=variable_formatter(template="var {name} = {value}"),
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

    def __init__(
        self,
        *,
        date_format: DateFormats = DateFormats.SCALA,
        datetime_format: DatetimeFormats = DatetimeFormats.SCALA,
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
    ) -> None:
        """Initialize Scala language specification."""
        self.variable_type_hints = variable_type_hints
        self.sequence_format = sequence_format
        self.null_literal = "null"
        self.true_literal = "true"
        self.false_literal = "false"
        fmt = sequence_format.value
        self.sequence_format_config: SequenceFormatConfig = fmt
        self.set_format = set_format
        date_tp = date_format.value.type_produced
        dt_tp = datetime_format.value.type_produced
        openers = _scala_opener_config.build(
            scalar_type_overrides={
                datetime.date: _SCALA_SCALAR_TYPES[date_tp],
                datetime.datetime: _SCALA_SCALAR_TYPES[dt_tp],
            },
            set_opener_template=set_format.value.set_opener_template or None,
        )
        self.set_format_config: SetFormatConfig = dataclasses.replace(
            set_format.value,
            set_open=typed_set_open(
                type_to_opener=openers.set,
                fallback=set_format.value.set_open([]),
            ),
        )
        self.sequence_open: Callable[[list[Value]], str] = (
            _list_sequence_open(
                date_type=_SCALA_SCALAR_TYPES[date_tp],
                datetime_type=_SCALA_SCALAR_TYPES[dt_tp],
            )
            if sequence_format is self.sequence_formats.LIST
            else typed_sequence_open(
                type_to_opener=openers.seq,
                fallback="Array(",
            )
            if sequence_format is self.sequence_formats.ARRAY
            else fmt.sequence_open
        )
        self.dict_format_config: DictFormatConfig = DictFormatConfig(
            open_fn=typed_dict_open(
                type_to_opener=openers.dict,
                fallback="Map(",
            ),
            close=")",
            format_entry=dict_entry_with_separator(separator=" -> "),
            empty_dict=None,
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
                open_str="scala.collection.immutable.ListMap(",
                close=")",
                preamble_lines=(),
            )
        )
        self.format_ordered_map_entry: Callable[[str, str], str] = (
            dict_entry_with_separator(separator=" -> ")
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
        self.scalar_preamble: dict[type, tuple[str, ...]] = (
            date_scalar_preamble(
                date_format=date_format,
                datetime_format=datetime_format,
            )
        )
        self.scalar_body_preamble: dict[type, tuple[str, ...]] = {}
        self.type_hint_collection_preamble_lines: tuple[str, ...] = ()
