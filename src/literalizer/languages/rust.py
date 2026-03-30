"""Rust language specification."""

import datetime
import enum
from collections.abc import Callable
from types import MappingProxyType
from typing import TYPE_CHECKING

from beartype import beartype

from literalizer._formatters.format_dates import (
    format_date_iso,
    format_datetime_iso,
)
from literalizer._formatters.format_entries import (
    format_bytes_base64,
    format_bytes_hex,
    passthrough_sequence_entry,
    passthrough_set_entry,
    tuple_dict_entry,
    variable_formatter,
)
from literalizer._formatters.format_factories import (
    dict_format_factory,
    sequence_format_factory,
    set_format_factory,
)
from literalizer._formatters.format_floats import (
    format_float_fixed,
    format_float_repr,
    format_float_scientific,
)
from literalizer._formatters.format_integers import (
    format_integer_binary,
    format_integer_hex,
    format_integer_octal,
    format_integer_underscore,
)
from literalizer._formatters.format_strings import (
    format_string_backslash,
    format_string_raw_rust,
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
    date_scalar_preamble,
    no_type_hint_preamble,
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

        default_sequence_element_type: Type name used for empty
            ``Vec`` literals, e.g. ``Vec::<String>::new()``.
            Defaults to ``"String"``.
    """

    extension = ".rs"
    pygments_name = "rust"
    supports_default_set_element_type = True
    supports_default_sequence_element_type = True
    supports_default_dict_value_type = True
    supports_default_dict_key_type = True
    supports_default_ordered_map_value_type = False

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
        BASE64 = enum.member(value=format_bytes_base64)

        def __call__(self, data: bytes, /) -> str:
            """Format bytes."""
            return self.value(value=data)

    class SequenceFormats(enum.Enum):
        """Sequence type options for Rust."""

        VEC = enum.member(
            value=sequence_format_factory(
                open_template="vec![",
                close="]",
                supports_heterogeneity=False,
                single_element_trailing_comma=False,
                supports_trailing_comma=True,
                empty_template="Vec::<{type}>::new()",
                preamble_lines=(),
                format_entry=passthrough_sequence_entry,
                typed_opener_fallback_template=None,
            )
        )
        ARRAY = enum.member(
            value=sequence_format_factory(
                open_template="[",
                close="]",
                supports_heterogeneity=False,
                single_element_trailing_comma=False,
                supports_trailing_comma=True,
                empty_template=None,
                preamble_lines=(),
                format_entry=passthrough_sequence_entry,
                typed_opener_fallback_template=None,
            )
        )
        TUPLE = enum.member(
            value=sequence_format_factory(
                open_template="(",
                close=")",
                supports_heterogeneity=True,
                single_element_trailing_comma=False,
                supports_trailing_comma=True,
                empty_template=None,
                preamble_lines=(),
                format_entry=passthrough_sequence_entry,
                typed_opener_fallback_template=None,
            )
        )

        def __call__(self, default_type: str) -> SequenceFormatConfig:
            """Create a sequence format config for the given type."""
            return self.value(default_type)

        @property
        def supports_heterogeneity(self) -> bool:
            """Whether this sequence format supports mixed-type
            elements.
            """
            return self(default_type="String").supports_heterogeneity

    class SetFormats(enum.Enum):
        """Set type options for Rust."""

        HASH_SET = enum.member(
            value=set_format_factory(
                open_template="HashSet::from([",
                close="])",
                empty_template="HashSet::<{type}>::new()",
                preamble_lines=("use std::collections::HashSet;",),
                set_opener_template="",
            )
        )
        BTREE_SET = enum.member(
            value=set_format_factory(
                open_template="BTreeSet::from([",
                close="])",
                empty_template="BTreeSet::<{type}>::new()",
                preamble_lines=("use std::collections::BTreeSet;",),
                set_opener_template="",
            )
        )

        def __call__(self, default_type: str) -> SetFormatConfig:
            """Create a set format config for the given type."""
            return self.value(default_type)

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
            supports_redefinition=True,
        )
        LET_MUT = DeclarationStyleConfig(
            formatter=variable_formatter(template="let mut {name} = {value};"),
            supports_redefinition=True,
        )

    class DictEntryStyles(enum.Enum):
        """Dict entry style options."""

        DEFAULT = "default"

    class DictFormats(enum.Enum):
        """Dict/map format options."""

        HASH_MAP = enum.member(
            value=dict_format_factory(
                open_template="HashMap::from([",
                close="])",
                format_entry=tuple_dict_entry(
                    format_value=passthrough_sequence_entry
                ),
                empty_template="HashMap::<{key_type}, {type}>::from([])",
                preamble_lines=("use std::collections::HashMap;",),
                narrowed_open=None,
            )
        )
        BTREE_MAP = enum.member(
            value=dict_format_factory(
                open_template="BTreeMap::from([",
                close="])",
                format_entry=tuple_dict_entry(
                    format_value=passthrough_sequence_entry
                ),
                empty_template="BTreeMap::<{key_type}, {type}>::from([])",
                preamble_lines=("use std::collections::BTreeMap;",),
                narrowed_open=None,
            )
        )

        def __call__(
            self,
            default_type: str,
            *,
            default_key_type: str = "&str",
        ) -> DictFormatConfig:
            """Create a dict format config for the given type."""
            return self.value(
                default_type,
                default_key_type=default_key_type,
            )

    class EmptyDictKey(enum.Enum):
        """Empty dict key options."""

        ALLOW = "allow"

    class FloatFormats(enum.Enum):
        """Float format options."""

        REPR = enum.member(value=format_float_repr)
        SCIENTIFIC = enum.member(value=format_float_scientific)
        FIXED = enum.member(value=format_float_fixed)

        def __call__(self, value: float, /) -> str:
            """Format a float."""
            return self.value(value=value)

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

    class NumericLiteralSuffixes(enum.Enum):
        """Numeric literal suffix options."""

        NONE = "none"

    class NumericSeparators(enum.Enum):
        """Numeric separator options."""

        NONE = "none"
        UNDERSCORE = "underscore"

    class StringFormats(enum.Enum):
        """String format options."""

        DOUBLE = enum.member(value=format_string_backslash)
        RAW = enum.member(value=format_string_raw_rust)

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

        AUTO = "auto"

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

    def __init__(
        self,
        *,
        date_format: DateFormats = DateFormats.RUST,
        datetime_format: DatetimeFormats = DatetimeFormats.RUST,
        bytes_format: BytesFormats = BytesFormats.HEX,
        sequence_format: SequenceFormats = SequenceFormats.VEC,
        set_format: SetFormats = SetFormats.HASH_SET,
        default_sequence_element_type: str = "String",
        default_set_element_type: str = "String",
        default_dict_key_type: str = "String",
        default_dict_value_type: str = "String",
        variable_type_hints: VariableTypeHints = VariableTypeHints.AUTO,
        comment_format: CommentFormats = CommentFormats.DOUBLE_SLASH,
        declaration_style: DeclarationStyles = DeclarationStyles.LET,
        dict_entry_style: DictEntryStyles = DictEntryStyles.DEFAULT,
        dict_format: DictFormats = DictFormats.HASH_MAP,
        float_format: FloatFormats = FloatFormats.REPR,
        integer_format: IntegerFormats = IntegerFormats.DECIMAL,
        numeric_literal_suffix: NumericLiteralSuffixes = (
            NumericLiteralSuffixes.NONE
        ),
        numeric_separator: NumericSeparators = NumericSeparators.NONE,
        string_format: StringFormats = StringFormats.DOUBLE,
        trailing_comma: TrailingCommas = TrailingCommas.YES,
        line_ending: LineEndings = LineEndings.SEMICOLON,
        indent: str = "    ",
    ) -> None:
        """Initialize Rust language specification."""
        self.variable_type_hints = variable_type_hints
        self.sequence_format = sequence_format
        self.null_literal = "None::<()>"
        self.true_literal = "true"
        self.false_literal = "false"
        fmt = sequence_format(default_type=default_sequence_element_type)
        self.sequence_format_config: SequenceFormatConfig = fmt
        self.set_format = set_format

        self.set_format_config: SetFormatConfig = set_format(
            default_type=default_set_element_type,
        )
        self.sequence_open: Callable[[list[Value]], str] = fmt.sequence_open
        self.dict_format_config: DictFormatConfig = dict_format(
            default_type=default_dict_value_type,
            default_key_type=default_dict_key_type,
        )
        self.trailing_comma_config: TrailingCommaConfig = trailing_comma.value
        self.format_bytes: Callable[[bytes], str] = bytes_format
        self.format_date: Callable[[datetime.date], str] = date_format
        self.format_datetime: Callable[[datetime.datetime], str] = (
            datetime_format
        )

        self.format_string: Callable[[str], str] = string_format
        self.format_float: Callable[[float], str] = float_format
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
                open_str="HashMap::from([",
                close="])",
                preamble_lines=("use std::collections::HashMap;",),
            )
        )
        self.format_ordered_map_entry: Callable[[str, Value, str], str] = (
            tuple_dict_entry(format_value=passthrough_sequence_entry)
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
