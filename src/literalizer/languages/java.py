"""Java language specification."""

import datetime
import enum
from collections.abc import Callable
from types import MappingProxyType
from typing import TYPE_CHECKING, Any

from beartype import beartype

from literalizer._formatters import (
    TypedOpenerConfig,
    date_ymd_formatter,
    datetime_iso_formatter,
    dict_entry_with_template,
    fixed_dict_open,
    fixed_set_open,
    format_bytes_hex,
    format_date_iso,
    format_datetime_iso,
    format_integer_binary,
    format_integer_hex,
    format_integer_octal_c_style,
    format_integer_underscore,
    format_string_backslash,
    make_element_to_type,
    make_type_to_opener,
    passthrough_sequence_entry,
    passthrough_set_entry,
    typed_sequence_open,
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
    date_scalar_preamble,
)
from literalizer.exceptions import NullInCollectionError

if TYPE_CHECKING:
    from collections.abc import Sequence

    from literalizer._types import Value


@beartype
def _format_datetime_java_zoned(value: datetime.datetime) -> str:
    """Format a datetime as a Java ``ZonedDateTime.of(...)`` call."""
    tz = value.tzname() or "UTC"
    nanos = value.microsecond * 1000
    return (
        f"ZonedDateTime.of({value.year}, {value.month}, {value.day}, "
        f"{value.hour}, {value.minute}, {value.second}, "
        f'{nanos}, ZoneId.of("{tz}"))'
    )


@beartype
def _list_of_open(items: list[Any]) -> str:
    """Return ``List.of(`` after checking for null elements.

    Java's ``List.of()`` throws ``NullPointerException`` on null elements.
    """
    if any(item is None for item in items):
        msg = (
            "Java's List.of() does not accept null elements. "
            "Use sequence_format=ARRAY instead."
        )
        raise NullInCollectionError(msg)
    return "List.of("


@beartype
class Java(metaclass=LanguageCls):
    """Java language specification.

    Args:
        date_format: How to format :class:`datetime.date` values.

            * ``date_formats.JAVA`` — ``LocalDate.of(...)`` call,
              e.g. ``LocalDate.of(2024, 1, 15)``.
            * ``date_formats.ISO`` — ISO 8601 quoted string,
              e.g. ``"2024-01-15"``.

        datetime_format: How to format :class:`datetime.datetime` values.

            * ``datetime_formats.INSTANT`` — ``Instant.parse(...)`` call,
              e.g. ``Instant.parse("2024-01-15T12:30:00")``.
            * ``datetime_formats.ZONED`` — ``ZonedDateTime.of(...)`` call,
              e.g. ``ZonedDateTime.of(2024, 1, 15, 12, 30, 0, 0,
              ZoneId.of("UTC"))``.
            * ``datetime_formats.ISO`` — ISO 8601 quoted string,
              e.g. ``"2024-01-15T12:30:00"``.

        sequence_format: How to format sequences.

            * ``sequence_formats.ARRAY`` — Java array literal,
              e.g. ``new Object[]{1, 2, 3}``.
            * ``sequence_formats.LIST`` — ``List.of(...)`` call,
              e.g. ``List.of(1, 2, 3)``.
    """

    extension = ".java"
    pygments_name = "java"

    class DateFormats(enum.Enum):
        """Date formatting options for Java."""

        JAVA = DateFormatConfig(
            formatter=date_ymd_formatter(
                template="LocalDate.of({year}, {month}, {day})",
            ),
            preamble_lines=("import java.time.LocalDate;",),
        )
        ISO = DateFormatConfig(formatter=format_date_iso, type_produced=str)

        def __call__(self, date_value: datetime.date, /) -> str:
            """Format a date."""
            return self.value.formatter(date_value)

    class DatetimeFormats(enum.Enum):
        """Datetime formatting options for Java."""

        INSTANT = DatetimeFormatConfig(
            formatter=datetime_iso_formatter(
                template='Instant.parse("{iso}")',
            ),
            preamble_lines=("import java.time.Instant;",),
        )
        ZONED = DatetimeFormatConfig(
            formatter=_format_datetime_java_zoned,
            preamble_lines=(
                "import java.time.ZoneId;",
                "import java.time.ZonedDateTime;",
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
        """Sequence type options for Java."""

        ARRAY = SequenceFormatConfig(
            sequence_open=typed_sequence_open(
                type_to_opener=make_type_to_opener(
                    element_to_type=make_element_to_type(
                        str_type="String",
                        bool_type="boolean",
                        int_type="int",
                        float_type="double",
                        mixed_numeric_type="double",
                        bytes_type="String",
                        date_type="LocalDate",
                        list_template="{inner}[]",
                    ),
                    opener_template="new {type_name}[]{{",
                ),
                fallback="new Object[]{",
            ),
            close="}",
            supports_heterogeneity=True,
            single_element_trailing_comma=False,
            empty_sequence=None,
            preamble_lines=(),
            format_entry=passthrough_sequence_entry,
            typed_opener_fallback="new Object[]{",
        )
        LIST = SequenceFormatConfig(
            sequence_open=_list_of_open,
            format_entry=passthrough_sequence_entry,
            typed_opener_fallback=None,
            close=")",
            supports_heterogeneity=True,
            single_element_trailing_comma=False,
            empty_sequence="List.of()",
            preamble_lines=("import java.util.List;",),
        )

        @property
        def supports_heterogeneity(self) -> bool:
            """Whether this sequence format supports mixed-type
            elements.
            """
            return self.value.supports_heterogeneity

    class SetFormats(enum.Enum):
        """Set type options for Java."""

        SET = SetFormatConfig(
            set_open=fixed_set_open(open_str="Set.of("),
            close=")",
            empty_set=None,
            preamble_lines=("import java.util.Set;",),
            set_opener_template="",
        )
        TREE_SET = SetFormatConfig(
            set_open=fixed_set_open(open_str="new TreeSet<>(Set.of("),
            close="))",
            empty_set="new TreeSet<>()",
            preamble_lines=(
                "import java.util.Set;",
                "import java.util.TreeSet;",
            ),
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

        VAR = "var"

    class DictFormats(enum.Enum):
        """Dict/map format options."""

        MAP_OF_ENTRIES = DictFormatConfig(
            open_fn=fixed_dict_open(open_str="Map.ofEntries("),
            close=")",
            format_entry=dict_entry_with_template(
                template="Map.entry({key}, {value})",
                format_value=passthrough_sequence_entry,
            ),
            empty_dict=None,
            preamble_lines=("import java.util.Map;",),
        )
        HASH_MAP = DictFormatConfig(
            open_fn=fixed_dict_open(open_str="new HashMap<>(Map.ofEntries("),
            close="))",
            format_entry=dict_entry_with_template(
                template="Map.entry({key}, {value})",
                format_value=passthrough_sequence_entry,
            ),
            empty_dict="new HashMap<>()",
            preamble_lines=(
                "import java.util.HashMap;",
                "import java.util.Map;",
            ),
        )

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
        OCTAL = MappingProxyType(
            mapping={
                "NONE": format_integer_octal_c_style,
                "UNDERSCORE": format_integer_octal_c_style,
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
        date_format: DateFormats = DateFormats.JAVA,
        datetime_format: DatetimeFormats = DatetimeFormats.INSTANT,
        bytes_format: BytesFormats = BytesFormats.HEX,
        sequence_format: SequenceFormats = SequenceFormats.ARRAY,
        set_format: SetFormats = SetFormats.SET,
        variable_type_hints: VariableTypeHints = VariableTypeHints.NONE,
        comment_format: CommentFormats = CommentFormats.DOUBLE_SLASH,
        _variable_type_hints: VariableTypeHints = VariableTypeHints.NONE,
        declaration_style: DeclarationStyles = DeclarationStyles.VAR,
        dict_format: DictFormats = DictFormats.MAP_OF_ENTRIES,
        integer_format: IntegerFormats = IntegerFormats.DECIMAL,
        numeric_separator: NumericSeparators = NumericSeparators.NONE,
        string_format: StringFormats = StringFormats.DOUBLE,
        trailing_comma: TrailingCommas = TrailingCommas.NO,
        line_ending: LineEndings = LineEndings.SEMICOLON,
    ) -> None:
        """Initialize Java language specification."""
        self.variable_type_hints = variable_type_hints
        self.sequence_format = sequence_format
        self.null_literal = "null"
        self.true_literal = "true"
        self.false_literal = "false"
        fmt = sequence_format.value
        self.sequence_format_config: SequenceFormatConfig = fmt
        self.set_format = set_format
        java_dict_entry = dict_entry_with_template(
            template="Map.entry({key}, {value})",
            format_value=passthrough_sequence_entry,
        )
        self.set_format_config: SetFormatConfig = set_format.value

        date_tp = date_format.value.type_produced
        opener_config = TypedOpenerConfig(
            str_type="String",
            bool_type="boolean",
            int_type="int",
            float_type="double",
            mixed_numeric_type="double",
            bytes_type="String",
            date_type="LocalDate",
            datetime_type=None,
            list_template="{inner}[]",
            sequence_opener_template="new {type_name}[]{{",
            dict_opener_template="new {type_name}[]{{",
            set_opener_template="Set.of(",
        )
        openers = opener_config.build(
            date_type=opener_config.type_name(py_type=date_tp),
            datetime_type=opener_config.type_name(
                py_type=datetime_format.value.type_produced,
            ),
        )
        self.sequence_open: Callable[[list[Value]], str] = (
            typed_sequence_open(
                type_to_opener=openers.seq,
                fallback=fmt.typed_opener_fallback,
            )
            if fmt.typed_opener_fallback is not None
            else fmt.sequence_open
        )
        self.dict_format_config: DictFormatConfig = dict_format.value
        self.trailing_comma_config: TrailingCommaConfig = trailing_comma.value
        self.format_bytes: Callable[[bytes], str] = bytes_format
        self.format_date: Callable[[datetime.date], str] = date_format
        self.format_datetime: Callable[[datetime.datetime], str] = (
            datetime_format
        )
        self.format_string: Callable[[str], str] = format_string_backslash
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
                open_str="new java.util.ArrayList<>(java.util.Arrays.asList(",
                close="))",
                preamble_lines=("import java.util.Map;",),
            )
        )
        self.format_ordered_map_entry: Callable[[str, Value, str], str] = (
            java_dict_entry
        )
        self.multiline_close_indent = ""
        self.element_separator = ", "
        self.skip_null_dict_values = True
        self.supports_collection_comments = True
        self.format_variable_declaration: Callable[[str, str, Value], str] = (
            variable_formatter(template="var {name} = {value};")
        )
        self.format_variable_assignment: Callable[[str, str, Value], str] = (
            variable_formatter(template="{name} = {value};")
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
        self.compute_body_preamble: Callable[
            [frozenset[type], Value], tuple[str, ...]
        ] = body_preamble_from_scalars(
            scalar_body_preamble=self.scalar_body_preamble,
        )

        self.type_hint_collection_preamble_lines: tuple[str, ...] = ()
