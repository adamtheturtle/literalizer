"""Zig language specification."""

import datetime
import enum
import functools
from collections.abc import Callable
from types import MappingProxyType
from typing import TYPE_CHECKING

from beartype import beartype

from literalizer._formatters.collection_openers import (
    fixed_dict_open,
    fixed_sequence_open,
    fixed_set_open,
)
from literalizer._formatters.format_dates import (
    format_date_iso,
    format_datetime_iso,
)
from literalizer._formatters.format_entries import (
    dict_entry_with_template,
    format_bytes_base64,
    format_bytes_hex,
    passthrough_sequence_entry,
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
    format_string_backslash_control,
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
    no_type_hint_preamble,
)
from literalizer._types import Value

if TYPE_CHECKING:
    from collections.abc import Sequence


@beartype
def _format_date_zig(value: datetime.date) -> str:
    """Format a date as epoch seconds (midnight UTC)."""
    dt = datetime.datetime(
        year=value.year,
        month=value.month,
        day=value.day,
        tzinfo=datetime.UTC,
    )
    return str(object=int(dt.timestamp()))


@beartype
def _format_datetime_zig(value: datetime.datetime) -> str:
    """Format a datetime as epoch seconds (UTC)."""
    if value.tzinfo is None:
        value = value.replace(tzinfo=datetime.UTC)
    return str(object=int(value.timestamp()))


@beartype
def _format_zig_entry(original: Value, formatted: str) -> str:
    """Wrap a formatted entry in the appropriate Zig ``ZVal`` union
    tag.
    """
    match original:
        case bool():
            return formatted
        case int():
            return f".{{ .int = {formatted} }}"
        case float():
            return f".{{ .float = {formatted} }}"
        case str() | bytes():
            return f".{{ .str = {formatted} }}"
        case datetime.date():
            tag = "str" if formatted.startswith('"') else "int"
            return f".{{ .{tag} = {formatted} }}"
        case _:
            return formatted


@beartype
def _format_const_declaration(name: str, value: str, data: Value) -> str:
    """Format a Zig ``const`` declaration with explicit ``ZVal`` type."""
    wrapped = _format_zig_entry(original=data, formatted=value)
    return f"const {name}: ZVal = {wrapped};"


@beartype
def _format_var_declaration(name: str, value: str, data: Value) -> str:
    """Format a Zig ``var`` declaration with explicit ``ZVal`` type."""
    wrapped = _format_zig_entry(original=data, formatted=value)
    return f"var {name}: ZVal = {wrapped};"


@beartype
def _format_variable_assignment(name: str, value: str, data: Value) -> str:
    """Format a Zig assignment to an existing ``ZVal`` variable."""
    wrapped = _format_zig_entry(original=data, formatted=value)
    return f"{name} = {wrapped};"


@beartype
class Zig(metaclass=LanguageCls):
    """Zig language specification."""

    extension = ".zig"
    pygments_name = "zig"
    supports_default_set_element_type = False
    supports_default_sequence_element_type = False
    supports_default_dict_value_type = False
    supports_default_dict_key_type = False
    supports_default_ordered_map_value_type = False
    supports_non_printable_ascii_dict_keys = True

    class DateFormats(enum.Enum):
        """Date format options for Zig."""

        ZIG = DateFormatConfig(formatter=_format_date_zig)
        ISO = DateFormatConfig(formatter=format_date_iso, type_produced=str)

        def __call__(self, date_value: datetime.date, /) -> str:
            """Format a date."""
            return self.value.formatter(date_value)

    class DatetimeFormats(enum.Enum):
        """Datetime format options for Zig."""

        ZIG = DatetimeFormatConfig(formatter=_format_datetime_zig)
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
        """Sequence type options for Zig."""

        ARRAY = SequenceFormatConfig(
            sequence_open=fixed_sequence_open(open_str=".{ .arr = &.{"),
            close="}}",
            supports_heterogeneity=True,
            single_element_trailing_comma=False,
            supports_trailing_comma=True,
            empty_sequence=None,
            preamble_lines=(),
            format_entry=passthrough_sequence_entry,
            typed_opener_fallback=None,
            uses_typed_literal_for_scalars=False,
            requires_uniform_record_shapes=False,
        )

        @property
        def supports_heterogeneity(self) -> bool:
            """Whether this sequence format supports mixed-type
            elements.
            """
            return self.value.supports_heterogeneity

    class SetFormats(enum.Enum):
        """Set type options for Zig."""

        SET = SetFormatConfig(
            set_open=fixed_set_open(open_str=".{ .set = &.{"),
            close="}}",
            empty_set=None,
            preamble_lines=(),
            set_opener_template="",
            coerce_mixed_to_str=False,
        )

    class CommentFormats(enum.Enum):
        """Comment style options."""

        DOUBLE_SLASH = CommentConfig(
            prefix="//",
            suffix="",
        )

    class DeclarationStyles(enum.Enum):
        """Declaration style options."""

        CONST = DeclarationStyleConfig(
            formatter=_format_const_declaration,
            supports_redefinition=False,
        )
        VAR = DeclarationStyleConfig(
            formatter=_format_var_declaration,
            supports_redefinition=True,
        )

    class DictEntryStyles(enum.Enum):
        """Dict entry style options."""

        DEFAULT = enum.auto()

    class DictFormats(enum.Enum):
        """Dict/map format options."""

        DEFAULT = enum.auto()

    class EmptyDictKey(enum.Enum):
        """Empty dict key options."""

        ALLOW = enum.auto()

    class FloatFormats(enum.Enum):
        """Float format options."""

        REPR = enum.member(
            value=functools.partial(
                format_float_repr,
                inf_literal="std.math.inf(f64)",
                neg_inf_literal="-std.math.inf(f64)",
                nan_literal="std.math.nan(f64)",
            )
        )
        SCIENTIFIC = enum.member(
            value=functools.partial(
                format_float_scientific,
                inf_literal="std.math.inf(f64)",
                neg_inf_literal="-std.math.inf(f64)",
                nan_literal="std.math.nan(f64)",
            )
        )
        FIXED = enum.member(
            value=functools.partial(
                format_float_fixed,
                inf_literal="std.math.inf(f64)",
                neg_inf_literal="-std.math.inf(f64)",
                nan_literal="std.math.nan(f64)",
            )
        )

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

        NONE = enum.auto()

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
        date_format: DateFormats = DateFormats.ZIG,
        datetime_format: DatetimeFormats = DatetimeFormats.ZIG,
        bytes_format: BytesFormats = BytesFormats.HEX,
        sequence_format: SequenceFormats = SequenceFormats.ARRAY,
        set_format: SetFormats = SetFormats.SET,
        variable_type_hints: VariableTypeHints = VariableTypeHints.AUTO,
        comment_format: CommentFormats = CommentFormats.DOUBLE_SLASH,
        declaration_style: DeclarationStyles = DeclarationStyles.CONST,
        dict_entry_style: DictEntryStyles = DictEntryStyles.DEFAULT,
        dict_format: DictFormats = DictFormats.DEFAULT,
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
        """Initialize Zig language specification."""
        self.variable_type_hints = variable_type_hints
        self.sequence_format = sequence_format
        self.null_literal = ".nil"
        self.true_literal = ".{ .bool = true }"
        self.false_literal = ".{ .bool = false }"
        fmt = sequence_format.value
        self.sequence_format_config: SequenceFormatConfig = fmt
        self.set_format = set_format
        self.set_format_config: SetFormatConfig = set_format.value
        self.sequence_open: Callable[[list[Value]], str] = fmt.sequence_open
        self.dict_format_config: DictFormatConfig = DictFormatConfig(
            open_fn=fixed_dict_open(open_str=".{ .map = &.{"),
            close="}}",
            format_entry=dict_entry_with_template(
                template=".{{ .key = {key}, .val = {value} }}",
                format_value=_format_zig_entry,
            ),
            empty_dict=None,
            preamble_lines=(),
            narrowed_open=None,
        )
        self.trailing_comma_config: TrailingCommaConfig = trailing_comma.value
        self.format_bytes: Callable[[bytes], str] = bytes_format
        self.format_date: Callable[[datetime.date], str] = date_format
        self.format_datetime: Callable[[datetime.datetime], str] = (
            datetime_format
        )
        self.format_string: Callable[[str], str] = functools.partial(
            format_string_backslash_control,
            control_char_fmt="\\x{:02x}",
        )
        self.format_float: Callable[[float], str] = float_format
        self.format_integer: Callable[[int], str] = (
            integer_format.get_formatter(
                numeric_separator=numeric_separator,
            )
        )
        self.format_sequence_entry: Callable[[Value, str], str] = (
            _format_zig_entry
        )
        self.format_set_entry: Callable[[Value, str], str] = _format_zig_entry
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
                open_str=".{ .map = &.{",
                close="}}",
                preamble_lines=(),
            )
        )
        self.format_ordered_map_entry: Callable[[str, Value, str], str] = (
            dict_entry_with_template(
                template=".{{ .key = {key}, .val = {value} }}",
                format_value=_format_zig_entry,
            )
        )
        self.indent = indent
        self.indent_closing_delimiter = False
        self.element_separator = ", "
        self.skip_null_dict_values = False
        self.supports_collection_comments = True
        self.supports_scalar_before_comments = True
        self.supports_scalar_inline_comments = False
        self.format_variable_declaration: Callable[[str, str, Value], str] = (
            declaration_style.value.formatter
        )
        self.format_variable_assignment: Callable[[str, str, Value], str] = (
            _format_variable_assignment
        )
        self.static_preamble: Sequence[str] = (
            "const ZVal = union(enum) {",
            "    nil,",
            "    bool: bool,",
            "    int: i64,",
            "    float: f64,",
            "    str: []const u8,",
            "    arr: []const ZVal,",
            "    map: []const ZKV,",
            "    set: []const ZVal,",
            "};",
            "const ZKV = struct { key: []const u8, val: ZVal };",
        )
        self.static_body_preamble: Sequence[str] = ()
        self.scalar_preamble: dict[type, tuple[str, ...]] = {}
        self.scalar_body_preamble: dict[type, tuple[str, ...]] = {}
        self.compute_body_preamble: Callable[
            [frozenset[type], Value], tuple[str, ...]
        ] = body_preamble_from_scalars(
            scalar_body_preamble=self.scalar_body_preamble,
        )

        self.type_hint_collection_preamble_lines = no_type_hint_preamble
        self.special_float_preamble: tuple[str, ...] = (
            'const std = @import("std");',
        )
