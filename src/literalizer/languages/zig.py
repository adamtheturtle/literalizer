"""Zig language specification."""

import dataclasses
import datetime
import enum
import functools
import textwrap
from collections.abc import Callable, Sequence
from functools import cached_property
from types import MappingProxyType
from typing import ClassVar

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
    CallStyleConfig,
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
    identity_call_target,
    no_call_stub,
    no_data_preamble,
    no_type_hint_preamble,
    prepend_body_preamble,
)
from literalizer._types import Value


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
@dataclasses.dataclass(frozen=True, kw_only=True)
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
    supports_variable_names = True
    supports_dotted_calls = True

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
            declared_type=None,
        )

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

    class FloatFormats(
        FloatSpecialsMixin,
        enum.Enum,
        positive_infinity="std.math.inf(f64)",
        negative_infinity="-std.math.inf(f64)",
        nan="std.math.nan(f64)",
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

    class NumericStyles(enum.Enum):
        """Numeric literal style options."""

        OVERLOADED = enum.auto()

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
    numeric_styles = NumericStyles
    string_formats = StringFormats
    trailing_commas = TrailingCommas

    class LineEndings(enum.Enum):
        """Line ending options."""

        SEMICOLON = "semicolon"

    line_endings = LineEndings

    class CallStyles(enum.Enum):
        """Zig call style options."""

    call_styles = CallStyles

    @staticmethod
    def wrap_in_file(
        content: str,
        variable_name: str,
        body_preamble: tuple[str, ...],
    ) -> str:
        """Wrap a Zig declaration in a main function."""
        content = prepend_body_preamble(
            content=content,
            body_preamble=body_preamble,
        )
        indented = textwrap.indent(text=content, prefix="    ")
        if "var " in content:
            use = f"    {variable_name} = .nil;"
        else:
            use = f"    _ = {variable_name};"
        return f"pub fn main() void {{\n{indented}\n{use}\n}}"

    @staticmethod
    def wrap_combined_in_file(
        declaration: str,
        assignment: str,
        variable_name: str,
        body_preamble: tuple[str, ...],
    ) -> str:
        """Wrap Zig declaration + assignment in a main function."""
        return Zig.wrap_in_file(
            content=declaration + "\n" + assignment,
            variable_name=variable_name,
            body_preamble=body_preamble,
        )

    date_format: DateFormats = DateFormats.ZIG
    datetime_format: DatetimeFormats = DatetimeFormats.ZIG
    bytes_format: BytesFormats = BytesFormats.HEX
    sequence_format: SequenceFormats = SequenceFormats.ARRAY
    set_format: SetFormats = SetFormats.SET
    variable_type_hints: VariableTypeHints = VariableTypeHints.AUTO
    comment_format: CommentFormats = CommentFormats.DOUBLE_SLASH
    declaration_style: DeclarationStyles = DeclarationStyles.CONST
    dict_entry_style: DictEntryStyles = DictEntryStyles.DEFAULT
    dict_format: DictFormats = DictFormats.DEFAULT
    float_format: FloatFormats = FloatFormats.REPR
    integer_format: IntegerFormats = IntegerFormats.DECIMAL
    numeric_literal_suffix: NumericLiteralSuffixes = (
        NumericLiteralSuffixes.NONE
    )
    numeric_separator: NumericSeparators = NumericSeparators.NONE
    numeric_style: NumericStyles = NumericStyles.OVERLOADED
    string_format: StringFormats = StringFormats.DOUBLE
    trailing_comma: TrailingCommas = TrailingCommas.YES
    line_ending: LineEndings = LineEndings.SEMICOLON
    indent: str = "    "

    null_literal: ClassVar[str] = ".nil"
    true_literal: ClassVar[str] = ".{ .bool = true }"
    false_literal: ClassVar[str] = ".{ .bool = false }"
    indent_closing_delimiter: ClassVar[bool] = False
    element_separator: ClassVar[str] = ", "
    skip_null_dict_values: ClassVar[bool] = False
    supports_collection_comments: ClassVar[bool] = True
    supports_scalar_before_comments: ClassVar[bool] = True
    supports_scalar_inline_comments: ClassVar[bool] = False
    statement_terminator: ClassVar[str] = ";"
    static_preamble: ClassVar[Sequence[str]] = (
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
    static_body_preamble: ClassVar[Sequence[str]] = ()
    special_float_preamble: ClassVar[tuple[str, ...]] = (
        'const std = @import("std");',
    )
    call_style_config: ClassVar[CallStyleConfig | None] = None
    format_sequence_entry = staticmethod(_format_zig_entry)
    format_set_entry = staticmethod(_format_zig_entry)
    format_variable_assignment = staticmethod(_format_variable_assignment)
    data_dependent_preamble = staticmethod(no_data_preamble)
    type_hint_collection_preamble_lines = staticmethod(no_type_hint_preamble)
    format_call_stub = staticmethod(no_call_stub)
    format_call_preamble_stub = staticmethod(no_call_stub)
    format_call_target = staticmethod(identity_call_target)

    @cached_property
    def sequence_format_config(self) -> SequenceFormatConfig:
        """Configuration for the chosen sequence format."""
        return self.sequence_format.value

    @cached_property
    def set_format_config(self) -> SetFormatConfig:
        """Configuration for the chosen set format."""
        return self.set_format.value

    @cached_property
    def sequence_open(self) -> Callable[[list[Value]], str]:
        """Callable that returns the opening delimiter for a sequence."""
        return self.sequence_format.value.sequence_open

    @cached_property
    def dict_format_config(self) -> DictFormatConfig:
        """Configuration for dict formatting."""
        return DictFormatConfig(
            dict_open=fixed_dict_open(open_str=".{ .map = &.{"),
            close="}}",
            format_entry=dict_entry_with_template(
                template=".{{ .key = {key}, .val = {value} }}",
                format_value=_format_zig_entry,
            ),
            empty_dict=None,
            preamble_lines=(),
            narrowed_open=None,
        )

    @cached_property
    def trailing_comma_config(self) -> TrailingCommaConfig:
        """Configuration for trailing-comma behavior."""
        return self.trailing_comma.value

    @cached_property
    def format_bytes(self) -> Callable[[bytes], str]:
        """Callable that formats a bytes value as a string literal."""
        return self.bytes_format

    @cached_property
    def format_date(self) -> Callable[[datetime.date], str]:
        """Callable that formats a date as a string literal."""
        return self.date_format

    @cached_property
    def format_datetime(self) -> Callable[[datetime.datetime], str]:
        """Callable that formats a datetime as a string literal."""
        return self.datetime_format

    @cached_property
    def format_string(self) -> Callable[[str], str]:
        """Callable that formats a string value as a quoted literal."""
        return functools.partial(
            format_string_backslash_control,
            control_char_fmt="\\x{:02x}",
        )

    @cached_property
    def format_float(self) -> Callable[[float], str]:
        """Callable that formats a float value as a literal."""
        return self.float_format

    @cached_property
    def format_integer(self) -> Callable[[int], str]:
        """Callable that formats an int value as a literal."""
        return self.integer_format.get_formatter(
            numeric_separator=self.numeric_separator,
        )

    @cached_property
    def comment_config(self) -> CommentConfig:
        """Configuration for the language's comment syntax."""
        return self.comment_format.value

    @cached_property
    def ordered_map_format_config(self) -> OrderedMapFormatConfig:
        """Configuration for ordered-map formatting."""
        return OrderedMapFormatConfig(
            ordered_map_open=fixed_dict_open(open_str=".{ .map = &.{"),
            close="}}",
            preamble_lines=(),
        )

    @cached_property
    def format_ordered_map_entry(self) -> Callable[[str, Value, str], str]:
        """Callable that formats one ordered-map entry."""
        return dict_entry_with_template(
            template=".{{ .key = {key}, .val = {value} }}",
            format_value=_format_zig_entry,
        )

    @cached_property
    def format_variable_declaration(
        self,
    ) -> Callable[[str, str, Value], str]:
        """Callable that formats a new variable declaration."""
        return self.declaration_style.value.formatter

    @cached_property
    def scalar_preamble(self) -> dict[type, tuple[str, ...]]:
        """Per-instance scalar preamble (Zig needs none)."""
        return {}

    @cached_property
    def scalar_body_preamble(self) -> dict[type, tuple[str, ...]]:
        """Per-instance scalar body preamble (Zig needs none)."""
        return {}

    @cached_property
    def compute_body_preamble(
        self,
    ) -> Callable[[frozenset[type], Value], tuple[str, ...]]:
        """Compute body-preamble lines from the scalar map."""
        return body_preamble_from_scalars(
            scalar_body_preamble=self.scalar_body_preamble,
            format_lines=tuple,
        )
