"""Java language specification."""

import datetime
import enum
from collections.abc import Callable
from types import MappingProxyType
from typing import TYPE_CHECKING, Any

from beartype import beartype

from literalizer._formatters.collection_openers import (
    TypedOpenerConfig,
    fixed_dict_open,
    fixed_sequence_open,
    fixed_set_open,
    typed_collection_open,
)
from literalizer._formatters.format_dates import (
    date_ymd_formatter,
    datetime_iso_formatter,
    format_date_iso,
    format_datetime_iso,
)
from literalizer._formatters.format_entries import (
    dict_entry_with_template,
    format_bytes_base64,
    format_bytes_hex,
    passthrough_sequence_entry,
    passthrough_set_entry,
    variable_formatter,
)
from literalizer._formatters.format_floats import (
    format_float_fixed,
    format_float_repr,
    format_float_scientific,
)
from literalizer._formatters.format_integers import (
    format_integer_binary,
    format_integer_hex,
    format_integer_octal_c_style,
    format_integer_underscore,
    make_long_suffix_formatter,
)
from literalizer._formatters.format_strings import format_string_backslash
from literalizer._language import (
    CommentConfig,
    DateFormatConfig,
    DatetimeFormatConfig,
    DeclarationStyleConfig,
    DictFormatConfig,
    FloatSpecialsMixin,
    LanguageCls,
    OrderedMapFormatConfig,
    SequenceFormatConfig,
    SetFormatConfig,
    TrailingCommaConfig,
    body_preamble_from_scalars,
    date_scalar_preamble,
    no_type_hint_preamble,
)
from literalizer.exceptions import NullInCollectionError

if TYPE_CHECKING:
    from collections.abc import Sequence

    from literalizer._types import Value


@beartype
def _format_datetime_java_zoned(value: datetime.datetime) -> str:
    """Format a datetime as a Java ``ZonedDateTime.of(...)`` call."""
    timezone_name = value.tzname() or "UTC"
    nanoseconds = value.microsecond * 1000
    return (
        f"ZonedDateTime.of({value.year}, {value.month}, {value.day}, "
        f"{value.hour}, {value.minute}, {value.second}, "
        f'{nanoseconds}, ZoneId.of("{timezone_name}"))'
    )


@beartype
def _list_of_open(items: list[Any]) -> str:
    """Return ``List.of(`` after checking for null elements.

    Java's ``List.of()`` throws ``NullPointerException`` on null elements.
    """
    if any(item is None for item in items):
        msg = (
            f"Java's List.of() does not accept null elements"
            f" (got {len(items)} items, including null). "
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
    supports_default_set_element_type = False
    supports_default_sequence_element_type = False
    supports_default_dict_value_type = False
    supports_default_dict_key_type = False
    supports_default_ordered_map_value_type = False
    supports_non_printable_ascii_dict_keys = True

    _opener_config = TypedOpenerConfig(
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
        dict_type_template=None,
        fallback_value_type=None,
    )

    _opener_config_long = TypedOpenerConfig(
        str_type="String",
        bool_type="boolean",
        int_type="long",
        float_type="double",
        mixed_numeric_type="double",
        bytes_type="String",
        date_type="LocalDate",
        datetime_type=None,
        list_template="{inner}[]",
        sequence_opener_template="new {type_name}[]{{",
        dict_opener_template="new {type_name}[]{{",
        set_opener_template="Set.of(",
        dict_type_template=None,
        fallback_value_type=None,
    )

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
        BASE64 = enum.member(value=format_bytes_base64)

        def __call__(self, data: bytes, /) -> str:
            """Format bytes."""
            return self.value(value=data)

    class SequenceFormats(enum.Enum):
        """Sequence type options for Java."""

        ARRAY = SequenceFormatConfig(
            sequence_open=fixed_sequence_open(open_str="new Object[]{"),
            close="}",
            supports_heterogeneity=True,
            single_element_trailing_comma=False,
            supports_trailing_comma=True,
            empty_sequence=None,
            preamble_lines=(),
            format_entry=passthrough_sequence_entry,
            typed_opener_fallback="new Object[]{",
            uses_typed_literal_for_scalars=False,
            requires_uniform_record_shapes=False,
            declared_type=None,
        )
        LIST = SequenceFormatConfig(
            sequence_open=_list_of_open,
            format_entry=passthrough_sequence_entry,
            typed_opener_fallback=None,
            uses_typed_literal_for_scalars=False,
            requires_uniform_record_shapes=False,
            close=")",
            supports_heterogeneity=True,
            single_element_trailing_comma=False,
            supports_trailing_comma=False,
            empty_sequence="List.of()",
            preamble_lines=("import java.util.List;",),
            declared_type=None,
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
            coerce_mixed_to_str=False,
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
            coerce_mixed_to_str=False,
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

        VAR = DeclarationStyleConfig(
            formatter=variable_formatter(template="var {name} = {value};"),
            supports_redefinition=True,
        )

    class DictEntryStyles(enum.Enum):
        """Dict entry style options."""

        DEFAULT = enum.auto()

    class DictFormats(enum.Enum):
        """Dict/map format options."""

        MAP_OF_ENTRIES = DictFormatConfig(
            dict_open=fixed_dict_open(open_str="Map.ofEntries("),
            close=")",
            format_entry=dict_entry_with_template(
                template="Map.entry({key}, {value})",
                format_value=passthrough_sequence_entry,
            ),
            empty_dict=None,
            preamble_lines=("import java.util.Map;",),
            narrowed_open=None,
        )
        HASH_MAP = DictFormatConfig(
            dict_open=fixed_dict_open(open_str="new HashMap<>(Map.ofEntries("),
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
            narrowed_open=None,
        )

    class EmptyDictKey(enum.Enum):
        """Empty dict key options."""

        ALLOW = enum.auto()

    class FloatFormats(
        FloatSpecialsMixin,
        enum.Enum,
        positive_infinity="Double.POSITIVE_INFINITY",
        negative_infinity="Double.NEGATIVE_INFINITY",
        nan="Double.NaN",
    ):
        """Float format options."""

        REPR = enum.member(value=format_float_repr)
        SCIENTIFIC = enum.member(value=format_float_scientific)
        FIXED = enum.member(value=format_float_fixed)

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

    class NumericLiteralSuffixes(enum.Enum):
        """Numeric literal suffix options."""

        NONE = enum.auto()
        AUTO = enum.auto()

    class NumericSeparators(enum.Enum):
        """Numeric separator options."""

        NONE = enum.auto()
        UNDERSCORE = enum.auto()

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

        AUTO = enum.auto()

    variable_type_hints_formats = VariableTypeHints
    declaration_styles = DeclarationStyles
    dict_entry_styles = DictEntryStyles
    dict_formats = DictFormats
    empty_dict_keys = EmptyDictKey
    float_formats = FloatFormats
    integer_formats = IntegerFormats
    numeric_literal_suffixes = NumericLiteralSuffixes
    numeric_separators = NumericSeparators
    string_formats = StringFormats
    trailing_commas = TrailingCommas

    class LineEndings(enum.Enum):
        """Line ending options."""

        SEMICOLON = "semicolon"

    line_endings = LineEndings

    def __init__(  # noqa: PLR0915
        self,
        *,
        date_format: DateFormats = DateFormats.JAVA,
        datetime_format: DatetimeFormats = DatetimeFormats.INSTANT,
        bytes_format: BytesFormats = BytesFormats.HEX,
        sequence_format: SequenceFormats = SequenceFormats.ARRAY,
        set_format: SetFormats = SetFormats.SET,
        variable_type_hints: VariableTypeHints = VariableTypeHints.AUTO,
        comment_format: CommentFormats = CommentFormats.DOUBLE_SLASH,
        declaration_style: DeclarationStyles = DeclarationStyles.VAR,
        dict_entry_style: DictEntryStyles = DictEntryStyles.DEFAULT,
        dict_format: DictFormats = DictFormats.MAP_OF_ENTRIES,
        float_format: FloatFormats = FloatFormats.REPR,
        integer_format: IntegerFormats = IntegerFormats.DECIMAL,
        numeric_literal_suffix: NumericLiteralSuffixes = (
            NumericLiteralSuffixes.NONE
        ),
        numeric_separator: NumericSeparators = NumericSeparators.NONE,
        string_format: StringFormats = StringFormats.DOUBLE,
        trailing_comma: TrailingCommas = TrailingCommas.NO,
        line_ending: LineEndings = LineEndings.SEMICOLON,
        indent: str = "    ",
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
        suffix_is_auto = numeric_literal_suffix.name == "AUTO"
        cfg = (
            self._opener_config_long if suffix_is_auto else self._opener_config
        )
        openers = cfg.build(
            date_type=cfg.type_name(py_type=date_tp),
            datetime_type=cfg.type_name(
                py_type=datetime_format.value.type_produced,
            ),
            set_opener_template=None,
            narrow_dict_values=False,
        )
        self.sequence_open: Callable[[list[Value]], str] = (
            typed_collection_open(
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
        self.format_float: Callable[[float], str] = float_format
        base_int_formatter = integer_format.get_formatter(
            numeric_separator=numeric_separator,
        )
        self.format_integer: Callable[[int], str] = (
            make_long_suffix_formatter(base=base_int_formatter)
            if suffix_is_auto
            else base_int_formatter
        )
        self.format_sequence_entry: Callable[[Value, str], str] = (
            passthrough_sequence_entry
        )
        self.format_set_entry: Callable[[Value, str], str] = (
            passthrough_set_entry
        )
        self.comment_format = comment_format
        self.declaration_style = declaration_style
        self.dict_entry_style = dict_entry_style
        self.dict_format = dict_format
        self.float_format = float_format
        self.integer_format = integer_format
        self.numeric_literal_suffix = numeric_literal_suffix
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
        self.indent = indent
        self.indent_closing_delimiter = False
        self.element_separator = ", "
        self.skip_null_dict_values = True
        self.supports_collection_comments = True
        self.supports_scalar_before_comments = False
        self.supports_scalar_inline_comments = False
        self.format_variable_declaration: Callable[[str, str, Value], str] = (
            declaration_style.value.formatter
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

        self.type_hint_collection_preamble_lines = no_type_hint_preamble
        self.special_float_preamble: tuple[str, ...] = ()
