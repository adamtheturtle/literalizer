"""C++ language specification."""

import dataclasses
import datetime
import enum
import math
from collections.abc import Callable
from types import MappingProxyType
from typing import TYPE_CHECKING

from beartype import beartype

from literalizer._formatters.collection_openers import (
    fixed_set_open,
    make_element_to_type,
    make_type_to_opener,
    typed_collection_open,
    typed_dict_open,
)
from literalizer._formatters.format_dates import (
    format_date_iso,
    format_datetime_iso,
)
from literalizer._formatters.format_entries import (
    braced_dict_entry,
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
    format_integer_tick,
    make_long_suffix_formatter,
)
from literalizer._formatters.format_strings import format_string_backslash
from literalizer._formatters.type_inference import (
    DictType,
    ListType,
)
from literalizer._language import (
    CallStyleConfig,
    CallStyleKind,
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
from literalizer._types import Value

if TYPE_CHECKING:
    from collections.abc import Sequence


@beartype
def _format_date_cpp(value: datetime.date) -> str:
    """Format a date as a C++ chrono year_month_day literal."""
    return (
        f"std::chrono::year_month_day{{"
        f"std::chrono::year{{{value.year}}}, "
        f"std::chrono::month{{{value.month}}}, "
        f"std::chrono::day{{{value.day}}}}}"
    )


@beartype
def _format_datetime_cpp(value: datetime.datetime) -> str:
    """Format a datetime as a C++ chrono time_point construction."""
    ymd = _format_date_cpp(value=value)
    parts = [f"std::chrono::sys_days{{{ymd}}}"]
    if value.hour:
        parts.append(f"std::chrono::hours{{{value.hour}}}")
    if value.minute:
        parts.append(f"std::chrono::minutes{{{value.minute}}}")
    if value.second:
        parts.append(f"std::chrono::seconds{{{value.second}}}")
    if value.microsecond:
        parts.append(f"std::chrono::microseconds{{{value.microsecond}}}")
    return " + ".join(parts)


@beartype
def _make_cpp_element_to_type(
    *,
    int_type: str,
) -> Callable[[type | ListType | DictType], str | None]:
    """Build the C++ element-to-type resolver."""
    return make_element_to_type(
        str_type="std::string",
        bool_type="bool",
        int_type=int_type,
        float_type="double",
        mixed_numeric_type="double",
        bytes_type="std::string",
        date_type=None,
        datetime_type=None,
        list_template="std::vector<{inner}>",
        dict_type_template="std::map<std::string, {inner}>",
        fallback_value_type="_Any",
    )


@beartype
def _cpp_array_open(items: list[Value]) -> str:
    """Infer element type and return a ``std::array<T, N>`` opener."""
    element_to_type = _make_cpp_element_to_type(int_type="int")
    type_name = element_to_type(type(items[0])) if items else None
    if type_name is None or not all(
        element_to_type(type(i)) == type_name for i in items
    ):
        return "{"
    return f"std::array<{type_name}, {len(items)}>{{"


@beartype
def _make_initializer_list_config(
    *,
    int_type: str,
) -> SequenceFormatConfig:
    """Build an INITIALIZER_LIST sequence config for the given int
    type.
    """
    element_to_type = _make_cpp_element_to_type(int_type=int_type)
    return SequenceFormatConfig(
        sequence_open=typed_collection_open(
            type_to_opener=make_type_to_opener(
                element_to_type=element_to_type,
                opener_template="std::vector<{type_name}>{{",
            ),
            fallback="{",
        ),
        close="}",
        supports_heterogeneity=True,
        single_element_trailing_comma=False,
        supports_trailing_comma=True,
        empty_sequence=None,
        preamble_lines=("#include <vector>",),
        format_entry=passthrough_sequence_entry,
        typed_opener_fallback=None,
        uses_typed_literal_for_scalars=False,
        requires_uniform_record_shapes=False,
        declared_type=None,
    )


_ARRAY_CONFIG = SequenceFormatConfig(
    sequence_open=_cpp_array_open,
    close="}",
    supports_heterogeneity=False,
    single_element_trailing_comma=False,
    supports_trailing_comma=True,
    empty_sequence=None,
    preamble_lines=("#include <array>",),
    format_entry=passthrough_sequence_entry,
    typed_opener_fallback=None,
    uses_typed_literal_for_scalars=False,
    requires_uniform_record_shapes=False,
    declared_type=None,
)


@beartype
def _make_array_config(*, int_type: str) -> SequenceFormatConfig:
    """Return the ARRAY sequence config (ignores int_type)."""
    del int_type
    return _ARRAY_CONFIG


@dataclasses.dataclass(frozen=True)
class _NumericLiteralSuffixConfig:
    """Configuration for a numeric literal suffix option."""

    int_type: str
    formatter_wrapper: Callable[[Callable[[int], str]], Callable[[int], str]]


def _identity_wrapper(
    base: Callable[[int], str],
) -> Callable[[int], str]:
    """Return the formatter unchanged."""
    return base


@beartype
def _rebuild_dict_opener(
    *,
    int_type: str,
    dict_format: enum.Enum,
) -> DictFormatConfig:
    """Rebuild the dict opener for the given int type."""
    element_to_type = _make_cpp_element_to_type(int_type=int_type)
    dict_opener_template = (
        "std::unordered_map<std::string, {type_name}>{{"
        if dict_format.name == "UNORDERED_MAP"
        else "std::map<std::string, {type_name}>{{"
    )
    base_config: DictFormatConfig = dict_format.value
    return dataclasses.replace(
        base_config,
        open_fn=typed_dict_open(
            type_to_opener=make_type_to_opener(
                element_to_type=element_to_type,
                opener_template=dict_opener_template,
            ),
            fallback="{",
        ),
    )


@beartype
def _format_variable_declaration(
    name: str,
    value: str,
    _data: Value,
) -> str:
    """Format a C++ variable declaration."""
    return f"_Any {name} = {value};"


@beartype
class Cpp(metaclass=LanguageCls):
    """C++ language specification.

    Args:
        date_format: How to format :class:`datetime.date` values.

            * ``date_formats.CPP`` — ``std::chrono::year_month_day`` literal,
              e.g. ``std::chrono::year_month_day{std::chrono::year{2024},
              std::chrono::month{1}, std::chrono::day{15}}``.
            * ``date_formats.ISO`` — ISO 8601 quoted string,
              e.g. ``"2024-01-15"``.

        datetime_format: How to format :class:`datetime.datetime` values.

            * ``datetime_formats.CPP`` — ``std::chrono::sys_days`` with
              time-of-day durations,
              e.g. ``std::chrono::sys_days{...} + std::chrono::hours{12}
              + std::chrono::minutes{30}``.
            * ``datetime_formats.ISO`` — ISO 8601 quoted string,
              e.g. ``"2024-01-15T12:30:00"``.
    """

    extension = ".cpp"
    pygments_name = "cpp"
    supports_default_set_element_type = False
    supports_default_sequence_element_type = False
    supports_default_dict_value_type = False
    supports_default_dict_key_type = False
    supports_default_ordered_map_value_type = False
    supports_non_printable_ascii_dict_keys = True

    class DateFormats(enum.Enum):
        """Date format options for C++."""

        CPP = DateFormatConfig(
            formatter=_format_date_cpp,
            preamble_lines=("#include <chrono>",),
        )
        ISO = DateFormatConfig(
            formatter=format_date_iso,
            preamble_lines=("#include <string>",),
            type_produced=str,
        )

        def __call__(self, date_value: datetime.date, /) -> str:
            """Format a date."""
            return self.value.formatter(date_value)

    class DatetimeFormats(enum.Enum):
        """Datetime format options for C++."""

        CPP = DatetimeFormatConfig(
            formatter=_format_datetime_cpp,
            preamble_lines=("#include <chrono>",),
        )
        ISO = DatetimeFormatConfig(
            formatter=format_datetime_iso,
            preamble_lines=("#include <string>",),
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
        """Sequence type options for C++."""

        INITIALIZER_LIST = enum.member(value=_make_initializer_list_config)
        ARRAY = enum.member(value=_make_array_config)

        def get_config(self, *, int_type: str) -> SequenceFormatConfig:
            """Return the sequence format config for the given int
            type.
            """
            factory: Callable[..., SequenceFormatConfig] = self.value
            return factory(int_type=int_type)

        @property
        def supports_heterogeneity(self) -> bool:
            """Whether this sequence format supports mixed-type
            elements.
            """
            return self.get_config(int_type="int").supports_heterogeneity

    class SetFormats(enum.Enum):
        """Set type options for C++."""

        SET = SetFormatConfig(
            set_open=fixed_set_open(open_str="{"),
            close="}",
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
        BLOCK = CommentConfig(
            prefix="/*",
            suffix=" */",
        )

    class DeclarationStyles(enum.Enum):
        """Declaration style options."""

        AUTO = DeclarationStyleConfig(
            formatter=_format_variable_declaration,
            supports_redefinition=True,
        )

    class DictEntryStyles(enum.Enum):
        """Dict entry style options."""

        DEFAULT = enum.auto()

    class DictFormats(enum.Enum):
        """Dict/map format options."""

        MAP = DictFormatConfig(
            open_fn=typed_dict_open(
                type_to_opener=make_type_to_opener(
                    element_to_type=_make_cpp_element_to_type(int_type="int"),
                    opener_template="std::map<std::string, {type_name}>{{",
                ),
                fallback="{",
            ),
            close="}",
            format_entry=braced_dict_entry(
                format_value=passthrough_sequence_entry
            ),
            empty_dict=None,
            preamble_lines=("#include <map>",),
            narrowed_open=None,
        )
        UNORDERED_MAP = DictFormatConfig(
            open_fn=typed_dict_open(
                type_to_opener=make_type_to_opener(
                    element_to_type=_make_cpp_element_to_type(int_type="int"),
                    opener_template=(
                        "std::unordered_map<std::string, {type_name}>{{"
                    ),
                ),
                fallback="{",
            ),
            close="}",
            format_entry=braced_dict_entry(
                format_value=passthrough_sequence_entry
            ),
            empty_dict=None,
            preamble_lines=("#include <unordered_map>",),
            narrowed_open=None,
        )

    class EmptyDictKey(enum.Enum):
        """Empty dict key options."""

        ALLOW = enum.auto()

    class FloatFormats(enum.Enum):
        """Float format options."""

        REPR = enum.member(value=format_float_repr)
        SCIENTIFIC = enum.member(value=format_float_scientific)
        FIXED = enum.member(value=format_float_fixed)

        def __call__(self, value: float, /) -> str:
            """Format a float."""
            if math.isinf(value):
                return "-INFINITY" if value < 0 else "INFINITY"
            if math.isnan(value):
                return "NAN"
            return self.value(value=value)

    class IntegerFormats(enum.Enum):
        """Integer format options."""

        DECIMAL = MappingProxyType(
            mapping={
                "NONE": str,
                "UNDERSCORE": format_integer_tick,
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

        NONE = _NumericLiteralSuffixConfig(
            int_type="int",
            formatter_wrapper=_identity_wrapper,
        )
        AUTO = _NumericLiteralSuffixConfig(
            int_type="long",
            formatter_wrapper=make_long_suffix_formatter,
        )

        @property
        def int_type(self) -> str:
            """Return the C++ integer type for this suffix."""
            config: _NumericLiteralSuffixConfig = self.value
            return config.int_type

        def wrap_integer_formatter(
            self,
            base: Callable[[int], str],
        ) -> Callable[[int], str]:
            """Wrap the base integer formatter."""
            config: _NumericLiteralSuffixConfig = self.value
            return config.formatter_wrapper(base)

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
        date_format: DateFormats = DateFormats.CPP,
        datetime_format: DatetimeFormats = DatetimeFormats.CPP,
        bytes_format: BytesFormats = BytesFormats.HEX,
        sequence_format: SequenceFormats = SequenceFormats.INITIALIZER_LIST,
        set_format: SetFormats = SetFormats.SET,
        variable_type_hints: VariableTypeHints = VariableTypeHints.AUTO,
        comment_format: CommentFormats = CommentFormats.DOUBLE_SLASH,
        declaration_style: DeclarationStyles = DeclarationStyles.AUTO,
        dict_entry_style: DictEntryStyles = DictEntryStyles.DEFAULT,
        dict_format: DictFormats = DictFormats.MAP,
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
        """Initialize Cpp language specification."""
        self.variable_type_hints = variable_type_hints
        self.sequence_format = sequence_format
        self.null_literal = "nullptr"
        self.true_literal = "true"
        self.false_literal = "false"
        self.sequence_format_config: SequenceFormatConfig = (
            sequence_format.get_config(
                int_type=numeric_literal_suffix.int_type,
            )
        )
        self.set_format = set_format
        self.set_format_config: SetFormatConfig = set_format.value
        self.sequence_open: Callable[[list[Value]], str] = (
            self.sequence_format_config.sequence_open
        )
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
            numeric_literal_suffix.wrap_integer_formatter(
                base=base_int_formatter,
            )
        )
        self.dict_format_config: DictFormatConfig = _rebuild_dict_opener(
            int_type=numeric_literal_suffix.int_type,
            dict_format=dict_format,
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
                open_str="{",
                close="}",
                preamble_lines=(),
            )
        )
        self.format_ordered_map_entry: Callable[[str, Value, str], str] = (
            braced_dict_entry(format_value=passthrough_sequence_entry)
        )
        self.indent = indent
        self.indent_closing_delimiter = False
        self.element_separator = ", "
        self.skip_null_dict_values = False
        self.supports_collection_comments = True
        self.supports_scalar_before_comments = True
        self.supports_scalar_inline_comments = False
        self.static_preamble: Sequence[str] = ("#include <initializer_list>",)
        self.static_body_preamble: Sequence[str] = (
            "struct _Any {",
            "    template<class T> _Any(T&&) noexcept {}",
            "    _Any(std::initializer_list<_Any>) noexcept {}",
            "};",
        )
        self.format_variable_declaration: Callable[[str, str, Value], str] = (
            declaration_style.value.formatter
        )
        self.format_variable_assignment: Callable[[str, str, Value], str] = (
            variable_formatter(template="{name} = {value};")
        )
        self.scalar_preamble: dict[type, tuple[str, ...]] = (
            date_scalar_preamble(
                date_format=date_format,
                datetime_format=datetime_format,
                extra={
                    str: ("#include <string>",),
                    bytes: ("#include <string>",),
                    type(None): ("#include <cstddef>",),
                },
            )
        )
        self.scalar_body_preamble: dict[type, tuple[str, ...]] = {}
        self.compute_body_preamble: Callable[
            [frozenset[type], Value], tuple[str, ...]
        ] = body_preamble_from_scalars(
            scalar_body_preamble=self.scalar_body_preamble,
        )

        self.type_hint_collection_preamble_lines = no_type_hint_preamble
        self.special_float_preamble: tuple[str, ...] = ("#include <cmath>",)
        self.call_style_config: CallStyleConfig = CallStyleConfig(
            kind=CallStyleKind.POSITIONAL,
        )
