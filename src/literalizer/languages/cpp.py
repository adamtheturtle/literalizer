"""C++ language specification."""

import datetime
import enum
from typing import TYPE_CHECKING

from beartype import beartype

from literalizer._formatters import (
    MixedNumeric,
    _infer_element_type,
    fixed_set_open,
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
)
from literalizer._types import Value

if TYPE_CHECKING:
    from collections.abc import Callable, Sequence


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


_CPP_SCALAR_TYPES: dict[type, str] = {
    str: "std::string",
    bool: "bool",
    int: "int",
    float: "double",
    MixedNumeric: "double",
    bytes: "std::string",
}

_cpp_element_to_type = make_element_to_type(
    scalar_types=_CPP_SCALAR_TYPES,
    list_template="std::vector<{inner}>",
)

_cpp_type_to_opener = make_type_to_opener(
    element_to_type=_cpp_element_to_type,
    opener_template="std::vector<{type_name}>{{",
)

_cpp_dict_type_to_opener = make_type_to_opener(
    element_to_type=_cpp_element_to_type,
    opener_template="std::map<std::string, {type_name}>{{",
)


@beartype
def _cpp_array_open(items: list[Value]) -> str:
    """Infer element type and return a ``std::array<T, N>`` opener."""
    type_name = _cpp_element_to_type(type(items[0])) if items else None
    if type_name is None or not all(
        _cpp_element_to_type(type(i)) == type_name for i in items
    ):
        return "{"
    return f"std::array<{type_name}, {len(items)}>{{"


@beartype
def _format_cpp_dict_entry(key: str, value: str) -> str:
    """Format a C++ dict entry as a brace-enclosed pair."""
    return f"{{{key}, {value}}}"


_ANY_PREAMBLE: tuple[str, ...] = (
    "#include <initializer_list>",
    "struct _Any {",
    "    template<class T> _Any(T&&) noexcept {}",
    "    _Any(std::initializer_list<_Any>) noexcept {}",
    "};",
)


@beartype
def _is_heterogeneous(data: Value) -> bool:
    """Check whether *data* is a collection with mixed element types.

    Returns ``True`` when the top-level structure is a list, dict,
    set, or frozenset whose elements cannot be unified into a single
    C++ type, making ``auto`` deduction impossible.
    """
    if isinstance(data, list) and data:
        return _infer_element_type(items=data) is None
    if isinstance(data, dict) and data:
        return _infer_element_type(items=list(data.values())) is None
    if isinstance(data, (set, frozenset)) and data:
        return _infer_element_type(items=list(data)) is None
    return False


@beartype
def _format_variable_assignment(name: str, value: str, _data: Value) -> str:
    """Format a C++ variable assignment."""
    return f"{name} = {value};"


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

        def __call__(self, data: bytes, /) -> str:
            """Format bytes."""
            return self.value(value=data)

    class SequenceFormats(enum.Enum):
        """Sequence type options for C++."""

        INITIALIZER_LIST = SequenceFormatConfig(
            sequence_open=typed_sequence_open(
                type_to_opener=_cpp_type_to_opener,
                fallback="{",
            ),
            close="}",
            supports_heterogeneity=True,
            single_element_trailing_comma=False,
            empty_sequence=None,
            preamble_lines=("#include <vector>",),
            format_entry=passthrough_sequence_entry,
        )
        ARRAY = SequenceFormatConfig(
            sequence_open=_cpp_array_open,
            close="}",
            supports_heterogeneity=False,
            single_element_trailing_comma=False,
            empty_sequence=None,
            preamble_lines=("#include <array>",),
            format_entry=passthrough_sequence_entry,
        )

        @property
        def supports_heterogeneity(self) -> bool:
            """Whether this sequence format supports mixed-type
            elements.
            """
            return self.value.supports_heterogeneity

    class SetFormats(enum.Enum):
        """Set type options for C++."""

        SET = SetFormatConfig(
            set_open=fixed_set_open(open_str="{"),
            close="}",
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

        AUTO = "auto"

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
        date_format: DateFormats = DateFormats.CPP,
        datetime_format: DatetimeFormats = DatetimeFormats.CPP,
        bytes_format: BytesFormats = BytesFormats.HEX,
        sequence_format: SequenceFormats = SequenceFormats.INITIALIZER_LIST,
        set_format: SetFormats = SetFormats.SET,
        variable_type_hints: VariableTypeHints = VariableTypeHints.NONE,
        comment_format: CommentFormats = CommentFormats.DOUBLE_SLASH,
        _variable_type_hints: VariableTypeHints = VariableTypeHints.NONE,
        declaration_style: DeclarationStyles = DeclarationStyles.AUTO,
        dict_format: DictFormats = DictFormats.MAP,
        integer_format: IntegerFormats = IntegerFormats.DECIMAL,
        numeric_separator: NumericSeparators = NumericSeparators.NONE,
        string_format: StringFormats = StringFormats.DOUBLE,
        trailing_comma: TrailingCommas = TrailingCommas.YES,
    ) -> None:
        """Initialize Cpp language specification."""
        self.variable_type_hints = variable_type_hints
        self.sequence_format = sequence_format
        self.null_literal = "nullptr"
        self.true_literal = "true"
        self.false_literal = "false"
        fmt = sequence_format.value
        self.sequence_format_config: SequenceFormatConfig = fmt
        self.set_format = set_format
        self.set_format_config: SetFormatConfig = set_format.value
        self.sequence_open: Callable[[list[Value]], str] = fmt.sequence_open
        self.dict_format_config: DictFormatConfig = DictFormatConfig(
            open_fn=typed_dict_open(
                type_to_opener=_cpp_dict_type_to_opener,
                fallback="{",
            ),
            close="}",
            format_entry=_format_cpp_dict_entry,
            empty_dict=None,
            preamble_lines=("#include <map>",),
        )
        self.multiline_trailing_comma = True
        self.format_bytes: Callable[[bytes], str] = bytes_format
        self.format_date: Callable[[datetime.date], str] = date_format
        self.format_datetime: Callable[[datetime.datetime], str] = (
            datetime_format
        )

        self.format_string: Callable[[str], str] = format_string_backslash
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
                open_str="{",
                close="}",
                preamble_lines=(),
            )
        )
        self.format_ordered_map_entry: Callable[[str, str], str] = (
            _format_cpp_dict_entry
        )
        self.multiline_close_indent = ""
        self.element_separator = ", "
        self.skip_null_dict_values = False
        self.supports_collection_comments = True
        self.static_preamble: Sequence[str] = ()

        def _format_var_decl(
            name: str,
            value: str,
            _data: Value,
        ) -> str:
            """Format a C++ variable declaration."""
            if _is_heterogeneous(data=_data):
                self.static_preamble = (
                    tuple(self.static_preamble) + _ANY_PREAMBLE
                )
                return f"_Any {name} = {value};"
            return f"auto {name} = {value};"

        self.format_variable_declaration: Callable[[str, str, Value], str] = (
            _format_var_decl
        )
        self.format_variable_assignment: Callable[[str, str, Value], str] = (
            _format_variable_assignment
        )
        self.scalar_preamble: dict[type, tuple[str, ...]] = {
            str: ("#include <string>",),
            bytes: ("#include <string>",),
            type(None): ("#include <cstddef>",),
            **{
                t: p
                for t, p in (
                    (datetime.date, date_format.value.preamble_lines),
                    (datetime.datetime, datetime_format.value.preamble_lines),
                )
                if p
            },
        }
        self.scalar_body_preamble: dict[type, tuple[str, ...]] = {}
        self.type_hint_collection_preamble_lines: tuple[str, ...] = ()
