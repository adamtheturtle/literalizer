"""Rust language specification."""

import datetime
import enum
from collections.abc import Callable
from types import MappingProxyType
from typing import TYPE_CHECKING

from beartype import beartype

from literalizer._formatters import (
    fixed_dict_open,
    fixed_sequence_open,
    fixed_set_open,
    format_bytes_hex,
    format_date_iso,
    format_datetime_iso,
    format_integer_binary,
    format_integer_hex,
    format_integer_octal,
    format_integer_underscore,
    format_string_backslash,
    passthrough_sequence_entry,
    passthrough_set_entry,
    tuple_dict_entry,
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

if TYPE_CHECKING:
    from collections.abc import Sequence

    from literalizer._types import Value


@beartype
def _format_date_rust(value: datetime.date) -> str:
    """Format a date as a Rust ``NaiveDate::from_ymd_opt(...)`` call."""
    return (
        f"NaiveDate::from_ymd_opt({value.year}, {value.month}, {value.day})"
        ".unwrap()"
    )


@beartype
def _format_datetime_rust(value: datetime.datetime) -> str:
    """Format a datetime as a Rust ``NaiveDateTime::new(...)`` call."""
    date = _format_date_rust(value=value)
    if value.microsecond:
        time_call = (
            f"NaiveTime::from_hms_micro_opt("
            f"{value.hour}, {value.minute}, {value.second}, "
            f"{value.microsecond}).unwrap()"
        )
    else:
        time_call = (
            f"NaiveTime::from_hms_opt("
            f"{value.hour}, {value.minute}, {value.second}).unwrap()"
        )
    return f"NaiveDateTime::new({date}, {time_call})"


@beartype
class Rust(metaclass=LanguageCls):
    """Rust language specification.

    Args:
        date_format: How to format :class:`datetime.date` values.

            * ``date_formats.RUST`` —
              ``NaiveDate::from_ymd_opt(...)`` call,
              e.g. ``NaiveDate::from_ymd_opt(2024, 1, 15).unwrap()``.
              Requires the ``chrono`` crate.
            * ``date_formats.ISO`` — ISO 8601 quoted string,
              e.g. ``"2024-01-15"``.

        datetime_format: How to format :class:`datetime.datetime` values.

            * ``datetime_formats.RUST`` —
              ``NaiveDateTime::new(...)`` call, e.g.
              ``NaiveDateTime::new(NaiveDate::from_ymd_opt(2024, 1, 15)
              .unwrap(), NaiveTime::from_hms_opt(12, 30, 0).unwrap())``.
              Requires the ``chrono`` crate.
            * ``datetime_formats.ISO`` — ISO 8601 quoted string,
              e.g. ``"2024-01-15T12:30:00"``.

        sequence_format: Which Rust sequence type to use.

            * ``sequence_formats.VEC`` — ``vec![]`` macro,
              e.g. ``vec![1, 2, 3]``.  Because ``Vec`` is
              homogeneous, mixed-type sequences have all elements
              coerced to strings.
            * ``sequence_formats.ARRAY`` — fixed-size array literal,
              e.g. ``[1, 2, 3]``.  Because Rust arrays are
              homogeneous, mixed-type sequences have all elements
              coerced to strings.
            * ``sequence_formats.TUPLE`` — tuple literal,
              e.g. ``(1, 2, 3)``.
    """

    extension = ".rs"
    pygments_name = "rust"

    class DateFormats(enum.Enum):
        """Date format options for Rust."""

        RUST = DateFormatConfig(
            formatter=_format_date_rust,
            preamble_lines=("use chrono::NaiveDate;",),
        )
        ISO = DateFormatConfig(formatter=format_date_iso, type_produced=str)

        def __call__(self, date_value: datetime.date, /) -> str:
            """Format a date."""
            return self.value.formatter(date_value)

    class DatetimeFormats(enum.Enum):
        """Datetime format options for Rust."""

        RUST = DatetimeFormatConfig(
            formatter=_format_datetime_rust,
            preamble_lines=(
                "use chrono::NaiveDate;",
                "use chrono::NaiveDateTime;",
                "use chrono::NaiveTime;",
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
        """Sequence type options for Rust."""

        VEC = SequenceFormatConfig(
            sequence_open=fixed_sequence_open(open_str="vec!["),
            close="]",
            supports_heterogeneity=False,
            single_element_trailing_comma=False,
            empty_sequence="Vec::<String>::new()",
            preamble_lines=(),
            format_entry=passthrough_sequence_entry,
            typed_opener_fallback=None,
        )
        ARRAY = SequenceFormatConfig(
            sequence_open=fixed_sequence_open(open_str="["),
            close="]",
            supports_heterogeneity=False,
            single_element_trailing_comma=False,
            empty_sequence=None,
            preamble_lines=(),
            format_entry=passthrough_sequence_entry,
            typed_opener_fallback=None,
        )
        TUPLE = SequenceFormatConfig(
            sequence_open=fixed_sequence_open(open_str="("),
            close=")",
            supports_heterogeneity=True,
            single_element_trailing_comma=False,
            empty_sequence=None,
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
        """Set type options for Rust."""

        HASH_SET = SetFormatConfig(
            set_open=fixed_set_open(open_str="HashSet::from(["),
            close="])",
            empty_set="HashSet::<String>::new()",
            preamble_lines=("use std::collections::HashSet;",),
            set_opener_template="",
        )
        BTREE_SET = SetFormatConfig(
            set_open=fixed_set_open(open_str="BTreeSet::from(["),
            close="])",
            empty_set="BTreeSet::<String>::new()",
            preamble_lines=("use std::collections::BTreeSet;",),
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

        LET = DeclarationStyleConfig(
            formatter=variable_formatter(template="let {name} = {value};"),
        )
        LET_MUT = DeclarationStyleConfig(
            formatter=variable_formatter(template="let mut {name} = {value};"),
        )

    class DictFormats(enum.Enum):
        """Dict/map format options."""

        HASH_MAP = "hash_map"

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
                "NONE": format_integer_octal,
                "UNDERSCORE": format_integer_octal,
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
        date_format: DateFormats = DateFormats.RUST,
        datetime_format: DatetimeFormats = DatetimeFormats.RUST,
        bytes_format: BytesFormats = BytesFormats.HEX,
        sequence_format: SequenceFormats = SequenceFormats.VEC,
        set_format: SetFormats = SetFormats.HASH_SET,
        variable_type_hints: VariableTypeHints = VariableTypeHints.NONE,
        comment_format: CommentFormats = CommentFormats.DOUBLE_SLASH,
        _variable_type_hints: VariableTypeHints = VariableTypeHints.NONE,
        declaration_style: DeclarationStyles = DeclarationStyles.LET,
        dict_format: DictFormats = DictFormats.HASH_MAP,
        integer_format: IntegerFormats = IntegerFormats.DECIMAL,
        numeric_separator: NumericSeparators = NumericSeparators.NONE,
        string_format: StringFormats = StringFormats.DOUBLE,
        trailing_comma: TrailingCommas = TrailingCommas.YES,
        line_ending: LineEndings = LineEndings.SEMICOLON,
    ) -> None:
        """Initialize Rust language specification."""
        self.variable_type_hints = variable_type_hints
        self.sequence_format = sequence_format
        self.null_literal = "None::<()>"
        self.true_literal = "true"
        self.false_literal = "false"
        fmt = sequence_format.value
        self.sequence_format_config: SequenceFormatConfig = fmt
        self.set_format = set_format
        self.set_format_config: SetFormatConfig = set_format.value
        self.sequence_open: Callable[[list[Value]], str] = fmt.sequence_open
        self.dict_format_config: DictFormatConfig = DictFormatConfig(
            open_fn=fixed_dict_open(open_str="HashMap::from(["),
            close="])",
            format_entry=tuple_dict_entry(
                format_value=passthrough_sequence_entry
            ),
            empty_dict="HashMap::<&str, &str>::from([])",
            preamble_lines=("use std::collections::HashMap;",),
        )
        self.multiline_trailing_comma: bool = trailing_comma.name == "YES"
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
                open_str="HashMap::from([",
                close="])",
                preamble_lines=("use std::collections::HashMap;",),
            )
        )
        self.format_ordered_map_entry: Callable[[str, Value, str], str] = (
            tuple_dict_entry(format_value=passthrough_sequence_entry)
        )
        self.multiline_close_indent = ""
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
        self.scalar_preamble: dict[type, tuple[str, ...]] = (
            date_scalar_preamble(
                date_format=date_format,
                datetime_format=datetime_format,
            )
        )
        self.scalar_body_preamble: dict[type, tuple[str, ...]] = {}
        self.type_hint_collection_preamble_lines: tuple[str, ...] = ()
