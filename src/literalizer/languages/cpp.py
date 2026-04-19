"""C++ language specification."""

import dataclasses
import datetime
import enum
from collections.abc import Callable, Sequence
from types import MappingProxyType
from typing import assert_never

from beartype import beartype
from ruamel.yaml.compat import ordereddict

from literalizer._formatters.collection_openers import (
    make_element_to_type,
    make_type_to_opener,
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
    infer_element_type,
)
from literalizer._language import (
    CallStyle,
    CommentConfig,
    DateFormatConfig,
    DatetimeFormatConfig,
    DeclarationStyleConfig,
    DictFormatConfig,
    FloatSpecialsMixin,
    LanguageCls,
    OrderedMapFormatConfig,
    PositionalCallStyle,
    SequenceFormatConfig,
    SetFormatConfig,
    StubReturn,
    TrailingCommaConfig,
    body_preamble_from_scalars,
    date_scalar_preamble,
    no_call_stub,
    no_type_hint_preamble,
    prepend_body_preamble,
)
from literalizer._types import Value, ValueKind


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
    date_type: str | None,
    datetime_type: str | None,
) -> Callable[[type | ListType | DictType], str | None]:
    """Build the C++ element-to-type resolver."""
    return make_element_to_type(
        str_type="std::string",
        bool_type="bool",
        int_type=int_type,
        float_type="double",
        mixed_numeric_type="double",
        bytes_type="std::string",
        date_type=date_type,
        datetime_type=datetime_type,
        list_template="std::vector<{inner}>",
        dict_type_template="std::map<std::string, {inner}>",
        fallback_value_type=None,
    )


@beartype
def _cpp_array_open(items: list[Value]) -> str:
    """Infer element type and return a ``std::array<T, N>`` opener."""
    element_to_type = _make_cpp_element_to_type(
        int_type="int",
        date_type=None,
        datetime_type=None,
    )
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
    date_type: str | None,
    datetime_type: str | None,
) -> SequenceFormatConfig:
    """Build an INITIALIZER_LIST sequence config for the given int
    type.
    """
    return SequenceFormatConfig(
        sequence_open=_build_variant_sequence_open(
            int_type=int_type,
            date_type=date_type,
            datetime_type=datetime_type,
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


@beartype
def _make_array_config(
    *,
    int_type: str,
    date_type: str | None,
    datetime_type: str | None,
) -> SequenceFormatConfig:
    """Return the ARRAY sequence config."""
    del int_type, date_type, datetime_type
    return SequenceFormatConfig(
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


@dataclasses.dataclass(frozen=True)
class _DictFormatOption:
    """A dict format bundled with its typed opener template."""

    config: DictFormatConfig
    opener_template: str


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
def _compute_cpp_type(
    item: Value,
    element_to_type: Callable[[type | ListType | DictType], str | None],
) -> str:
    """Return the C++ type string for a single value."""
    match item:
        case ordereddict():
            omap_values = item.values()  # pyright: ignore[reportUnknownMemberType,reportUnknownVariableType]
            values: list[Value] = list(omap_values)  # pyright: ignore[reportUnknownArgumentType]
            value_type = _compute_element_type_for_items(
                items=values,
                element_to_type=element_to_type,
            )
            return f"std::vector<std::pair<std::string, {value_type}>>"
        case dict():
            values = list(item.values())
            value_type = _compute_element_type_for_items(
                items=values,
                element_to_type=element_to_type,
            )
            return f"std::map<std::string, {value_type}>"
        case list():
            inner_type = _compute_element_type_for_items(
                items=item,
                element_to_type=element_to_type,
            )
            return f"std::vector<{inner_type}>"
        case set():
            sorted_items: list[Value] = sorted(
                item,
                key=lambda v: (type(v).__name__, repr(v)),
            )
            inner_type = _compute_element_type_for_items(
                items=sorted_items,
                element_to_type=element_to_type,
            )
            return f"std::initializer_list<{inner_type}>"
        case _:
            cpp_type = element_to_type(type(item))
            if cpp_type is not None:
                return cpp_type
            return "std::nullptr_t"


@beartype
def _collect_unique_cpp_types(
    items: list[Value],
    element_to_type: Callable[[type | ListType | DictType], str | None],
) -> list[str]:
    """Collect unique C++ type names for each item, preserving order."""
    unique_cpp_types: list[str] = []
    seen: set[str] = set()
    for item in items:
        item_type = _compute_cpp_type(
            item=item,
            element_to_type=element_to_type,
        )
        if item_type not in seen:
            seen.add(item_type)
            unique_cpp_types.append(item_type)
    return unique_cpp_types


@beartype
def _compute_element_type_for_items(
    items: list[Value],
    element_to_type: Callable[[type | ListType | DictType], str | None],
) -> str:
    """Return the C++ element type for a collection of items.

    Returns a single type name when all items have the same C++ type,
    or ``std::variant<T1, T2, ...>`` for mixed types.  Returns
    ``std::nullptr_t`` for empty collections.
    """
    if not items:
        return "std::nullptr_t"
    element_type = infer_element_type(items=items)
    if element_type is not None:
        match element_type:
            case DictType(value_type=None):
                all_dict_values: list[Value] = [
                    v
                    for item in items
                    if isinstance(item, dict)  # pragma: no branch
                    for v in item.values()
                ]
                value_type = _compute_element_type_for_items(
                    items=all_dict_values,
                    element_to_type=element_to_type,
                )
                return f"std::map<std::string, {value_type}>"
            case _:
                cpp_type = element_to_type(element_type)
                if cpp_type is not None:
                    return cpp_type
    match _collect_unique_cpp_types(
        items=items,
        element_to_type=element_to_type,
    ):
        case [single]:
            return single
        case types:
            return f"std::variant<{', '.join(types)}>"


@beartype
def _items_need_variant(
    items: list[Value],
    element_to_type: Callable[[type | ListType | DictType], str | None],
) -> bool:
    """Check whether a collection's items need ``std::variant``."""
    if not items:
        return False
    element_type = infer_element_type(items=items)
    if element_type is None:
        return True
    match element_type:
        case DictType(value_type=vt):
            if vt is None or element_to_type(vt) is None:
                return True
        case other if element_to_type(other) is None:
            return True
        case _:
            pass
    return any(
        _needs_variant_type(
            data=v,
            element_to_type=element_to_type,
        )
        for v in items
    )


@beartype
def _needs_variant_type(
    data: Value,
    element_to_type: Callable[[type | ListType | DictType], str | None],
) -> bool:
    """Check whether *data* would produce ``std::variant`` or
    ``std::nullptr_t`` types in the generated C++ code.

    Used to determine whether ``#include <variant>`` is needed.
    """
    match data:
        case set():
            sorted_items: list[Value] = sorted(
                data,
                key=lambda v: (type(v).__name__, repr(v)),
            )
            return _items_need_variant(
                items=sorted_items,
                element_to_type=element_to_type,
            )
        case ordereddict():
            omap_vals = data.values()  # pyright: ignore[reportUnknownMemberType,reportUnknownVariableType]
            values: list[Value] = list(omap_vals)  # pyright: ignore[reportUnknownArgumentType]
            return _items_need_variant(
                items=values,
                element_to_type=element_to_type,
            )
        case list():
            return _items_need_variant(
                items=data,
                element_to_type=element_to_type,
            )
        case dict():
            return _items_need_variant(
                items=list(data.values()),
                element_to_type=element_to_type,
            )
        case _:
            return False


@beartype
def _has_empty_collection(data: Value) -> bool:
    """Check whether *data* contains any empty list/dict/set/omap.

    Empty collections produce ``std::nullptr_t`` placeholders, which
    require ``#include <cstddef>``.
    """
    match data:
        case list() | set() | dict() | ordereddict() if not data:
            return True
        case list():
            return any(_has_empty_collection(data=v) for v in data)
        case ordereddict() | dict():
            mapping_values = data.values()  # pyright: ignore[reportUnknownMemberType,reportUnknownVariableType]
            return any(
                _has_empty_collection(data=v)  # pyright: ignore[reportUnknownArgumentType]
                for v in mapping_values  # pyright: ignore[reportUnknownVariableType]
            )
        case _:
            return False


@beartype
def _build_variant_preamble(
    *,
    int_type: str,
    date_type: str | None,
    datetime_type: str | None,
) -> Callable[[Value], tuple[str, ...]]:
    """Build a ``data_dependent_preamble`` that emits
    ``#include <variant>`` when the data needs variant types.
    """
    element_to_type = _make_cpp_element_to_type(
        int_type=int_type,
        date_type=date_type,
        datetime_type=datetime_type,
    )

    def _variant_preamble(data: Value, /) -> tuple[str, ...]:
        """Return headers required by variant/nullptr_t usage."""
        lines: list[str] = []
        if _has_empty_collection(data=data):
            lines.append("#include <cstddef>")
        if _needs_variant_type(data=data, element_to_type=element_to_type):
            lines.append("#include <variant>")
        return tuple(lines)

    return _variant_preamble


@beartype
def _apply_cpp_variant_sequence_open(
    items: list[Value],
    type_to_opener: Callable[[type | ListType | DictType], str | None],
    element_to_type: Callable[[type | ListType | DictType], str | None],
) -> str:
    """Return a typed ``std::vector`` opener."""
    element_type = infer_element_type(items=items)
    if element_type is not None:
        opener = type_to_opener(element_type)
        if opener is not None:
            return opener
    inner = _compute_element_type_for_items(
        items=items,
        element_to_type=element_to_type,
    )
    return f"std::vector<{inner}>{{"


@beartype
def _apply_cpp_variant_dict_open(
    items: dict[str, Value],
    type_to_opener: Callable[[type | ListType | DictType], str | None],
    element_to_type: Callable[[type | ListType | DictType], str | None],
    opener_template: str,
) -> str:
    """Return a typed ``std::map`` opener."""
    element_type = infer_element_type(items=list(items.values()))
    if element_type is not None:
        opener = type_to_opener(element_type)
        if opener is not None:
            return opener
    value_type = _compute_element_type_for_items(
        items=list(items.values()),
        element_to_type=element_to_type,
    )
    if "unordered" in opener_template:
        map_kind = "std::unordered_map"
    else:
        map_kind = "std::map"
    return f"{map_kind}<std::string, {value_type}>{{"


@beartype
def _apply_cpp_variant_set_open(
    items: list[Value],
    element_to_type: Callable[[type | ListType | DictType], str | None],
) -> str:
    """Return a typed ``std::initializer_list`` opener."""
    inner = _compute_element_type_for_items(
        items=items,
        element_to_type=element_to_type,
    )
    return f"std::initializer_list<{inner}>{{"


@beartype
def _apply_cpp_variant_ordered_map_open(
    data: dict[str, Value],
    element_to_type: Callable[[type | ListType | DictType], str | None],
) -> str:
    """Return a typed ordered-map opener."""
    values: list[Value] = list(data.values())
    value_type = _compute_element_type_for_items(
        items=values,
        element_to_type=element_to_type,
    )
    return f"std::vector<std::pair<std::string, {value_type}>>{{"


@beartype
def _build_variant_sequence_open(
    *,
    int_type: str,
    date_type: str | None,
    datetime_type: str | None,
) -> Callable[[list[Value]], str]:
    """Build a sequence opener that uses ``std::variant`` for
    heterogeneous lists.
    """
    element_to_type = _make_cpp_element_to_type(
        int_type=int_type,
        date_type=date_type,
        datetime_type=datetime_type,
    )
    type_to_opener = make_type_to_opener(
        element_to_type=element_to_type,
        opener_template="std::vector<{type_name}>{{",
    )

    def _open(items: list[Value]) -> str:
        """Delegate to module-level implementation."""
        return _apply_cpp_variant_sequence_open(
            items, type_to_opener, element_to_type
        )

    return _open


@beartype
def _build_variant_dict_open(
    *,
    int_type: str,
    date_type: str | None,
    datetime_type: str | None,
    opener_template: str,
) -> Callable[[dict[str, Value]], str]:
    """Build a dict opener that uses ``std::variant`` for
    heterogeneous dict values.
    """
    element_to_type = _make_cpp_element_to_type(
        int_type=int_type,
        date_type=date_type,
        datetime_type=datetime_type,
    )
    type_to_opener = make_type_to_opener(
        element_to_type=element_to_type,
        opener_template=opener_template,
    )

    def _open(items: dict[str, Value]) -> str:
        """Delegate to module-level implementation."""
        return _apply_cpp_variant_dict_open(
            items, type_to_opener, element_to_type, opener_template
        )

    return _open


@beartype
def _build_variant_set_open(
    *,
    int_type: str,
    date_type: str | None,
    datetime_type: str | None,
) -> Callable[[list[Value]], str]:
    """Build a set opener that uses typed ``std::initializer_list``."""
    element_to_type = _make_cpp_element_to_type(
        int_type=int_type,
        date_type=date_type,
        datetime_type=datetime_type,
    )

    def _open(items: list[Value]) -> str:
        """Delegate to module-level implementation."""
        return _apply_cpp_variant_set_open(items, element_to_type)

    return _open


@beartype
def _build_variant_ordered_map_open(
    *,
    int_type: str,
    date_type: str | None,
    datetime_type: str | None,
) -> Callable[[dict[str, Value]], str]:
    """Build an ordered-map opener that uses
    ``std::vector<std::pair<...>>``.
    """
    element_to_type = _make_cpp_element_to_type(
        int_type=int_type,
        date_type=date_type,
        datetime_type=datetime_type,
    )

    def _open(data: dict[str, Value]) -> str:
        """Delegate to module-level implementation."""
        return _apply_cpp_variant_ordered_map_open(data, element_to_type)

    return _open


@beartype
def _build_ordered_map_config(
    *,
    int_type: str,
    date_type: str | None,
    datetime_type: str | None,
) -> OrderedMapFormatConfig:
    """Build an ``OrderedMapFormatConfig`` with a variant opener."""
    return OrderedMapFormatConfig(
        ordered_map_open=_build_variant_ordered_map_open(
            int_type=int_type,
            date_type=date_type,
            datetime_type=datetime_type,
        ),
        close="}",
        preamble_lines=(
            "#include <utility>",
            "#include <vector>",
        ),
    )


@beartype
def _format_variable_declaration(
    name: str,
    value: str,
    _data: Value,
) -> str:
    """Format a C++ variable declaration.

    * ``const auto*`` — string literal (``"..."``), required by
      ``readability-qualified-auto``.
    * ``auto`` — typed expression
      (e.g. ``std::vector<int>{...}``).
    """
    match _infer_value_kind(value=value):
        case ValueKind.STRING_LITERAL:
            type_keyword = "const auto*"
        case ValueKind.TYPED_EXPRESSION:
            type_keyword = "auto"
        case _ as unreachable:
            assert_never(unreachable)  # pyrefly: ignore[bad-argument-type]
    return f"{type_keyword} {name} = {value};"


def _infer_value_kind(*, value: str) -> ValueKind:
    """Classify a formatted C++ value string."""
    if value.startswith('"'):
        return ValueKind.STRING_LITERAL
    return ValueKind.TYPED_EXPRESSION


def _cpp_call_stub(
    name: str, _params: Sequence[str], stub_return: StubReturn, /
) -> tuple[str, ...]:
    """Return C++ stub declarations for a call name."""
    parts = name.split(sep=".")
    if len(parts) == 1:
        return (f"auto {parts[0]}(auto...) {{ return 0; }}",)
    root = parts[0]
    method = parts[-1]
    fields = parts[1:-1]
    if not fields:
        type_name = f"{root}Type_"
        return (
            f"struct {type_name} {{"
            f" auto {method}(auto...) const {{ return 0; }} }};",
            f"const {type_name} {root};",
        )
    lines: list[str] = []
    inner_type = f"{fields[-1]}Type_"
    if stub_return is StubReturn.VALUE:
        lines.append(
            f"struct {inner_type} {{"
            f" [[nodiscard]] auto {method}(auto...) const"
            f" {{ return 0; }} }};"
        )
    else:
        lines.append(
            f"struct {inner_type} {{ void {method}(auto...) const {{}} }};"
        )
    prev_type = inner_type
    for i in range(len(fields) - 2, -1, -1):
        curr_type = f"{fields[i]}Type_"
        lines.append(f"struct {curr_type} {{ {prev_type} {fields[i + 1]}; }};")
        prev_type = curr_type
    root_type = f"{root}Type_"
    lines.append(f"struct {root_type} {{ {prev_type} {fields[0]}; }};")
    lines.append(f"const {root_type} {root};")
    return tuple(lines)


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
    supports_variable_names = True
    supports_dotted_calls = True

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

        @property
        def cpp_type(self) -> str:
            """Return the C++ type name for this date format."""
            cfg: DateFormatConfig = self.value
            if cfg.type_produced is str:
                return "std::string"
            return "std::chrono::year_month_day"

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

        @property
        def cpp_type(self) -> str:
            """Return the C++ type name for this datetime format."""
            cfg: DatetimeFormatConfig = self.value
            if cfg.type_produced is str:
                return "std::string"
            return "std::chrono::system_clock::time_point"

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

        def get_config(
            self,
            *,
            int_type: str,
            date_type: str | None,
            datetime_type: str | None,
        ) -> SequenceFormatConfig:
            """Return the sequence format config for the given int
            type.
            """
            factory: Callable[..., SequenceFormatConfig] = self.value
            return factory(
                int_type=int_type,
                date_type=date_type,
                datetime_type=datetime_type,
            )

    class SetFormats(enum.Enum):
        """Set type options for C++."""

        SET = SetFormatConfig(
            set_open=lambda _items: "{",
            close="}",
            empty_set=None,
            preamble_lines=(),
            set_opener_template="",
            coerce_mixed_to_str=False,
        )

        def get_config(
            self,
            *,
            int_type: str,
            date_type: str,
            datetime_type: str,
        ) -> SetFormatConfig:
            """Return the set format config with variant opener."""
            return dataclasses.replace(
                self.value,
                set_open=_build_variant_set_open(
                    int_type=int_type,
                    date_type=date_type,
                    datetime_type=datetime_type,
                ),
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

        MAP = _DictFormatOption(
            config=DictFormatConfig(
                dict_open=lambda _items: "{",
                close="}",
                format_entry=braced_dict_entry(
                    format_value=passthrough_sequence_entry
                ),
                empty_dict=None,
                preamble_lines=("#include <map>",),
                narrowed_open=None,
            ),
            opener_template="std::map<std::string, {type_name}>{{",
        )
        UNORDERED_MAP = _DictFormatOption(
            config=DictFormatConfig(
                dict_open=lambda _items: "{",
                close="}",
                format_entry=braced_dict_entry(
                    format_value=passthrough_sequence_entry
                ),
                empty_dict=None,
                preamble_lines=("#include <unordered_map>",),
                narrowed_open=None,
            ),
            opener_template=("std::unordered_map<std::string, {type_name}>{{"),
        )

        def get_config(
            self,
            *,
            int_type: str,
            date_type: str,
            datetime_type: str,
        ) -> DictFormatConfig:
            """Return the dict format config with variant opener."""
            option: _DictFormatOption = self.value
            return dataclasses.replace(
                option.config,
                dict_open=_build_variant_dict_open(
                    int_type=int_type,
                    date_type=date_type,
                    datetime_type=datetime_type,
                    opener_template=option.opener_template,
                ),
            )

    class EmptyDictKey(enum.Enum):
        """Empty dict key options."""

        ALLOW = enum.auto()

    class FloatFormats(
        FloatSpecialsMixin,
        enum.Enum,
        positive_infinity="INFINITY",
        negative_infinity="-INFINITY",
        nan="NAN",
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
        """Cpp call style options."""

        POSITIONAL = PositionalCallStyle()

    call_styles = CallStyles

    @staticmethod
    def wrap_in_file(
        content: str,
        variable_name: str,
        body_preamble: tuple[str, ...],
    ) -> str:
        """Wrap a C++ declaration in a function body."""
        del variable_name
        content = prepend_body_preamble(
            content=content,
            body_preamble=body_preamble,
        )
        return f"void check_() {{\n{content}\n}}"

    @staticmethod
    def wrap_combined_in_file(
        declaration: str,
        assignment: str,
        variable_name: str,
        body_preamble: tuple[str, ...],
    ) -> str:
        """Wrap C++ declaration + assignment in a function body."""
        return Cpp.wrap_in_file(
            content=declaration + "\n" + assignment,
            variable_name=variable_name,
            body_preamble=body_preamble,
        )

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
        numeric_style: NumericStyles = NumericStyles.OVERLOADED,
        string_format: StringFormats = StringFormats.DOUBLE,
        trailing_comma: TrailingCommas = TrailingCommas.YES,
        line_ending: LineEndings = LineEndings.SEMICOLON,
        call_style: CallStyles = CallStyles.POSITIONAL,
        indent: str = "    ",
    ) -> None:
        """Initialize Cpp language specification."""
        self.variable_type_hints = variable_type_hints
        self.sequence_format = sequence_format
        self.null_literal = "nullptr"
        self.true_literal = "true"
        self.false_literal = "false"
        cpp_date_type = date_format.cpp_type
        cpp_datetime_type = datetime_format.cpp_type
        int_type = numeric_literal_suffix.int_type
        self.sequence_format_config: SequenceFormatConfig = (
            sequence_format.get_config(
                int_type=int_type,
                date_type=cpp_date_type,
                datetime_type=cpp_datetime_type,
            )
        )
        self.set_format = set_format
        self.set_format_config: SetFormatConfig = set_format.get_config(
            int_type=int_type,
            date_type=cpp_date_type,
            datetime_type=cpp_datetime_type,
        )
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
        self.dict_format_config: DictFormatConfig = dict_format.get_config(
            int_type=int_type,
            date_type=cpp_date_type,
            datetime_type=cpp_datetime_type,
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
        self.numeric_style = numeric_style
        self.string_format = string_format
        self.trailing_comma = trailing_comma
        self.line_ending = line_ending
        self.comment_config: CommentConfig = comment_format.value
        self.ordered_map_format_config: OrderedMapFormatConfig = (
            _build_ordered_map_config(
                int_type=int_type,
                date_type=cpp_date_type,
                datetime_type=cpp_datetime_type,
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
        self.static_body_preamble: Sequence[str] = ()
        self.data_dependent_preamble: Callable[[Value], tuple[str, ...]] = (
            _build_variant_preamble(
                int_type=int_type,
                date_type=cpp_date_type,
                datetime_type=cpp_datetime_type,
            )
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
            format_lines=tuple,
        )

        self.type_hint_collection_preamble_lines = no_type_hint_preamble
        self.special_float_preamble: tuple[str, ...] = ("#include <cmath>",)
        self.call_style = call_style
        self.call_style_config: CallStyle | None = call_style.value
        self.statement_terminator = ";"
        self.format_call_stub: Callable[
            [str, Sequence[str], StubReturn], tuple[str, ...]
        ] = no_call_stub
        self.format_call_preamble_stub: Callable[
            [str, Sequence[str], StubReturn], tuple[str, ...]
        ] = _cpp_call_stub
