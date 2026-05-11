"""C++ language specification."""

import dataclasses
import datetime
import enum
from collections.abc import Callable, Sequence
from functools import cached_property
from types import MappingProxyType
from typing import ClassVar, assert_never

from beartype import beartype
from ruamel.yaml.compat import ordereddict

from literalizer._formatters.collection_openers import (
    make_element_to_type,
)
from literalizer._formatters.format_dates import (
    format_date_iso,
    format_datetime_epoch,
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
    make_overflow_fallback_formatter,
    make_ull_fallback,
)
from literalizer._formatters.format_strings import format_string_backslash
from literalizer._formatters.type_inference import (
    DictType,
    ListType,
    infer_element_type,
)
from literalizer._language import (
    NO_HETEROGENEOUS_BEHAVIOR,
    NON_KEBAB_REF_CASES,
    CallStyle,
    CommentConfig,
    DateFormatConfig,
    DatetimeFormatConfig,
    DeclarationStyleConfig,
    DictFormatConfig,
    FloatSpecialsMixin,
    HeterogeneousBehavior,
    IdentifierCase,
    LanguageCls,
    ModifierCombination,
    OrderedMapFormatConfig,
    PositionalCallStyle,
    SequenceFormatConfig,
    SetFormatConfig,
    StubReturn,
    TrailingCommaConfig,
    body_preamble_from_scalars,
    date_scalar_preamble,
    default_wrap_calls_with_declarations,
    identity_call_arg,
    identity_call_ref_identifier,
    identity_call_statement,
    identity_call_target,
    never_inhibits_consuming_form,
    no_call_stub,
    no_type_hint_preamble,
    no_validate_call_arg,
    no_validate_spec_for_data,
    prepend_body_preamble,
)
from literalizer._types import Value, ValueKind


class _CppModifiers(enum.Enum):
    """Declaration modifiers supported by C++.

    Each member's value is the C++ keyword it renders to.  Declaration
    order matches canonical C++ modifier order (``static`` before
    ``const``).

    Exposed as :attr:`Cpp.Modifiers` / :attr:`Cpp.modifiers`.
    """

    STATIC = "static"
    """Storage: internal linkage at namespace scope, or per-class
    storage inside a class.
    """

    CONST = "const"
    """Immutability: the variable cannot be reassigned."""


_INT32_MIN = -(1 << 31)
_INT32_MAX = (1 << 31) - 1


_IntTypeResolver = Callable[[list[int]], str]


@beartype
def _narrowest_cpp_int_type(values: list[int]) -> str:
    """Return the narrowest C++ integer type holding every value in
    *values*: ``int`` when every value fits in 32 bits, else
    ``long long``.  Empty inputs return ``"int"``.  ``long`` is skipped
    because its width is platform-dependent (32-bit on Windows, 64-bit
    on Unix).
    """
    if all(_INT32_MIN <= v <= _INT32_MAX for v in values):
        return "int"
    return "long long"


@beartype
def _static_int_resolver(int_type: str) -> _IntTypeResolver:
    """Return a resolver that always yields *int_type*."""

    def _resolve(_values: list[int]) -> str:
        """Return the fixed int type, ignoring values."""
        return int_type

    return _resolve


@beartype
def _collect_int_leaves(
    *,
    items: list[Value],
    element_type: type | ListType | DictType,
) -> list[int]:
    """Collect int values that would occupy the int leaf of
    *element_type* when *items* is resolved to its C++ type.
    """
    if element_type is int:
        return [
            item
            for item in items
            if isinstance(item, int) and not isinstance(item, bool)
        ]
    if isinstance(element_type, ListType):
        return [
            leaf
            for item in items
            if isinstance(item, list)
            for leaf in _collect_int_leaves(
                items=item,
                element_type=element_type.inner,
            )
        ]
    if (
        isinstance(element_type, DictType)
        and element_type.value_type is not None
    ):
        return [
            leaf
            for item in items
            if isinstance(item, dict)
            for leaf in _collect_int_leaves(
                items=list(item.values()),
                element_type=element_type.value_type,
            )
        ]
    return []


@beartype
def _collect_direct_ints(items: list[Value]) -> list[int]:
    """Collect int values that are direct items (not nested in
    sub-collections).  Excludes booleans.
    """
    return [
        item
        for item in items
        if isinstance(item, int) and not isinstance(item, bool)
    ]


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
    return f"std::chrono::system_clock::time_point{{{' + '.join(parts)}}}"


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


@dataclasses.dataclass(frozen=True)
class _CppTypeCtx:
    """Context for C++ type resolution with value-driven int narrowing.

    Bundles the date/datetime type strings (which are static) with an
    :data:`_IntTypeResolver` that picks the narrowest int type for a
    given collection of values.  Used wherever a type string is emitted
    so that the int type can be specialized per-collection.
    """

    int_resolver: _IntTypeResolver
    date_type: str | None
    datetime_type: str | None

    def element_to_type(
        self,
        *,
        int_type: str,
    ) -> Callable[[type | ListType | DictType], str | None]:
        """Build an element-to-type resolver with the given *int_type*."""
        return _make_cpp_element_to_type(
            int_type=int_type,
            date_type=self.date_type,
            datetime_type=self.datetime_type,
        )


@beartype
def _build_cpp_array_open(
    *,
    type_ctx: _CppTypeCtx,
) -> Callable[[list[Value]], str]:
    """Build an opener that emits ``std::array<T, N>`` with the int
    type narrowed to the narrowest that holds every int value.
    """

    def _open(items: list[Value]) -> str:
        """Return the typed ``std::array`` opener, or ``{`` on
        fallback.
        """
        int_type = type_ctx.int_resolver(
            [
                item
                for item in items
                if isinstance(item, int) and not isinstance(item, bool)
            ],
        )
        element_to_type = type_ctx.element_to_type(int_type=int_type)
        type_name = element_to_type(type(items[0])) if items else None
        if type_name is None or not all(
            element_to_type(type(i)) == type_name for i in items
        ):
            return "{"
        return f"std::array<{type_name}, {len(items)}>{{"

    return _open


@beartype
def _make_initializer_list_config(
    *,
    type_ctx: _CppTypeCtx,
) -> SequenceFormatConfig:
    """Build an INITIALIZER_LIST sequence config."""
    return SequenceFormatConfig(
        sequence_open=_build_variant_sequence_open(type_ctx=type_ctx),
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
        narrowed_empty_form=None,
    )


@beartype
def _make_array_config(
    *,
    type_ctx: _CppTypeCtx,
) -> SequenceFormatConfig:
    """Return the ARRAY sequence config."""
    return SequenceFormatConfig(
        sequence_open=_build_cpp_array_open(type_ctx=type_ctx),
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
        narrowed_empty_form=None,
    )


@dataclasses.dataclass(frozen=True)
class _DictFormatOption:
    """A dict format bundled with its typed opener template."""

    config: DictFormatConfig
    opener_template: str


@dataclasses.dataclass(frozen=True)
class _NumericLiteralSuffixConfig:
    """Configuration for a numeric literal suffix option."""

    int_resolver: _IntTypeResolver
    formatter_wrapper: Callable[[Callable[[int], str]], Callable[[int], str]]


def _identity_wrapper(
    base: Callable[[int], str],
) -> Callable[[int], str]:
    """Return the formatter unchanged."""
    return base


@beartype
def _compute_cpp_type(
    *,
    item: Value,
    element_to_type: Callable[[type | ListType | DictType], str | None],
    type_ctx: _CppTypeCtx,
) -> str:
    """Return the C++ type string for a single value.

    *element_to_type* must have the int type already narrowed for the
    enclosing collection's variant arm (or homogeneous leaf).  When the
    value is a sub-collection, recursion re-narrows independently via
    *type_ctx*.
    """
    match item:
        case ordereddict():
            omap_values = item.values()  # pyright: ignore[reportUnknownMemberType,reportUnknownVariableType]
            values: list[Value] = list(omap_values)  # pyright: ignore[reportUnknownArgumentType]
            value_type = _compute_element_type_for_items(
                items=values,
                type_ctx=type_ctx,
            )
            return f"std::vector<std::pair<std::string, {value_type}>>"
        case dict():
            values = list(item.values())
            value_type = _compute_element_type_for_items(
                items=values,
                type_ctx=type_ctx,
            )
            return f"std::map<std::string, {value_type}>"
        case list():
            inner_type = _compute_element_type_for_items(
                items=item,
                type_ctx=type_ctx,
            )
            return f"std::vector<{inner_type}>"
        case set():
            sorted_items: list[Value] = sorted(
                item,
                key=lambda v: (type(v).__name__, repr(v)),
            )
            inner_type = _compute_element_type_for_items(
                items=sorted_items,
                type_ctx=type_ctx,
            )
            return f"std::initializer_list<{inner_type}>"
        case _:
            cpp_type = element_to_type(type(item))
            if cpp_type is not None:
                return cpp_type
            return "std::nullptr_t"


@beartype
def _collect_unique_cpp_types(
    *,
    items: list[Value],
    element_to_type: Callable[[type | ListType | DictType], str | None],
    type_ctx: _CppTypeCtx,
) -> list[str]:
    """Collect unique C++ type names for each item, preserving order."""
    unique_cpp_types: list[str] = []
    seen: set[str] = set()
    for item in items:
        item_type = _compute_cpp_type(
            item=item,
            element_to_type=element_to_type,
            type_ctx=type_ctx,
        )
        if item_type not in seen:
            seen.add(item_type)
            unique_cpp_types.append(item_type)
    return unique_cpp_types


@beartype
def _compute_element_type_for_items(
    *,
    items: list[Value],
    type_ctx: _CppTypeCtx,
) -> str:
    """Return the C++ element type for a collection of items.

    Returns a single type name when all items have the same C++ type,
    or ``std::variant<T1, T2, ...>`` for mixed types.  Returns
    ``std::nullptr_t`` for empty collections.  Narrows int-valued leaves
    to the narrowest C++ int type that holds the actual values.
    """
    if not items:
        return "std::nullptr_t"
    element_type = infer_element_type(items=items)
    if element_type is not None:
        match element_type:
            case DictType(value_type=None, values=dict_values):
                value_type = _compute_element_type_for_items(
                    items=list(dict_values),
                    type_ctx=type_ctx,
                )
                return f"std::map<std::string, {value_type}>"
            case _:
                int_leaves = _collect_int_leaves(
                    items=items,
                    element_type=element_type,
                )
                homogeneous_int_type = type_ctx.int_resolver(int_leaves)
                element_to_type = type_ctx.element_to_type(
                    int_type=homogeneous_int_type,
                )
                cpp_type = element_to_type(element_type)
                if cpp_type is not None:
                    return cpp_type
    variant_int_type = type_ctx.int_resolver(
        _collect_direct_ints(items=items),
    )
    variant_element_to_type = type_ctx.element_to_type(
        int_type=variant_int_type,
    )
    match _collect_unique_cpp_types(
        items=items,
        element_to_type=variant_element_to_type,
        type_ctx=type_ctx,
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
    type_ctx: _CppTypeCtx,
) -> Callable[[Value], tuple[str, ...]]:
    """Build a ``data_dependent_preamble`` that emits
    ``#include <variant>`` when the data needs variant types.
    """
    element_to_type = type_ctx.element_to_type(int_type="long long")

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
    *,
    items: list[Value],
    type_ctx: _CppTypeCtx,
) -> str:
    """Return a typed ``std::vector`` opener."""
    inner = _compute_element_type_for_items(items=items, type_ctx=type_ctx)
    return f"std::vector<{inner}>{{"


@beartype
def _apply_cpp_variant_dict_open(
    *,
    items: dict[str, Value],
    type_ctx: _CppTypeCtx,
    opener_template: str,
) -> str:
    """Return a typed ``std::map`` or ``std::unordered_map`` opener."""
    value_type = _compute_element_type_for_items(
        items=list(items.values()),
        type_ctx=type_ctx,
    )
    map_kind = (
        "std::unordered_map" if "unordered" in opener_template else "std::map"
    )
    return f"{map_kind}<std::string, {value_type}>{{"


@beartype
def _apply_cpp_variant_set_open(
    *,
    items: list[Value],
    type_ctx: _CppTypeCtx,
) -> str:
    """Return a typed ``std::initializer_list`` opener."""
    inner = _compute_element_type_for_items(items=items, type_ctx=type_ctx)
    return f"std::initializer_list<{inner}>{{"


@beartype
def _apply_cpp_variant_ordered_map_open(
    *,
    data: dict[str, Value],
    type_ctx: _CppTypeCtx,
) -> str:
    """Return a typed ordered-map opener."""
    values: list[Value] = list(data.values())
    value_type = _compute_element_type_for_items(
        items=values,
        type_ctx=type_ctx,
    )
    return f"std::vector<std::pair<std::string, {value_type}>>{{"


@beartype
def _build_variant_sequence_open(
    *,
    type_ctx: _CppTypeCtx,
) -> Callable[[list[Value]], str]:
    """Build a sequence opener that uses ``std::variant`` for
    heterogeneous lists.
    """

    def _open(items: list[Value]) -> str:
        """Delegate to module-level implementation."""
        return _apply_cpp_variant_sequence_open(items=items, type_ctx=type_ctx)

    return _open


@beartype
def _build_variant_dict_open(
    *,
    type_ctx: _CppTypeCtx,
    opener_template: str,
) -> Callable[[dict[str, Value]], str]:
    """Build a dict opener that uses ``std::variant`` for
    heterogeneous dict values.
    """

    def _open(items: dict[str, Value]) -> str:
        """Delegate to module-level implementation."""
        return _apply_cpp_variant_dict_open(
            items=items,
            type_ctx=type_ctx,
            opener_template=opener_template,
        )

    return _open


@beartype
def _build_variant_set_open(
    *,
    type_ctx: _CppTypeCtx,
) -> Callable[[list[Value]], str]:
    """Build a set opener that uses typed ``std::initializer_list``."""

    def _open(items: list[Value]) -> str:
        """Delegate to module-level implementation."""
        return _apply_cpp_variant_set_open(items=items, type_ctx=type_ctx)

    return _open


@beartype
def _build_variant_ordered_map_open(
    *,
    type_ctx: _CppTypeCtx,
) -> Callable[[dict[str, Value]], str]:
    """Build an ordered-map opener that uses
    ``std::vector<std::pair<...>>``.
    """

    def _open(data: dict[str, Value]) -> str:
        """Delegate to module-level implementation."""
        return _apply_cpp_variant_ordered_map_open(
            data=data,
            type_ctx=type_ctx,
        )

    return _open


@beartype
def _build_ordered_map_config(
    *,
    type_ctx: _CppTypeCtx,
) -> OrderedMapFormatConfig:
    """Build an ``OrderedMapFormatConfig`` with a variant opener."""
    return OrderedMapFormatConfig(
        ordered_map_open=_build_variant_ordered_map_open(type_ctx=type_ctx),
        close="}",
        preamble_lines=(
            "#include <utility>",
            "#include <vector>",
        ),
    )


@beartype
def _cpp_modifier_prefix(modifiers: frozenset[enum.Enum]) -> str:
    """Return the ``static const `` prefix for a C++ declaration,
    including a trailing space when non-empty.

    Values that are not :class:`_CppModifiers` members are ignored.
    """
    keywords = [m.value for m in _CppModifiers if m in modifiers]
    if not keywords:
        return ""
    return " ".join(keywords) + " "


@beartype
def _format_variable_declaration(
    name: str,
    value: str,
    _data: Value,
    modifiers: frozenset[enum.Enum],
) -> str:
    """Format a C++ variable declaration.

    * ``const auto*`` — string literal (``"..."``), required by
      ``readability-qualified-auto``.
    * ``auto`` — typed expression (e.g. ``std::vector<int>{...}``).

    When *modifiers* is non-empty, applicable modifier keywords
    (``static``, ``const``) are prepended.  ``const`` is not duplicated
    against the built-in ``const auto*`` for string literals.
    """
    match _infer_value_kind(value=value):
        case ValueKind.STRING_LITERAL:
            type_keyword = "const auto*"
            extra = modifiers - {_CppModifiers.CONST}
        case ValueKind.TYPED_EXPRESSION:
            type_keyword = "auto"
            extra = modifiers
        case _ as unreachable:
            assert_never(unreachable)  # pyrefly: ignore[bad-argument-type]
    prefix = _cpp_modifier_prefix(modifiers=extra)
    return f"{prefix}{type_keyword} {name} = {value};"


def _infer_value_kind(*, value: str) -> ValueKind:
    """Classify a formatted C++ value string."""
    if value.startswith('"'):
        return ValueKind.STRING_LITERAL
    return ValueKind.TYPED_EXPRESSION


def _cpp_call_stub(
    parts: Sequence[str],
    _params: Sequence[str],
    stub_return: StubReturn,
    _args: Sequence[Value],
    /,
) -> tuple[str, ...]:
    """Return C++ stub declarations for a call name."""
    if len(parts) == 1:
        return (f"auto {parts[0]}(auto...) {{ return 0; }}",)
    root = parts[0]
    method = parts[-1]
    fields = parts[1:-1]
    if not fields:
        type_name = f"{root}Type_"
        if stub_return is StubReturn.VOID:
            method_decl = f"void {method}(auto...) const {{}}"
        else:
            method_decl = (
                f"[[nodiscard]] auto {method}(auto...) const {{ return 0; }}"
            )
        return (
            f"struct {type_name} {{ {method_decl} }};",
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
@dataclasses.dataclass(frozen=True, kw_only=True)
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

    module_name: str = "Module"

    extension = ".cpp"
    pygments_name = "cpp"
    supports_special_floats = True
    supports_variable_names = True
    supports_dotted_calls = True
    has_free_function_calls = True
    reserved_identifiers: ClassVar[frozenset[str]] = frozenset()
    allows_bare_call_statement = True
    allows_empty_call_parens = True
    supports_dotted_call_stub = True
    call_returns_expression = True
    supports_zero_parameter_calls = True
    supports_inline_multiline_dict_args = True
    supports_standalone_comments_in_wrapped_calls = True
    supports_commented_dict_call_args = True
    supports_module_name = True
    supports_call_refs_in_dict_literals = True

    format_call_arg: ClassVar["staticmethod[[Value, str], str]"] = (
        staticmethod(
            identity_call_arg,
        )
    )
    """Callable that rewrites a formatted direct call argument."""

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

        EPOCH = DatetimeFormatConfig(
            formatter=format_datetime_epoch,
            type_produced=int,
        )

        @property
        def cpp_type(self) -> str:
            """Return the C++ type name for this datetime format."""
            cfg: DatetimeFormatConfig = self.value
            if cfg.type_produced is str:
                return "std::string"
            if cfg.type_produced is int:
                return "long long"
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
            type_ctx: _CppTypeCtx,
        ) -> SequenceFormatConfig:
            """Return the sequence format config for the given context."""
            factory: Callable[..., SequenceFormatConfig] = self.value
            return factory(type_ctx=type_ctx)

    class SetFormats(enum.Enum):
        """Set type options for C++."""

        SET = SetFormatConfig(
            set_open=lambda _items: "{",
            close="}",
            empty_set=None,
            preamble_lines=(),
            set_opener_template="",
            supports_heterogeneity=True,
            supports_trailing_comma=True,
        )

        def get_config(
            self,
            *,
            type_ctx: _CppTypeCtx,
        ) -> SetFormatConfig:
            """Return the set format config with variant opener."""
            return dataclasses.replace(
                self.value,
                set_open=_build_variant_set_open(type_ctx=type_ctx),
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
                supports_trailing_comma=True,
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
                supports_trailing_comma=True,
            ),
            opener_template=("std::unordered_map<std::string, {type_name}>{{"),
        )

        def get_config(
            self,
            *,
            type_ctx: _CppTypeCtx,
        ) -> DictFormatConfig:
            """Return the dict format config with variant opener."""
            option: _DictFormatOption = self.value
            return dataclasses.replace(
                option.config,
                dict_open=_build_variant_dict_open(
                    type_ctx=type_ctx,
                    opener_template=option.opener_template,
                ),
            )

    class EmptyDictKey(enum.Enum):
        """Empty dict key options."""

        ALLOW = enum.auto()

    class FloatFormats(
        FloatSpecialsMixin,
        enum.Enum,
        positive_infinity="static_cast<double>(INFINITY)",
        negative_infinity="-static_cast<double>(INFINITY)",
        nan="static_cast<double>(NAN)",
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
            int_resolver=_narrowest_cpp_int_type,
            formatter_wrapper=_identity_wrapper,
        )
        AUTO = _NumericLiteralSuffixConfig(
            int_resolver=_static_int_resolver(int_type="long"),
            formatter_wrapper=make_long_suffix_formatter,
        )

        @property
        def int_resolver(self) -> _IntTypeResolver:
            """Return the value-driven int type resolver."""
            config: _NumericLiteralSuffixConfig = self.value
            return config.int_resolver

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

        DOUBLE = enum.auto()

    class TrailingCommas(enum.Enum):
        """Trailing comma options."""

        YES = TrailingCommaConfig(multiline_trailing_comma=True)
        NO = TrailingCommaConfig(multiline_trailing_comma=False)

    Modifiers = _CppModifiers

    date_formats = DateFormats
    datetime_formats = DatetimeFormats
    bytes_formats = BytesFormats
    sequence_formats = SequenceFormats
    set_formats = SetFormats
    comment_formats = CommentFormats
    modifiers = _CppModifiers

    class HeterogeneousStrategies(enum.Enum):
        """Heterogeneous-scalar strategy options — this language only
        supports raising.
        """

        ERROR = NO_HETEROGENEOUS_BEHAVIOR

    heterogeneous_strategies = HeterogeneousStrategies

    class VersionFormats(enum.Enum):
        """Version options for C++."""

        CPP20 = enum.auto()

    version_formats = VersionFormats

    module_name_case: ClassVar[IdentifierCase] = IdentifierCase.SNAKE
    identifier_cases: ClassVar[tuple[IdentifierCase, ...]] = (
        IdentifierCase.SNAKE,
        IdentifierCase.UPPER_SNAKE,
        IdentifierCase.PASCAL,
        IdentifierCase.CAMEL,
    )
    supported_ref_cases: ClassVar[frozenset[IdentifierCase]] = (
        NON_KEBAB_REF_CASES
    )

    modifier_combinations: ClassVar[tuple[ModifierCombination, ...]] = (
        ModifierCombination(
            name="static_const",
            modifiers=frozenset(
                {_CppModifiers.STATIC, _CppModifiers.CONST},
            ),
        ),
    )
    validate_spec_for_data = no_validate_spec_for_data

    @cached_property
    def validate_call_arg(self) -> Callable[[Value], None]:
        """Return call-argument validation for this language."""
        return no_validate_call_arg

    @cached_property
    def format_call_statement(self) -> Callable[[str], str]:
        """Return call-statement formatting for this language."""
        return identity_call_statement

    wrap_calls_with_declarations = default_wrap_calls_with_declarations

    class VariableTypeHints(enum.Enum):
        """Variable type hint options."""

        NEVER = enum.auto()
        SAFE = enum.auto()

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

    class StatementTerminatorStyles(enum.Enum):
        """Statement terminator options."""

        SEMICOLON = enum.auto()

    statement_terminator_styles = StatementTerminatorStyles

    class CallStyles(enum.Enum):
        """Cpp call style options."""

        POSITIONAL = PositionalCallStyle()

    call_styles = CallStyles

    def wrap_in_file(
        self,
        content: str,
        variable_name: str,
        body_preamble: tuple[str, ...],
    ) -> str:
        """Wrap a C++ declaration in a main function."""
        content = prepend_body_preamble(
            content=content,
            body_preamble=body_preamble,
        )
        use_line = f"\n    (void){variable_name};" if variable_name else ""
        return (
            f"int {self.module_name}() {{\n{content}{use_line}\n"
            "    return 0;\n}"
        )

    def wrap_combined_in_file(
        self,
        declaration: str,
        assignment: str,
        variable_name: str,
        body_preamble: tuple[str, ...],
    ) -> str:
        """Wrap C++ declaration + assignment in a function body.

        Reads ``variable_name`` between the declaration and the
        assignment so the initial value is not a dead store flagged by
        clang-tidy's ``clang-analyzer-deadcode.DeadStores`` check.
        """
        mid_use = f"(void){variable_name};\n"
        return self.wrap_in_file(
            content=f"{declaration}\n{mid_use}{assignment}",
            variable_name=variable_name,
            body_preamble=body_preamble,
        )

    date_format: DateFormats = DateFormats.CPP
    datetime_format: DatetimeFormats = DatetimeFormats.CPP
    bytes_format: BytesFormats = BytesFormats.HEX
    sequence_format: SequenceFormats = SequenceFormats.INITIALIZER_LIST
    set_format: SetFormats = SetFormats.SET
    variable_type_hints: VariableTypeHints = VariableTypeHints.NEVER
    comment_format: CommentFormats = CommentFormats.DOUBLE_SLASH
    declaration_style: DeclarationStyles = DeclarationStyles.AUTO
    dict_entry_style: DictEntryStyles = DictEntryStyles.DEFAULT
    dict_format: DictFormats = DictFormats.MAP
    float_format: FloatFormats = FloatFormats.REPR
    integer_format: IntegerFormats = IntegerFormats.DECIMAL
    numeric_literal_suffix: NumericLiteralSuffixes = (
        NumericLiteralSuffixes.NONE
    )
    numeric_separator: NumericSeparators = NumericSeparators.NONE
    numeric_style: NumericStyles = NumericStyles.OVERLOADED
    string_format: StringFormats = StringFormats.DOUBLE
    trailing_comma: TrailingCommas = TrailingCommas.YES
    statement_terminator_style: StatementTerminatorStyles = (
        StatementTerminatorStyles.SEMICOLON
    )
    call_style: CallStyles = CallStyles.POSITIONAL
    heterogeneous_strategy: HeterogeneousStrategies = (
        HeterogeneousStrategies.ERROR
    )
    # Keep in sync with the ``-std=`` flag passed to clang++ in
    # ``.github/workflows/lint.yml``.
    language_version: VersionFormats = VersionFormats.CPP20
    indent: str = "    "

    null_literal: ClassVar[str] = "nullptr"
    true_literal: ClassVar[str] = "true"
    false_literal: ClassVar[str] = "false"
    indent_closing_delimiter: ClassVar[bool] = False
    element_separator: ClassVar[str] = ", "
    skip_null_dict_values: ClassVar[bool] = False
    supports_collection_comments: ClassVar[bool] = True
    supports_scalar_before_comments: ClassVar[bool] = True
    supports_scalar_inline_comments: ClassVar[bool] = False
    statement_terminator: ClassVar[str] = ";"
    static_preamble: ClassVar[Sequence[str]] = ("#include <initializer_list>",)
    static_body_preamble: ClassVar[Sequence[str]] = ()
    special_float_preamble: ClassVar[tuple[str, ...]] = ("#include <cmath>",)

    @cached_property
    def format_string(self) -> Callable[[str], str]:
        """Format a string value as a quoted literal."""
        return format_string_backslash

    @cached_property
    def format_sequence_entry(self) -> Callable[[Value, str], str]:
        """Format a sequence entry."""
        return passthrough_sequence_entry

    @cached_property
    def format_set_entry(self) -> Callable[[Value, str], str]:
        """Format a set entry."""
        return passthrough_set_entry

    @cached_property
    def format_variable_assignment(self) -> Callable[[str, str, Value], str]:
        """Format an assignment to an existing variable."""
        return variable_formatter(template="{name} = {value};")

    @cached_property
    def call_data_dependent_preamble(
        self,
    ) -> Callable[[Value], tuple[str, ...]]:
        """Return data-dependent preamble lines for call rendering."""
        return self.data_dependent_preamble

    @cached_property
    def type_hint_collection_preamble_lines(
        self,
    ) -> Callable[[frozenset[type]], tuple[str, ...]]:
        """Return preamble lines for empty-collection type hints."""
        return no_type_hint_preamble

    @cached_property
    def format_call_stub(
        self,
    ) -> Callable[
        [Sequence[str], Sequence[str], StubReturn, Sequence[Value]],
        tuple[str, ...],
    ]:
        """Return stub declarations for a call expression."""
        return no_call_stub

    @cached_property
    def format_call_preamble_stub(
        self,
    ) -> Callable[
        [Sequence[str], Sequence[str], StubReturn, Sequence[Value]],
        tuple[str, ...],
    ]:
        """Return file-scope stubs for a call expression."""
        return _cpp_call_stub

    @cached_property
    def format_call_target(self) -> Callable[[Sequence[str]], str]:
        """Rewrite a dotted call target into the language's call
        syntax.
        """
        return identity_call_target

    @cached_property
    def format_call_ref_identifier(self) -> Callable[[str], str]:
        """Wrap a ``{"$ref": "name"}`` identifier in ``std::move()``.

        A direct copy assignment (``auto my_data = my_var``) triggers
        clang-tidy ``performance-unnecessary-copy-initialization`` when
        the variable is never modified.  Using ``std::move`` avoids the
        copy and satisfies the linter.
        """

        def _format_cpp_ref_identifier(name: str, /) -> str:
            """Wrap the identifier in ``std::move()``."""
            return f"std::move({name})"

        return _format_cpp_ref_identifier

    @cached_property
    def format_call_arg_ref_identifier(self) -> Callable[[str], str]:
        """Emit a call-argument ``$ref`` as the bare identifier.

        ``std::move`` would consume the variable, which is unsafe when
        the caller may use it again in a later call (or after the
        ``literalize_call`` block).  Callers opt in to consuming a
        specific ref by listing it in ``literalize_call``'s
        ``consumable_refs`` set; in that case
        :attr:`format_call_arg_ref_identifier_consumable` is used
        instead and emits ``std::move(name)``.
        """
        return identity_call_ref_identifier

    @cached_property
    def format_call_arg_ref_identifier_consumable(
        self,
    ) -> Callable[[str], str]:
        """Wrap a consumable call-argument ``$ref`` in ``std::move()``.

        Used only for refs the caller declared as consumable on
        :func:`~literalizer.literalize_call` and that appear in just
        one call argument, so the move cannot strand a later use.
        """

        def _format_cpp_ref_identifier_consumable(name: str, /) -> str:
            """Wrap the identifier in ``std::move()``."""
            return f"std::move({name})"

        return _format_cpp_ref_identifier_consumable

    @cached_property
    def consumable_ref_value_inhibits_consuming_form(
        self,
    ) -> Callable[[Value], bool]:
        """Predicate deciding whether a ref's underlying value type
        inhibits the consume form.

        Delegates to :data:`never_inhibits_consuming_form`.  ``std::move``
        is valid for every value type in this codebase.
        """
        return never_inhibits_consuming_form

    @cached_property
    def _cpp_date_type(self) -> str:
        """Resolved C++ type name for the chosen date format."""
        return self.date_format.cpp_type

    @cached_property
    def _cpp_datetime_type(self) -> str:
        """Resolved C++ type name for the chosen datetime format."""
        return self.datetime_format.cpp_type

    @cached_property
    def _type_ctx(self) -> _CppTypeCtx:
        """Context bundle for C++ type resolution."""
        return _CppTypeCtx(
            int_resolver=self.numeric_literal_suffix.int_resolver,
            date_type=self._cpp_date_type,
            datetime_type=self._cpp_datetime_type,
        )

    @cached_property
    def sequence_format_config(self) -> SequenceFormatConfig:
        """Configuration for the chosen sequence format."""
        return self.sequence_format.get_config(type_ctx=self._type_ctx)

    @cached_property
    def set_format_config(self) -> SetFormatConfig:
        """Configuration for the chosen set format."""
        return self.set_format.get_config(type_ctx=self._type_ctx)

    @cached_property
    def sequence_open(self) -> Callable[[list[Value]], str]:
        """Callable that returns the opening delimiter for a sequence."""
        return self.sequence_format_config.sequence_open

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
    def format_float(self) -> Callable[[float], str]:
        """Callable that formats a float value as a literal."""
        return self.float_format

    @cached_property
    def format_integer(self) -> Callable[[int], str]:
        """Callable that formats an int value as a literal."""
        base_int_formatter = self.integer_format.get_formatter(
            numeric_separator=self.numeric_separator,
        )
        return make_overflow_fallback_formatter(
            base=self.numeric_literal_suffix.wrap_integer_formatter(
                base=base_int_formatter,
            ),
            fallback=make_ull_fallback(language_name="C++"),
        )

    @cached_property
    def dict_format_config(self) -> DictFormatConfig:
        """Configuration for dict formatting."""
        return self.dict_format.get_config(type_ctx=self._type_ctx)

    @cached_property
    def comment_config(self) -> CommentConfig:
        """Configuration for the language's comment syntax."""
        return self.comment_format.value

    @cached_property
    def ordered_map_format_config(self) -> OrderedMapFormatConfig:
        """Configuration for ordered-map formatting."""
        return _build_ordered_map_config(type_ctx=self._type_ctx)

    @cached_property
    def format_ordered_map_entry(self) -> Callable[[str, Value, str], str]:
        """Callable that formats one ordered-map entry."""
        return braced_dict_entry(format_value=passthrough_sequence_entry)

    @cached_property
    def data_dependent_preamble(
        self,
    ) -> Callable[[Value], tuple[str, ...]]:
        """Build data-dependent preamble lines (variant and ``nullptr``
        headers).
        """
        return _build_variant_preamble(type_ctx=self._type_ctx)

    @cached_property
    def heterogeneous_behavior(self) -> HeterogeneousBehavior:
        """Return the heterogeneous-behavior config."""
        return self.heterogeneous_strategy.value

    @cached_property
    def format_variable_declaration(
        self,
    ) -> Callable[[str, str, Value, frozenset[enum.Enum]], str]:
        """Callable that formats a new variable declaration."""
        return self.declaration_style.value.formatter

    @cached_property
    def scalar_preamble(self) -> dict[type, tuple[str, ...]]:
        """Per-instance scalar preamble computed from date/datetime format."""
        return date_scalar_preamble(
            date_format=self.date_format,
            datetime_format=self.datetime_format,
            extra={
                str: ("#include <string>",),
                bytes: ("#include <string>",),
                type(None): ("#include <cstddef>",),
            },
        )

    @cached_property
    def scalar_body_preamble(self) -> dict[type, tuple[str, ...]]:
        """Per-instance scalar body preamble (C++ needs none)."""
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

    @cached_property
    def call_style_config(self) -> CallStyle:
        """Configuration for the chosen call style."""
        return self.call_style.value
