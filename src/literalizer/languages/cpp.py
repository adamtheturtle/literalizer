"""C++ language specification."""

import dataclasses
import datetime
import enum
from collections.abc import Callable, Mapping, Sequence
from functools import cached_property
from types import MappingProxyType
from typing import ClassVar

from beartype import beartype

from literalizer._formatters.collection_openers import (
    fixed_open,
    make_element_to_type,
)
from literalizer._formatters.format_dates import (
    format_date_iso,
    format_datetime_epoch,
    format_datetime_iso,
    format_time_iso,
)
from literalizer._formatters.format_entries import (
    braced_dict_entry,
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
    I64_MAX,
    I64_MIN,
    format_integer_binary,
    format_integer_hex,
    format_integer_octal_c_style,
    format_integer_tick,
    make_long_suffix_formatter,
    make_overflow_fallback_formatter,
    make_ull_fallback,
)
from literalizer._formatters.format_json_value import format_json_value_text
from literalizer._formatters.format_strings import format_string_backslash
from literalizer._formatters.record_strategy import (
    RecordDeclarationField,
    RecordFieldType,
    RecordLiteralField,
    RecordRenderer,
    RecordStrategy,
    build_record_strategy,
)
from literalizer._formatters.tuple_strategy import (
    collect_tuple_list_ids,
    is_tuple_eligible,
)
from literalizer._formatters.type_inference import (
    BeyondI64,
    DictType,
    ListType,
    WideInt,
    collect_record_shapes,
    infer_element_type,
    record_shape_for_dict,
)
from literalizer._heterogeneous import iter_wrapped_scalars
from literalizer._language import (
    NO_CALL_PARAMETER_LIMIT,
    NO_HETEROGENEOUS_BEHAVIOR,
    NON_KEBAB_REF_CASES,
    BareIntegerWidthStrategies,
    CallStyle,
    CommentConfig,
    DateFormatConfig,
    DatetimeFormatConfig,
    DictFormatConfig,
    FloatSpecialsMixin,
    HeterogeneousBehavior,
    IdentifierCase,
    JsonType,
    LanguageCls,
    ModifierCombination,
    NestedMapWideningVariant,
    OrderedMapFormatConfig,
    PositionalCallStyle,
    RecordVariant,
    RenderedRecordLiteral,
    RenderedTupleLiteral,
    SequenceFormatConfig,
    SetFormatConfig,
    StubReturn,
    TrailingCommaConfig,
    VariantMetadata,
    body_preamble_from_scalars,
    date_scalar_preamble,
    default_format_call_variable_assignment,
    default_format_call_variable_declaration,
    default_sequence_binding_declarations,
    default_wrap_calls_with_declarations,
    identity_call_arg,
    identity_call_ref_identifier,
    identity_call_statement,
    identity_call_target,
    identity_constructor_target,
    no_call_binding_body_preamble,
    no_call_binding_file_pragmas,
    no_call_stub,
    no_compute_call_slot_wrap_ids,
    no_compute_wrap_ids,
    no_data_preamble,
    no_format_integer_beyond_i64,
    no_format_integer_widened,
    no_leading_preamble,
    no_type_hint_preamble,
    no_validate_call_arg,
    prepend_body_preamble,
)
from literalizer._types import OrderedMap, Scalar, Value
from literalizer.exceptions import (
    IncompatibleFormatsError,
    UnrepresentableInputError,
)


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
    *values*: ``int`` when every value fits in 32 bits, ``long long``
    when every value fits in signed 64 bits, else
    ``unsigned long long``.  Empty inputs return ``"int"``.  ``long``
    is skipped because its width is platform-dependent (32-bit on
    Windows, 64-bit on Unix).
    """
    if not values:
        return "int"
    if any(not I64_MIN <= v <= I64_MAX for v in values):
        return "unsigned long long"
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
    if (
        element_type is int
        or element_type is WideInt
        or element_type is BeyondI64
    ):
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
        time_type="std::string",
        list_template="std::vector<{inner}>",
        enable_list_type=True,
        dict_type_template="std::map<std::string, {inner}>",
        fallback_value_type=None,
        wide_int_type=None,
        beyond_i64_type=None,
    )


@beartype
def _cpp_value_inhibits_consuming_form(value: Value, /) -> bool:
    """Return ``True`` when ``std::move`` is unhelpful for *value*'s C++
    type.

    The literalize-generated C++ maps Python ``bool`` / ``int`` /
    ``float`` to ``bool`` / a narrow integer / ``double``, all of which
    are register-trivial.  ``date`` and ``datetime`` map to
    ``std::chrono::year_month_day`` and
    ``std::chrono::system_clock::time_point``, both also
    register-trivial.  Strings, bytes, lists, and dicts allocate or own
    heap storage, so ``std::move`` continues to deliver value for those.
    """
    if isinstance(value, (list, dict, set)):
        return False
    return isinstance(value, (bool, int, float, datetime.date))


@dataclasses.dataclass(frozen=True)
class _CppTypeCtx:
    """Context for C++ type resolution with value-driven int narrowing.

    Bundles the date/datetime type strings (which are static) with an
    :data:`_IntTypeResolver` that picks the narrowest int type for a
    given collection of values.  Used wherever a type string is emitted
    so that the int type can be specialized per-collection.

    ``tuple_strategy`` is ``True`` under the ``TUPLE`` heterogeneous
    strategy: a tuple-eligible heterogeneous scalar array in a mapping
    value (the document root needs no opener type) is then typed
    ``std::tuple<T0, ...>`` instead of
    ``std::vector<std::variant<...>>``, matching the
    ``std::make_tuple`` literal the strategy renders.
    """

    int_resolver: _IntTypeResolver
    date_type: str | None
    datetime_type: str | None
    tuple_strategy: bool
    variant_type_name: str

    def variant_type(self, types: Sequence[str], /) -> str:
        """Return the active heterogeneous-value carrier type."""
        return f"{self.variant_type_name}<{', '.join(types)}>"

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
        if not items:
            return "std::array<std::nullptr_t, 0>{"
        int_type = type_ctx.int_resolver(
            [
                item
                for item in items
                if isinstance(item, int) and not isinstance(item, bool)
            ],
        )
        element_to_type = type_ctx.element_to_type(int_type=int_type)
        type_name = element_to_type(type(items[0]))
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


@beartype
def _identity_wrapper(
    base: Callable[[int], str],
) -> Callable[[int], str]:
    """Return the formatter unchanged."""
    return base


@beartype
def _cpp_tuple_element_type(
    *,
    value: Value,
    type_ctx: _CppTypeCtx,
) -> str:
    """Return the C++ type for one tuple element.

    Tuple-eligible arrays are all-scalar (see
    :func:`~literalizer._formatters.tuple_strategy.is_tuple_eligible`),
    so *value* is always a scalar; each element's int width is narrowed
    to its own value so the declared type matches the
    ``std::make_tuple`` literal, whose integer arguments carry no width
    suffix.
    """
    if isinstance(value, int) and not isinstance(value, bool):
        int_type = type_ctx.int_resolver([value])
    else:
        int_type = "long long"
    element_to_type = type_ctx.element_to_type(int_type=int_type)
    return _compute_cpp_type(
        item=value,
        element_to_type=element_to_type,
        type_ctx=type_ctx,
        in_mapping_value=False,
    )


@beartype
def _cpp_tuple_type(
    *,
    items: list[Value],
    type_ctx: _CppTypeCtx,
) -> str:
    """Return ``std::tuple<T0, T1, ...>`` for a tuple-eligible array."""
    element_types = [
        _cpp_tuple_element_type(value=element, type_ctx=type_ctx)
        for element in items
    ]
    return f"std::tuple<{', '.join(element_types)}>"


@beartype
def _compute_cpp_type(  # noqa: PLR0911
    *,
    item: Value,
    element_to_type: Callable[[type | ListType | DictType], str | None],
    type_ctx: _CppTypeCtx,
    in_mapping_value: bool,
) -> str:
    """Return the C++ type string for a single value.

    *element_to_type* must have the int type already narrowed for the
    enclosing collection's variant arm (or homogeneous leaf).  When the
    value is a sub-collection, recursion re-narrows independently via
    *type_ctx*.  *in_mapping_value* is ``True`` when *item* is a dict /
    ordered-map value: a tuple-eligible heterogeneous scalar array in
    that position is typed ``std::tuple<...>`` under the ``TUPLE``
    strategy (the same lists :func:`collect_tuple_list_ids` marks,
    which are dict values or the document root, never list elements).
    """
    match item:
        case OrderedMap():
            omap_values = item.values()
            values: list[Value] = list(omap_values)
            value_type = _compute_element_type_for_items(
                items=values,
                type_ctx=type_ctx,
                in_mapping_value=True,
            )
            return f"std::vector<std::pair<std::string, {value_type}>>"
        case dict():
            values = list(item.values())
            value_type = _compute_element_type_for_items(
                items=values,
                type_ctx=type_ctx,
                in_mapping_value=True,
            )
            return f"std::map<std::string, {value_type}>"
        case list() if (
            in_mapping_value
            and type_ctx.tuple_strategy
            and is_tuple_eligible(value=item)
        ):
            return _cpp_tuple_type(items=item, type_ctx=type_ctx)
        case list():
            inner_type = _compute_element_type_for_items(
                items=item,
                type_ctx=type_ctx,
                in_mapping_value=False,
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
                in_mapping_value=False,
            )
            return f"std::vector<{inner_type}>"
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
    in_mapping_value: bool,
) -> list[str]:
    """Collect unique C++ type names for each item, preserving order."""
    unique_cpp_types: list[str] = []
    seen: set[str] = set()
    for item in items:
        item_type = _compute_cpp_type(
            item=item,
            element_to_type=element_to_type,
            type_ctx=type_ctx,
            in_mapping_value=in_mapping_value,
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
    in_mapping_value: bool,
) -> str:
    """Return the C++ element type for a collection of items.

    Returns a single type name when all items have the same C++ type,
    or ``std::variant<T1, T2, ...>`` for mixed types.  Returns
    ``std::nullptr_t`` for empty collections.  Narrows int-valued leaves
    to the narrowest C++ int type that holds the actual values.

    When *in_mapping_value* is set under the ``TUPLE`` strategy and any
    item is a tuple-eligible array, the homogeneous fast path is
    bypassed: each item is typed individually so a tuple-eligible array
    becomes ``std::tuple<...>`` (the fast path would otherwise widen a
    uniform list-of-arrays to ``std::vector<std::variant<...>>``).
    """
    if not items:
        return "std::nullptr_t"
    has_tuple_item = (
        in_mapping_value
        and type_ctx.tuple_strategy
        and any(
            isinstance(item, list) and is_tuple_eligible(value=item)
            for item in items
        )
    )
    element_type = None if has_tuple_item else infer_element_type(items=items)
    if element_type is not None:
        match element_type:
            case DictType(value_type=None, values=dict_values):
                value_type = _compute_element_type_for_items(
                    items=list(dict_values),
                    type_ctx=type_ctx,
                    in_mapping_value=True,
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
        in_mapping_value=in_mapping_value,
    ):
        case [single]:
            return single
        case types:
            return type_ctx.variant_type(types)


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
    *,
    tuple_list_ids: frozenset[int] = frozenset(),
    record_dict_ids: frozenset[int] = frozenset(),
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
        case list():
            if id(data) in tuple_list_ids:
                return False
            return _items_need_variant(
                items=data,
                element_to_type=element_to_type,
            )
        case dict():
            if id(data) in record_dict_ids:
                # A record gives every field its own declared type.  Do
                # not mistake its mixed fields for a map value variant,
                # but keep walking so a genuinely dynamic nested field
                # still requests the carrier it needs.
                return any(
                    _needs_variant_type(
                        data=value,
                        element_to_type=element_to_type,
                        tuple_list_ids=tuple_list_ids,
                        record_dict_ids=record_dict_ids,
                    )
                    for value in data.values()
                )
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
        case list() | set() | dict() if not data:
            return True
        case list():
            return any(_has_empty_collection(data=v) for v in data)
        case dict():
            mapping_values = data.values()
            return any(_has_empty_collection(data=v) for v in mapping_values)
        case _:
            return False


@beartype
def _build_variant_preamble(
    *,
    type_ctx: _CppTypeCtx,
    tuple_list_ids: frozenset[int] = frozenset(),
    record_dict_ids: frozenset[int] = frozenset(),
) -> Callable[[Value], tuple[str, ...]]:
    """Build a data preamble for the active variant implementation."""
    element_to_type = type_ctx.element_to_type(int_type="long long")

    def _variant_preamble(data: Value, /) -> tuple[str, ...]:
        """Return headers required by variant/nullptr_t usage."""
        lines: list[str] = []
        if _has_empty_collection(data=data):
            lines.append("#include <cstddef>")
        if _needs_variant_type(
            data=data,
            element_to_type=element_to_type,
            tuple_list_ids=tuple_list_ids,
            record_dict_ids=record_dict_ids,
        ):
            if type_ctx.variant_type_name == "std::variant":
                lines.append("#include <variant>")
            else:
                lines.append(
                    "template <typename... Types> struct "
                    "LiteralizerVariant { "
                    "template <typename T> LiteralizerVariant(T) {} "
                    "// NOLINT(google-explicit-constructor,"
                    "hicpp-explicit-conversions)\n"
                    "};"
                )
        return tuple(lines)

    return _variant_preamble


@beartype
def _build_tuple_preamble(
    *,
    type_ctx: _CppTypeCtx,
) -> Callable[[Value], tuple[str, ...]]:
    """Build the ``TUPLE``-strategy ``data_dependent_preamble``.

    Composes the variant preamble and additionally emits
    ``#include <tuple>`` whenever the data carries any tuple-eligible
    heterogeneous scalar array.  The ``<tuple>`` line is emitted off
    :func:`collect_tuple_list_ids` alone, so it fires even when the
    data has no record-shaped dicts at all (e.g. a bare top-level
    heterogeneous array) -- C++ has no ``RECORD`` strategy, so this is
    the only thing that pulls in the tuple header.
    """

    def _tuple_preamble(data: Value, /) -> tuple[str, ...]:
        """Return the variant headers plus ``<tuple>`` when needed."""
        tuple_list_ids = collect_tuple_list_ids(data=data)
        variant_preamble = _build_variant_preamble(
            type_ctx=type_ctx,
            tuple_list_ids=(
                tuple_list_ids
                if type_ctx.variant_type_name == "LiteralizerVariant"
                else frozenset()
            ),
        )
        lines = list(variant_preamble(data))
        if tuple_list_ids:
            lines.append("#include <tuple>")
        return tuple(lines)

    return _tuple_preamble


@beartype
def _render_cpp_tuple(
    value: list[Value],
    elements: Sequence[str],
) -> RenderedTupleLiteral:
    """Render a heterogeneous scalar array as ``std::make_tuple(...)``.

    ``collect_tuple_list_ids`` only marks arrays spanning at least two
    scalar buckets, so the call always has at least two arguments.  The
    shared layout assembler joins *elements* into the compact
    ``std::make_tuple(a, b)`` or one-per-line multiline form; *value* is
    unused because every element arrives already formatted.
    """
    del value
    return RenderedTupleLiteral(
        head="std::make_tuple(",
        entries=tuple(elements),
        closer=")",
        compact_pad="",
        # ``std::make_tuple(a, b,)`` is a syntax error (function call,
        # not a braced initializer), so suppress the trailing comma the
        # language-wide config would otherwise add in multiline form.
        multiline_trailing_comma=False,
    )


@beartype
def _cpp_tuple_list_ids(data: Value, /) -> frozenset[int]:
    """Adapt :func:`collect_tuple_list_ids` to the positional
    ``compute_tuple_list_ids`` hook signature.
    """
    return collect_tuple_list_ids(data=data)


_CPP_TUPLE_BEHAVIOR = HeterogeneousBehavior(
    skip_scalar_checks=False,
    compute_wrap_ids=no_compute_wrap_ids,
    wrap_scalar=None,
    wrap_non_scalar=None,
    wrap_empty_container=None,
    compute_call_slot_wrap_ids=no_compute_call_slot_wrap_ids,
    dict_open_for_wrap_ids=None,
    widens_nested_maps_by_wrapping_scalars=False,
    widens_unrecordizable_nested_sibling_maps=False,
    render_record_literal=None,
    compute_record_shapes=None,
    render_tuple_literal=_render_cpp_tuple,
    compute_tuple_list_ids=_cpp_tuple_list_ids,
)
"""``TUPLE`` strategy behavior: render fixed-length heterogeneous
scalar arrays as ``std::make_tuple`` literals.

C++ already represents the carved-out scalar checks via
``std::variant`` (``skip_scalar_checks`` is irrelevant -- the
sequence/dict formats report ``supports_heterogeneity``), so this only
adds the tuple render hook and the list-id collector.  The ``RECORD``
strategy is wired separately on the language (its behavior needs the
per-instance type context), so the ``TUPLE`` behavior does not compose
a record behavior here.
"""


# The ``RECORD`` strategy generates a plain aggregate ``struct`` per
# distinct record shape.  clang-tidy's
# ``cppcoreguidelines-pro-type-member-init`` requires every scalar
# member to carry an in-class initializer, while
# ``readability-redundant-member-init`` rejects one on a class-type
# member (its default constructor already value-initializes it).  So a
# field type that is a fundamental scalar gets a ``{}`` brace-or-equal
# initializer and a class type (``std::string``, ``std::vector<...>``,
# ``std::chrono::...``, a nested ``RecordN``) gets none.  These are
# exactly the scalar type names :func:`_make_cpp_element_to_type`
# emits, plus ``std::nullptr_t`` (a fundamental type, so it also needs
# the initializer and the redundant-init check does not apply).
_CPP_SCALAR_FIELD_TYPES: frozenset[str] = frozenset(
    {
        "bool",
        "double",
        "int",
        "long",
        "long long",
        "unsigned long long",
        "std::nullptr_t",
    },
)

# The ``RECORD`` strategy supports only auto ``Record0``/``Record1``/...
# names (no ``record_shape_names``), so the shared renderer always gets
# an empty custom-name mapping.
_CPP_NO_RECORD_SHAPE_NAMES: Mapping[frozenset[str], str] = MappingProxyType(
    mapping={},
)
_CPP_RECORD_MAP_VALUE = "LiteralizerRecordValue"
_CPP_RECORD_MAP_TYPE = f"std::map<std::string, {_CPP_RECORD_MAP_VALUE}>"


@beartype
def _cpp_record_field_identifier(key: str, /) -> str:
    """Return the C++ ``struct`` member name for a dict *key*.

    C++ member identifiers are the dict keys verbatim (no case
    conversion), matching the designated-initializer literal form
    ``Record0{.id = 1, ...}``.
    """
    return key


@beartype
def _cpp_record_literal(
    name: str,
    fields: Sequence[RecordLiteralField],
    /,
) -> RenderedRecordLiteral:
    """Render a C++ designated-initializer ``Name{.field = value, ...}``
    literal as structured pieces for the shared compact/multiline
    layout code.

    C++20 designated initializers must appear in declaration order; the
    shared strategy iterates the shape's keys in document order for both
    the declaration and the literal, so the orders always agree.  A
    trailing comma after the last initializer is valid in a
    brace-enclosed initializer list (unlike the ``std::make_tuple``
    call the ``TUPLE`` strategy renders), so the language-wide
    trailing-comma config applies unchanged.
    """
    return RenderedRecordLiteral(
        head=f"{name}{{",
        entries=tuple(
            f".{field.identifier} = {field.formatted}" for field in fields
        ),
        closer="}",
        compact_pad="",
    )


@beartype
def _cpp_record_literal_positional(
    name: str,
    fields: Sequence[RecordLiteralField],
    /,
) -> RenderedRecordLiteral:
    """Render a pre-C++20 positional aggregate initializer.

    C++14 and C++17 do not support designated initializers.  The shared
    record strategy preserves document order for both declarations and
    literals, so positional aggregate initialization remains well-formed.
    """
    return RenderedRecordLiteral(
        head=f"{name}{{",
        entries=tuple(field.formatted for field in fields),
        closer="}",
        compact_pad="",
    )


@beartype
def _cpp_render_record_declaration(
    name: str,
    fields: Sequence[RecordDeclarationField],
    /,
) -> str:
    """Render a C++ aggregate ``struct Name { Type field{}; ... };``.

    A scalar field carries a ``{}`` in-class initializer so the
    aggregate satisfies clang-tidy's member-init check; a class-type
    field omits it (its default constructor already value-initializes
    it, which the redundant-init check would otherwise flag).
    """
    members = " ".join(
        f"{field.type_name} {field.identifier}"
        f"{'{}' if field.type_name in _CPP_SCALAR_FIELD_TYPES else ''};"
        for field in fields
    )
    return f"struct {name} {{ {members} }};"


@beartype
def _cpp_int_field_type(
    *,
    value: int,
    int_resolver: _IntTypeResolver,
) -> str:
    """Return the C++ field type for an integer record field.

    Mirrors the literal :attr:`Cpp.format_integer` emits: an integer
    inside signed 64-bit range follows the value-driven *int_resolver*
    (``int``/``long long``, or the suffix-forced ``long``), while a
    positive value beyond it is written with a ``ULL`` suffix by the
    overflow fallback and is therefore ``unsigned long long`` (a
    negative out-of-range value raises at format time, so that side is
    never reached).
    """
    if not I64_MIN <= value <= I64_MAX:
        return "unsigned long long"
    return int_resolver([value])


@beartype
def _all_record_shaped(items: list[Value], /) -> bool:
    """Return whether *items* is a non-empty list whose every element
    is a record-shaped dict (non-empty, all-string-keyed, not an
    ordered map).

    Under the ``RECORD`` strategy such a list renders each element as a
    generated ``RecordN`` literal, so the C++ sequence opener widens to
    a ``std::vector`` whose element type is deduced from those literals
    (class-template argument deduction) rather than the homogeneous-map
    type the variant opener would otherwise emit.

    Uniformity of shape need not be checked here: a sibling list whose
    record-shaped dicts do not all share one shape is rejected for
    every ``RECORD`` language by the shared
    :func:`literalizer._checks.check_data` guard
    (:class:`~literalizer.exceptions.HeterogeneousSiblingListsError`)
    before any value is formatted, so a list reaching this predicate is
    always single-shape and the deduced ``std::vector<RecordN>`` is
    well-formed.
    """
    if not items:
        return False
    return all(
        isinstance(item, dict)
        and not isinstance(item, OrderedMap)
        and record_shape_for_dict(value=item) is not None
        for item in items
    )


@beartype
def _build_cpp_record_preamble(
    *,
    type_ctx: _CppTypeCtx,
    record_preamble: Callable[[Value], tuple[str, ...]],
    compute_wrap_ids: Callable[[Value], frozenset[int]],
    include_tuple_header: bool = False,
) -> Callable[[Value], tuple[str, ...]]:
    """Build the ``RECORD``-strategy ``data_dependent_preamble``.

    Composes the ``std::variant`` / ``std::nullptr_t`` header lines (a
    record field may still be a heterogeneous list or an empty
    collection) followed by the generated ``struct`` declarations.  The
    headers precede the declarations so a declared field may name
    ``std::nullptr_t`` or ``std::variant``; the scalar/sequence headers
    (``<string>``, ``<vector>``, ``<chrono>``) are emitted earlier
    still, by the type-driven preamble the core assembles before this
    one.
    """

    def _record_pre(data: Value, /) -> tuple[str, ...]:
        """Return the ``std::variant`` / ``std::nullptr_t`` headers plus
        the ``struct`` declarations.
        """
        wrap_ids = compute_wrap_ids(data)
        # Do not re-run the record strategy's shape computation here: its
        # render-time cache already holds the field requests that the
        # declaration preamble consumes.  The raw shape walk is enough to
        # distinguish individual struct fields from map values.
        record_dict_ids: frozenset[int] = (
            frozenset(collect_record_shapes(data=data))
            if type_ctx.variant_type_name == "LiteralizerVariant"
            else frozenset()
        )
        tuple_list_ids = collect_tuple_list_ids(data=data)
        variant_preamble = _build_variant_preamble(
            type_ctx=type_ctx,
            tuple_list_ids=(
                tuple_list_ids
                if type_ctx.variant_type_name == "LiteralizerVariant"
                else frozenset()
            ),
            record_dict_ids=record_dict_ids,
        )
        value_alias: tuple[str, ...] = ()
        headers = list(variant_preamble(data))
        if include_tuple_header and tuple_list_ids:
            headers.append("#include <tuple>")
        if wrap_ids:
            value_type = _compute_element_type_for_items(
                items=list(iter_wrapped_scalars(data=data, wrap_ids=wrap_ids)),
                type_ctx=type_ctx,
                in_mapping_value=True,
            )
            value_alias = (f"using {_CPP_RECORD_MAP_VALUE} = {value_type};",)
        return (*headers, *value_alias, *record_preamble(data))

    return _record_pre


@beartype
def _apply_cpp_variant_sequence_open(
    *,
    items: list[Value],
    type_ctx: _CppTypeCtx,
) -> str:
    """Return a typed ``std::vector`` opener."""
    inner = _compute_element_type_for_items(
        items=items,
        type_ctx=type_ctx,
        in_mapping_value=False,
    )
    return f"std::vector<{inner}>{{"


@beartype
def _apply_cpp_variant_dict_open(
    *,
    items: dict[Scalar, Value],
    type_ctx: _CppTypeCtx,
    opener_template: str,
) -> str:
    """Return a typed ``std::map`` or ``std::unordered_map`` opener."""
    value_type = _compute_element_type_for_items(
        items=list(items.values()),
        type_ctx=type_ctx,
        in_mapping_value=True,
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
    """Return a typed, owning ``std::vector`` opener."""
    inner = _compute_element_type_for_items(
        items=items,
        type_ctx=type_ctx,
        in_mapping_value=False,
    )
    return f"std::vector<{inner}>{{"


@beartype
def _apply_cpp_variant_ordered_map_open(
    *,
    data: dict[Scalar, Value],
    type_ctx: _CppTypeCtx,
) -> str:
    """Return a typed ordered-map opener."""
    values: list[Value] = list(data.values())
    value_type = _compute_element_type_for_items(
        items=values,
        type_ctx=type_ctx,
        in_mapping_value=True,
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
) -> Callable[[dict[Scalar, Value]], str]:
    """Build a dict opener that uses ``std::variant`` for
    heterogeneous dict values.
    """

    def _open(items: dict[Scalar, Value]) -> str:
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
    """Build a set opener that uses a typed, owning ``std::vector``."""

    def _open(items: list[Value]) -> str:
        """Delegate to module-level implementation."""
        return _apply_cpp_variant_set_open(items=items, type_ctx=type_ctx)

    return _open


@beartype
def _build_variant_ordered_map_open(
    *,
    type_ctx: _CppTypeCtx,
) -> Callable[[dict[Scalar, Value]], str]:
    """Build an ordered-map opener that uses
    ``std::vector<std::pair<...>>``.
    """

    def _open(data: dict[Scalar, Value]) -> str:
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


@dataclasses.dataclass(frozen=True)
class _CppDeclarationStyleConfig:
    """Configuration for a Cpp declaration style.

    Unlike :class:`DeclarationStyleConfig`, this carries no
    ``formatter`` slot: Cpp builds its declaration formatter
    per-instance in :attr:`Cpp.format_variable_declaration` so it can
    close over the chosen date/datetime ``type_produced``.
    """

    supports_redefinition: bool


@beartype
def _format_variable_declaration(
    *,
    name: str,
    value: str,
    data: Value,
    modifiers: frozenset[enum.Enum],
    date_type: type,
    datetime_type: type,
) -> str:
    """Format a C++ variable declaration.

    * ``const auto*`` — string literal (``"..."``), required by
      ``readability-qualified-auto``.  Driven by the parsed *data*
      together with the chosen date/datetime ``type_produced``: bytes
      and strings always render as quoted strings, and dates/datetimes
      do so when their format produces a :class:`str`.
    * ``auto`` — typed expression (e.g. ``std::vector<int>{...}``).

    When *modifiers* is non-empty, applicable modifier keywords
    (``static``, ``const``) are prepended.  ``const`` is not duplicated
    against the built-in ``const auto*`` for string literals.
    """
    if _renders_as_string_literal(
        data=data,
        date_type=date_type,
        datetime_type=datetime_type,
    ):
        type_keyword = "const auto*"
        extra = modifiers - {_CppModifiers.CONST}
    else:
        type_keyword = "auto"
        extra = modifiers
    prefix = _cpp_modifier_prefix(modifiers=extra)
    return f"{prefix}{type_keyword} {name} = {value};"


@beartype
def _renders_as_string_literal(
    *,
    data: Value,
    date_type: type,
    datetime_type: type,
) -> bool:
    """Return whether *data* renders as a C string literal.

    ``bytes`` and ``str`` always render as quoted strings in C++.
    ``datetime.datetime`` and ``datetime.date`` do so only when their
    format's ``type_produced`` is :class:`str` (the ISO variants);
    other variants render as ``std::chrono`` or numeric expressions.
    """
    match data:
        case bytes() | str():
            return True
        case datetime.datetime():
            return datetime_type is str
        case datetime.date():
            return date_type is str
        case _:
            return False


@beartype
def _cpp_call_stub(
    parts: Sequence[str],
    _params: Sequence[str],
    stub_return: StubReturn,
    _args: Sequence[Value],
    /,
    *,
    supports_abbreviated_templates: bool,
    supports_nodiscard: bool,
) -> tuple[str, ...]:
    """Return C++ stub declarations for a call name."""
    if supports_abbreviated_templates:
        parameter_pack = "auto..."
        template_prefix = ""
    else:
        parameter_pack = "Args..."
        template_prefix = "template <typename... Args> "
    nodiscard_prefix = "[[nodiscard]] " if supports_nodiscard else ""
    if len(parts) == 1:
        return (
            f"{template_prefix}auto {parts[0]}({parameter_pack}) "
            "{ return 0; }",
        )
    root = parts[0]
    method = parts[-1]
    fields = parts[1:-1]
    if not fields:
        type_name = f"{root}Type_"
        if stub_return is StubReturn.VOID:
            method_decl = (
                f"{template_prefix}void {method}({parameter_pack}) const {{}}"
            )
        else:
            method_decl = (
                f"{template_prefix}{nodiscard_prefix}auto {method}"
                f"({parameter_pack}) const {{ return 0; }}"
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
            f" {template_prefix}{nodiscard_prefix}auto {method}"
            f"({parameter_pack}) const"
            f" {{ return 0; }} }};"
        )
    else:
        lines.append(
            f"struct {inner_type} {{ {template_prefix}void {method}"
            f"({parameter_pack}) const {{}} }};"
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


_NLOHMANN_JSON_STATIC_PREAMBLE: tuple[str, ...] = (
    "#include <nlohmann/json.hpp>",
)

# C++ raw-string delimiter used to wrap the inline JSON document for
# ``nlohmann::json::parse``.  The lexer terminates the raw string at the
# first byte sequence ``)json"``; :func:`json.dumps` always escapes ``"``
# inside string literals as ``\"``, so the rendered JSON cannot contain
# the terminator unless the source data itself encodes the literal
# sequence ``)json"`` (e.g. through a Unicode escape).  The defensive
# check in :func:`_nlohmann_json_expression` rejects such inputs.
_NLOHMANN_JSON_DELIM = "json"
_NLOHMANN_JSON_RAW_TERMINATOR = f'){_NLOHMANN_JSON_DELIM}"'


_NLOHMANN_JSON_SEQUENCE_CONFIG = SequenceFormatConfig(
    sequence_open=fixed_open(open_str="["),
    close="]",
    supports_heterogeneity=True,
    single_element_trailing_comma=False,
    supports_trailing_comma=True,
    empty_sequence="[]",
    preamble_lines=(),
    format_entry=passthrough_sequence_entry,
    typed_opener_fallback=None,
    uses_typed_literal_for_scalars=False,
    requires_uniform_record_shapes=False,
    declared_type=None,
    narrowed_empty_form=None,
)


_NLOHMANN_JSON_SET_CONFIG = SetFormatConfig(
    set_open=fixed_open(open_str="["),
    close="]",
    empty_set="[]",
    preamble_lines=(),
    set_opener_template="",
    supports_heterogeneity=True,
    supports_trailing_comma=True,
)


_NLOHMANN_JSON_DICT_CONFIG = DictFormatConfig(
    dict_open=fixed_open(open_str="{"),
    close="}",
    format_entry=dict_entry_with_template(
        template="{key}: {value}",
        format_value=passthrough_sequence_entry,
    ),
    empty_dict="{}",
    preamble_lines=(),
    narrowed_open=None,
    supports_trailing_comma=True,
    narrowed_empty_form=None,
)


_NLOHMANN_JSON_ORDERED_MAP_CONFIG = OrderedMapFormatConfig(
    ordered_map_open=fixed_open(open_str="{"),
    close="}",
    preamble_lines=(),
)


@beartype
def _nlohmann_json_expression(data: Value) -> str:
    """Render a ``nlohmann::json::parse(...)`` expression for *data*.

    The framework's rendered ``value`` string is discarded in favor of a
    fresh :func:`json.dumps` of the raw data, so heterogeneous
    collections, ``OrderedMap`` values, sets, bytes and temporal values
    all fold into one shared JSON document.  The raw-string delimiter is
    chosen so the JSON encoding cannot terminate the literal early; if a
    pathological input still encodes the terminator sequence the
    rejection raised below keeps the emitted source well-formed.

    The trailing ``allow_exceptions=false`` argument disables
    ``parse``'s default throw-on-error behavior so the generated
    ``main`` is not made throwing by the parse call (which
    ``clang-tidy``'s ``bugprone-exception-escape`` would reject).  The
    rendered JSON is always well-formed by construction, so the
    discarded-error path is unreachable from valid input.
    """
    json_text = format_json_value_text(data=data)
    if _NLOHMANN_JSON_RAW_TERMINATOR in json_text:
        msg = (
            "Cpp(json_type=NLOHMANN_JSON) cannot represent a value whose "
            "JSON encoding contains the raw-string terminator "
            f"sequence {_NLOHMANN_JSON_RAW_TERMINATOR!r}."
        )
        raise UnrepresentableInputError(msg)
    return (
        f'nlohmann::json::parse(R"{_NLOHMANN_JSON_DELIM}'
        f'({json_text}){_NLOHMANN_JSON_DELIM}", nullptr, false)'
    )


@beartype
def _format_cpp_json_call_arg(raw_value: Value, _formatted: str) -> str:
    """Format a direct call argument as ``nlohmann::json::parse(...)``."""
    return _nlohmann_json_expression(data=raw_value)


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

        json_type: When set to ``json_types.NLOHMANN_JSON``, render values
            through ``nlohmann::json::parse`` over an inline JSON document
            instead of C++'s narrow ``std::vector`` / ``std::map`` /
            ``std::unordered_map`` collection types.  Dict keys must be
            strings so they remain valid JSON object keys.
    """

    format_integer_widened = no_format_integer_widened
    format_integer_beyond_i64 = no_format_integer_beyond_i64
    format_constructor_target: ClassVar["staticmethod[[str], str]"] = (
        staticmethod(identity_constructor_target)
    )
    format_call_variable_declaration = default_format_call_variable_declaration
    format_call_variable_assignment = default_format_call_variable_assignment
    sequence_binding_declarations = default_sequence_binding_declarations
    format_call_binding_body_preamble = no_call_binding_body_preamble
    format_call_binding_file_pragmas = no_call_binding_file_pragmas

    module_name: str = "Module"

    leading_preamble = no_leading_preamble
    extension = ".cpp"
    pygments_name = "cpp"
    supports_special_floats = True
    supports_variable_names = True
    supports_no_variable_wrap_in_file = False
    dict_supports_heterogeneous_values = True
    supports_dotted_calls = True
    has_free_function_calls = True
    reserved_identifiers: ClassVar[frozenset[str]] = frozenset()
    reserved_variable_identifiers_case_sensitive: bool = True
    reserved_variable_identifiers: frozenset[str] = frozenset(
        {
            "alignas",
            "alignof",
            "and",
            "and_eq",
            "asm",
            "auto",
            "bitand",
            "bitor",
            "bool",
            "break",
            "case",
            "catch",
            "char",
            "char16_t",
            "char32_t",
            "char8_t",
            "class",
            "co_await",
            "co_return",
            "co_yield",
            "compl",
            "concept",
            "const",
            "const_cast",
            "consteval",
            "constexpr",
            "constinit",
            "continue",
            "decltype",
            "default",
            "delete",
            "do",
            "double",
            "dynamic_cast",
            "else",
            "enum",
            "explicit",
            "export",
            "extern",
            "false",
            "float",
            "for",
            "friend",
            "goto",
            "if",
            "inline",
            "int",
            "long",
            "mutable",
            "namespace",
            "new",
            "noexcept",
            "not",
            "not_eq",
            "nullptr",
            "operator",
            "or",
            "or_eq",
            "private",
            "protected",
            "public",
            "reflexpr",
            "register",
            "reinterpret_cast",
            "requires",
            "return",
            "short",
            "signed",
            "sizeof",
            "static",
            "static_assert",
            "static_cast",
            "struct",
            "switch",
            "template",
            "this",
            "thread_local",
            "throw",
            "true",
            "try",
            "typedef",
            "typeid",
            "typename",
            "union",
            "unsigned",
            "using",
            "virtual",
            "void",
            "volatile",
            "wchar_t",
            "while",
            "xor",
            "xor_eq",
        }
    )
    allows_empty_call_parens = True
    supports_dotted_call_stub = True
    call_returns_expression = True
    supports_json_call_result_binding = False
    supports_zero_parameter_calls = True
    max_call_parameters = NO_CALL_PARAMETER_LIMIT
    supports_inline_multiline_dict_args = True
    supports_standalone_comments_in_wrapped_calls = True
    supports_multi_param_call_wrapper_stub = True
    supports_dict_literal_as_free_expression = True
    supports_module_name = True
    supports_empty_dict_key = False
    supports_call_style = True
    supports_default_dict_key_type = False
    supports_default_dict_value_type = False
    supports_default_sequence_element_type = False
    supports_default_set_element_type = False
    supports_default_ordered_map_value_type = False
    non_default_kwargs: ClassVar[dict[str, str]] = {}
    declaration_style_sequence_format_overrides: ClassVar[dict[str, str]] = {}
    json_type_variant_name_suffix: ClassVar[str | None] = None
    supports_non_ascii_string_literals = True
    variant_metadata: ClassVar[VariantMetadata] = VariantMetadata(
        string_literals_escape_null_byte=False,
        pre_indent_comment_scalar_variant=True,
        fixture_module_name_template=None,
        fixture_module_name_lowercase=False,
        golden_filename_lowercase=False,
        collection_layout_category="collection_layout",
        record_variants=frozenset({RecordVariant.FIELD_TYPE_SPLIT}),
        nested_map_widening=NestedMapWideningVariant.NONE,
        modifier_sequence_format_overrides={},
    )
    supports_record_struct_name_prefix = True
    supports_record_shape_names = False
    supports_non_string_dict_keys = False

    class DateFormats(enum.Enum):
        """Date format options for C++."""

        CPP = DateFormatConfig(
            formatter=_format_date_cpp,
            preamble_lines=("#include <chrono>",),
            type_produced=datetime.date,
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
            type_produced=datetime.datetime,
        )
        ISO = DatetimeFormatConfig(
            formatter=format_datetime_iso,
            preamble_lines=("#include <string>",),
            type_produced=str,
        )

        EPOCH = DatetimeFormatConfig(
            formatter=format_datetime_epoch,
            type_produced=int,
            preamble_lines=(),
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
            preamble_lines=("#include <vector>",),
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

        AUTO = _CppDeclarationStyleConfig(supports_redefinition=True)

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
                narrowed_empty_form=None,
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
                narrowed_empty_form=None,
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
        """Heterogeneous-scalar strategy options.

        C++ represents heterogeneous scalar collections with
        ``std::variant`` by default (``ERROR``); ``TUPLE`` additionally
        renders a fixed-length heterogeneous scalar array (a dict value
        or the document root, all elements scalar, spanning at least two
        scalar buckets) as ``std::make_tuple(...)`` typed
        ``std::tuple<...>``.  ``RECORD`` instead renders each
        record-shaped dict (non-empty, string-keyed) as a generated
        aggregate ``struct`` declared in the preamble plus a matching
        ``Record0{.field = value, ...}`` designated-initializer literal,
        so fields may mix scalars and containers that the homogeneous
        ``std::map`` cannot.
        """

        ERROR = enum.auto()
        TUPLE = enum.auto()
        RECORD = enum.auto()

    heterogeneous_strategies = HeterogeneousStrategies

    class BoolFormats(enum.Enum):
        """Empty: this language has no alternative boolean formats."""

    bool_formats = BoolFormats

    class VersionFormats(enum.Enum):
        """C++ language-standard targets.

        Select one with :attr:`Cpp.language_version`, for example
        ``Cpp(language_version=Cpp.version_formats.CPP17)``.  The
        default is :attr:`CPP20`.
        """

        CPP14 = enum.auto()
        """ISO C++14 (``-std=c++14``).

        Uses a local value carrier in place of ``std::variant``, positional
        aggregate initialization, ISO date/datetime strings, and explicit
        template parameter packs in generated call stubs.
        """

        CPP17 = enum.auto()
        """ISO C++17 (``-std=c++17``).

        Uses ``std::variant`` while retaining positional aggregate
        initialization, ISO date/datetime strings, and explicit template
        parameter packs in generated call stubs.
        """

        CPP20 = enum.auto()
        """ISO C++20 (``-std=c++20``; default)."""

    version_formats = VersionFormats

    class JsonTypes(JsonType):
        """JSON value type options for C++."""

        NLOHMANN_JSON = "nlohmann::json"
        """The ``nlohmann::json`` dynamic JSON value type from the
        ``nlohmann/json.hpp`` library.
        """

    json_types = JsonTypes

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

    def __post_init__(self) -> None:
        """Reject ``json_type`` combinations the generator cannot emit."""
        self._validate_json_type_spec()

    def _validate_json_type_spec(self) -> None:
        """Reject ``json_type`` combinations the generator cannot emit.

        Under ``json_type`` the rendered data flows through a single
        ``nlohmann::json::parse`` call.  That is incompatible with the
        ``RECORD`` and ``TUPLE`` heterogeneous strategies, both of
        which generate type declarations (``struct``s for ``RECORD``,
        ``std::tuple<...>`` aliases for ``TUPLE``) that the json_type
        renderer would silently drop on the floor.
        """
        if not self._json_type_active:
            return
        rejected = {
            self.heterogeneous_strategies.RECORD: "struct",
            self.heterogeneous_strategies.TUPLE: "std::tuple<...>",
        }
        if self.heterogeneous_strategy in rejected:
            strategy_name = self.heterogeneous_strategy.name
            generated = rejected[self.heterogeneous_strategy]
            msg = (
                "Cpp json_type renders data through "
                "nlohmann::json::parse(...) and is incompatible with "
                f"heterogeneous_strategy={strategy_name}, which generates "
                f"{generated} declarations. Use "
                "heterogeneous_strategy=ERROR."
            )
            raise IncompatibleFormatsError(msg)

    def validate_spec_for_data(self, data: Value) -> None:
        """Validate C++-specific data/format combinations."""
        if self._json_type_active:
            self._validate_json_value_keys(data=data)

    def _validate_json_value_keys(self, *, data: Value) -> None:
        """Reject non-string object keys for ``nlohmann::json``.

        ``OrderedMap`` is a subclass of :class:`dict`, so the ``dict``
        arm covers it as well.
        """
        match data:
            case dict():
                for key, value in data.items():
                    if not isinstance(key, str):
                        msg = (
                            "Cpp json_type can only represent dict keys "
                            "as JSON object strings, not "
                            f"{type(key).__name__}"
                        )
                        raise UnrepresentableInputError(msg)
                    self._validate_json_value_keys(data=value)
            case list() | set():
                for item in data:
                    self._validate_json_value_keys(data=item)
            case _:
                return

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
    integer_width_strategies = BareIntegerWidthStrategies
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

        POSITIONAL = PositionalCallStyle(
            arg_separator=", ", parenthesize_each_arg=False
        )

    call_styles = CallStyles

    def wrap_in_file(
        self,
        content: str,
        variable_name: str,
        body_preamble: tuple[str, ...],
    ) -> str:
        """Wrap a C++ declaration in a main function.

        Under :attr:`json_type` the body is additionally wrapped in
        ``try { ... } catch (...) { return 1; }`` so the
        potentially-throwing ``nlohmann::json::parse`` call cannot make
        ``main`` itself throwing — clang-tidy's
        ``bugprone-exception-escape`` check rejects an implicitly
        ``noexcept`` ``main`` that calls a function whose signature
        permits exceptions, even when the runtime flag
        ``allow_exceptions=false`` has been passed to suppress them.
        """
        content = prepend_body_preamble(
            content=content,
            body_preamble=body_preamble,
        )
        use_line = (
            f"\n{self.indent}(void){variable_name};" if variable_name else ""
        )
        if self._json_type_active:
            return (
                f"int {self.module_name}() {{\n"
                f"{self.indent}try {{\n{content}{use_line}\n"
                f"{self.indent}{self.indent}return 0;\n"
                f"{self.indent}}} catch (...) {{\n"
                f"{self.indent}{self.indent}return 1;\n"
                f"{self.indent}}}\n}}"
            )
        return (
            f"int {self.module_name}() {{\n{content}{use_line}\n"
            f"{self.indent}return 0;\n}}"
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
    integer_width_strategy: BareIntegerWidthStrategies = (
        BareIntegerWidthStrategies.BARE
    )
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
    json_type: JsonTypes | None = None
    record_struct_name_prefix: str = "Record"
    # C++20 is the default checked by CI (see ``.github/workflows/lint.yml``).
    # Earlier standards remain available through ``VersionFormats``.
    language_version: VersionFormats = VersionFormats.CPP20
    indent: str = "    "

    _default_null_literal: ClassVar[str] = "nullptr"
    true_literal: ClassVar[str] = "true"
    false_literal: ClassVar[str] = "false"
    indent_closing_delimiter: ClassVar[bool] = False
    element_separator: ClassVar[str] = ", "
    skip_null_dict_values: ClassVar[bool] = False
    supports_collection_comments: ClassVar[bool] = True
    supports_scalar_before_comments: ClassVar[bool] = True
    supports_scalar_inline_comments: ClassVar[bool] = False
    statement_terminator: ClassVar[str] = ";"
    _default_static_preamble: ClassVar[Sequence[str]] = (
        "#include <initializer_list>",
    )
    static_body_preamble: ClassVar[Sequence[str]] = ()
    special_float_preamble: ClassVar[tuple[str, ...]] = ("#include <cmath>",)

    @cached_property
    def _json_type_active(self) -> bool:
        """Return whether C++ should render via ``nlohmann::json``."""
        return self.json_type is not None

    @cached_property
    def null_literal(self) -> str:
        """Null literal for the active C++ representation."""
        if self._json_type_active:
            return "null"
        return self._default_null_literal

    @cached_property
    def static_preamble(self) -> Sequence[str]:
        """Static preamble lines emitted once per file.

        Under :attr:`json_type` the ``nlohmann/json.hpp`` header replaces
        the default ``<initializer_list>`` include because every emitted
        expression goes through :func:`nlohmann::json::parse`.
        """
        if self._json_type_active:
            return _NLOHMANN_JSON_STATIC_PREAMBLE
        return self._default_static_preamble

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
        if self._json_type_active:

            def _formatter(name: str, _value: str, data: Value) -> str:
                """Assign a parsed JSON literal to an existing C++ binding."""
                expr = _nlohmann_json_expression(data=data)
                return f"{name} = {expr};"

            return _formatter
        return variable_formatter(template="{name} = {value};")

    @cached_property
    def format_call_arg(self) -> Callable[[Value, str], str]:
        """Callable that rewrites a formatted direct call argument."""
        if self._json_type_active:
            return _format_cpp_json_call_arg
        return identity_call_arg

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

        def _formatter(
            parts: Sequence[str],
            params: Sequence[str],
            stub_return: StubReturn,
            args: Sequence[Value],
        ) -> tuple[str, ...]:
            """Render a stub in the selected C++ language mode."""
            return _cpp_call_stub(
                parts,
                params,
                stub_return,
                args,
                supports_abbreviated_templates=self._uses_cpp20,
                supports_nodiscard=(
                    self.language_version
                    in (
                        self.version_formats.CPP17,
                        self.version_formats.CPP20,
                    )
                ),
            )

        return _formatter

    @cached_property
    def format_call_target(self) -> Callable[[Sequence[str]], str]:
        """Rewrite a dotted call target into the language's call
        syntax.
        """
        return identity_call_target

    @cached_property
    def format_call_ref_identifier(
        self,
    ) -> Callable[[str, Value | None], str]:
        """Wrap a ``{"$ref": "name"}`` identifier in ``std::move()``,
        except for ``trivially-copyable`` scalars.

        A direct copy assignment (``auto my_data = my_var``) triggers
        clang-tidy ``performance-unnecessary-copy-initialization`` when
        the variable is never modified, so ``std::move`` is used for
        container-typed refs to satisfy the linter.  Applying
        ``std::move`` to a ``trivially-copyable`` scalar (``int``, ``bool``,
        ``float``) is itself a clang-tidy
        ``hicpp-move-const-arg`` / ``performance-move-const-arg``
        warning ("has no effect; remove std::move()"), so we drop the
        wrapper when the caller's ``ref_values`` identifies the ref as
        one of those types.  When the value is unknown we keep the
        historical ``std::move`` form.
        """

        def _format_cpp_ref_identifier(
            name: str, value: Value | None, /
        ) -> str:
            """Wrap the identifier in ``std::move()`` unless *value* is
            a ``trivially-copyable`` scalar.
            """
            if isinstance(value, bool | int | float):
                return name
            return f"std::move({name})"

        return _format_cpp_ref_identifier

    @cached_property
    def format_call_arg_ref_identifier(
        self,
    ) -> Callable[[str, Value | None], str]:
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
    ) -> Callable[[str, Value | None], str]:
        """Wrap a consumable call-argument ``$ref`` in ``std::move()``.

        Used only for refs the caller declared as consumable on
        :func:`~literalizer.literalize_call` and that appear in just
        one call argument, so the move cannot strand a later use.
        """

        def _format_cpp_ref_identifier_consumable(
            name: str, _value: Value | None, /
        ) -> str:
            """Wrap the identifier in ``std::move()``."""
            return f"std::move({name})"

        return _format_cpp_ref_identifier_consumable

    @cached_property
    def consumable_ref_value_inhibits_consuming_form(
        self,
    ) -> Callable[[Value], bool]:
        """Return ``True`` for ref values whose C++ type is register-
        trivial.

        ``clang-tidy``'s ``performance-move-const-arg`` rule (and the
        equivalent ``hicpp-move-const-arg``) reports ``std::move`` on a
        register-trivial value as an error: the move has no effect and
        the wrapping is wasteful.  The call site routes these refs
        through the non-consuming formatter so the emitted C++ compiles
        cleanly under ``--warnings-as-errors``.
        """
        return _cpp_value_inhibits_consuming_form

    @cached_property
    def _cpp_date_type(self) -> str:
        """Resolved C++ type name for the chosen date format."""
        return self._resolved_date_format.cpp_type

    @cached_property
    def _cpp_datetime_type(self) -> str:
        """Resolved C++ type name for the chosen datetime format."""
        return self._resolved_datetime_format.cpp_type

    @cached_property
    def _uses_cpp20(self) -> bool:
        """Return whether C++20-only syntax and chrono types are available."""
        return self.language_version is self.version_formats.CPP20

    @cached_property
    def _resolved_date_format(self) -> DateFormats:
        """Return the selected date representation for the target standard."""
        if not self._uses_cpp20 and self.date_format is self.date_formats.CPP:
            return self.date_formats.ISO
        return self.date_format

    @cached_property
    def _resolved_datetime_format(self) -> DatetimeFormats:
        """Return the selected datetime representation for the target."""
        if (
            not self._uses_cpp20
            and self.datetime_format is self.datetime_formats.CPP
        ):
            return self.datetime_formats.ISO
        return self.datetime_format

    @cached_property
    def _tuple_strategy_active(self) -> bool:
        """Return whether the ``TUPLE`` heterogeneous strategy is set."""
        return self.heterogeneous_strategy.name == "TUPLE"

    @cached_property
    def _record_strategy_active(self) -> bool:
        """Return whether the ``RECORD`` heterogeneous strategy is set."""
        return self.heterogeneous_strategy.name == "RECORD"

    @cached_property
    def _uses_cpp14_tuple_record_strategy(self) -> bool:
        """Return whether ``TUPLE`` should also render C++14 records."""
        return (
            self.language_version is self.version_formats.CPP14
            and self._tuple_strategy_active
        )

    def _cpp_record_field_type(self, request: RecordFieldType, /) -> str:
        """Return the C++ ``struct`` field type for a record field,
        derived structurally from the raw value.

        A field whose value is itself a nested record-shaped dict uses
        that record's generated name.  A field whose value is a list of
        record-shaped dicts (one shared shape) is typed
        ``std::vector<RecordN>`` to match the ``std::vector{`` opener's
        class-template argument deduction from the ``RecordN`` element
        literals (the same name the shared strategy resolves, the one
        piece unrecoverable from the raw value).  Every other value is
        typed by the same :func:`_compute_cpp_type` the collection
        openers in the value formatter use, with the integer width
        narrowed to the field's own value so the declared type matches
        the rendered integer literal whether or not it carries a suffix
        (including the ``unsigned long long`` an out-of-range integer's
        ``ULL`` overflow literal needs).  A set or non-record dict field
        is out of scope for the base ``RECORD`` port (the cross-language
        decision is tracked in #2317) and is not reached by any record
        golden, so it falls through to the shared
        :func:`_compute_cpp_type` map / initializer-list handling.
        """
        if request.record_name is not None:
            return request.record_name
        if request.element_record_name is not None:
            return f"std::vector<{request.element_record_name}>"
        value = request.value
        if (
            isinstance(value, dict)
            and not isinstance(value, OrderedMap)
            and record_shape_for_dict(value=value) is not None
        ):
            return _CPP_RECORD_MAP_TYPE
        if isinstance(value, int) and not isinstance(value, bool):
            int_type = _cpp_int_field_type(
                value=value,
                int_resolver=self._type_ctx.int_resolver,
            )
        else:
            int_type = "long long"
        element_to_type = self._type_ctx.element_to_type(int_type=int_type)
        return _compute_cpp_type(
            item=value,
            element_to_type=element_to_type,
            type_ctx=self._type_ctx,
            in_mapping_value=False,
        )

    @cached_property
    def _record_renderer(self) -> RecordRenderer:
        """C++ syntax hooks for the ``RECORD`` strategy."""
        return RecordRenderer(
            name_prefix=self.record_struct_name_prefix,
            record_shape_names=_CPP_NO_RECORD_SHAPE_NAMES,
            field_identifier=_cpp_record_field_identifier,
            field_type=self._cpp_record_field_type,
            render_declaration=_cpp_render_record_declaration,
            render_literal=(
                _cpp_record_literal
                if self._uses_cpp20
                else _cpp_record_literal_positional
            ),
        )

    @cached_property
    def _record_strategy(self) -> RecordStrategy:
        """Behavior + ``struct``-declaration preamble for ``RECORD``."""
        strategy = build_record_strategy(
            renderer=self._record_renderer,
            split_conflicting_field_types=True,
            widen_unrecordizable_nested_sibling_maps=True,
            derecordized_map_open=f"{_CPP_RECORD_MAP_TYPE}{{",
        )

        def _wrap_scalar(_raw_value: Scalar, formatted: str) -> str:
            """Construct the shared value variant for a widened map."""
            return f"{_CPP_RECORD_MAP_VALUE}{{{formatted}}}"

        return dataclasses.replace(
            strategy,
            behavior=dataclasses.replace(
                strategy.behavior,
                wrap_scalar=_wrap_scalar,
                widens_nested_maps_by_wrapping_scalars=True,
            ),
        )

    @cached_property
    def _tuple_record_strategy(self) -> RecordStrategy:
        """Compose C++14's candidate-facing tuple and record forms.

        A tuple-eligible field belongs to a generated record just as
        naturally as a scalar field.  Keeping the two native forms in
        one strategy prevents C++14 from falling back to the private
        ``LiteralizerVariant`` carrier for otherwise fixed-shape data.
        """

        def _field_type(request: RecordFieldType) -> str:
            """Resolve a tuple-eligible record field positionally."""
            value = request.value
            if isinstance(value, list) and is_tuple_eligible(value=value):
                return _cpp_tuple_type(items=value, type_ctx=self._type_ctx)
            return self._cpp_record_field_type(request)

        renderer = dataclasses.replace(
            self._record_renderer,
            field_type=_field_type,
        )
        strategy = build_record_strategy(
            renderer=renderer,
            split_conflicting_field_types=True,
            widen_unrecordizable_nested_sibling_maps=True,
            derecordized_map_open=f"{_CPP_RECORD_MAP_TYPE}{{",
        )

        def _wrap_scalar(_raw_value: Scalar, formatted: str) -> str:
            """Wrap a scalar widened beside a map that is not a record."""
            return f"{_CPP_RECORD_MAP_VALUE}{{{formatted}}}"

        behavior = dataclasses.replace(
            strategy.behavior,
            wrap_scalar=_wrap_scalar,
            widens_nested_maps_by_wrapping_scalars=True,
            render_tuple_literal=_render_cpp_tuple,
            compute_tuple_list_ids=_cpp_tuple_list_ids,
        )
        return dataclasses.replace(strategy, behavior=behavior)

    @cached_property
    def _type_ctx(self) -> _CppTypeCtx:
        """Context bundle for C++ type resolution."""
        return _CppTypeCtx(
            int_resolver=self.numeric_literal_suffix.int_resolver,
            date_type=self._cpp_date_type,
            datetime_type=self._cpp_datetime_type,
            tuple_strategy=self._tuple_strategy_active,
            variant_type_name=(
                "LiteralizerVariant"
                if self.language_version is self.version_formats.CPP14
                else "std::variant"
            ),
        )

    @cached_property
    def sequence_format_config(self) -> SequenceFormatConfig:
        """Configuration for the chosen sequence format."""
        if self._json_type_active:
            return _NLOHMANN_JSON_SEQUENCE_CONFIG
        return self.sequence_format.get_config(type_ctx=self._type_ctx)

    @cached_property
    def set_format_config(self) -> SetFormatConfig:
        """Configuration for the chosen set format."""
        if self._json_type_active:
            return _NLOHMANN_JSON_SET_CONFIG
        return self.set_format.get_config(type_ctx=self._type_ctx)

    @cached_property
    def sequence_open(self) -> Callable[[list[Value]], str]:
        """Callable that returns the opening delimiter for a sequence.

        Under the ``RECORD`` strategy a list whose every element is a
        record-shaped dict renders each element as a generated
        ``RecordN`` literal; the variant opener would type such a list
        ``std::vector<std::map<...>>`` (the homogeneous-map element type)
        which the struct literals cannot initialize.  Such a list is
        instead opened with a bare ``std::vector{`` so class-template
        argument deduction infers ``std::vector<RecordN>`` from the
        literals.  Every other list keeps the typed variant opener.
        """
        base_open = self.sequence_format_config.sequence_open
        if not self._record_strategy_active:
            return base_open

        def _open(items: list[Value]) -> str:
            """Return the CTAD ``std::vector{`` opener for an all-record
            list, else the typed variant opener.
            """
            if _all_record_shaped(items):
                return "std::vector{"
            return base_open(items)

        return _open

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
        if self._json_type_active:
            return format_date_iso
        return self._resolved_date_format

    @cached_property
    def format_datetime(self) -> Callable[[datetime.datetime], str]:
        """Callable that formats a datetime as a string literal."""
        if (
            self._json_type_active
            and self.datetime_format.value.type_produced is not int
        ):
            return format_datetime_iso
        return self._resolved_datetime_format

    @cached_property
    def format_time(self) -> Callable[[datetime.time], str]:
        """Callable that formats a time as a string literal."""
        return format_time_iso

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
            min_value=I64_MIN,
            max_value=I64_MAX,
        )

    @cached_property
    def dict_format_config(self) -> DictFormatConfig:
        """Configuration for dict formatting."""
        if self._json_type_active:
            return _NLOHMANN_JSON_DICT_CONFIG
        return self.dict_format.get_config(type_ctx=self._type_ctx)

    @cached_property
    def comment_config(self) -> CommentConfig:
        """Configuration for the language's comment syntax."""
        return self.comment_format.value

    @cached_property
    def ordered_map_format_config(self) -> OrderedMapFormatConfig:
        """Configuration for ordered-map formatting."""
        if self._json_type_active:
            return _NLOHMANN_JSON_ORDERED_MAP_CONFIG
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
        headers, plus ``<tuple>`` under the ``TUPLE`` strategy or the
        generated ``struct`` declarations under ``RECORD``).
        """
        if self._json_type_active:
            return no_data_preamble
        if self._record_strategy_active:
            return _build_cpp_record_preamble(
                type_ctx=self._type_ctx,
                record_preamble=self._record_strategy.preamble,
                compute_wrap_ids=(
                    self._record_strategy.behavior.compute_wrap_ids
                ),
            )
        if self._uses_cpp14_tuple_record_strategy:
            return _build_cpp_record_preamble(
                type_ctx=self._type_ctx,
                record_preamble=self._tuple_record_strategy.preamble,
                compute_wrap_ids=(
                    self._tuple_record_strategy.behavior.compute_wrap_ids
                ),
                include_tuple_header=True,
            )
        if self._tuple_strategy_active:
            return _build_tuple_preamble(type_ctx=self._type_ctx)
        return _build_variant_preamble(type_ctx=self._type_ctx)

    @cached_property
    def heterogeneous_behavior(self) -> HeterogeneousBehavior:
        """Return the heterogeneous-behavior config.

        ``RECORD`` resolves to the shared record behavior (its value
        needs the per-instance renderer, so it cannot be stored on the
        enum member); ``TUPLE`` and ``ERROR`` use their static
        behaviors.
        """
        if self._json_type_active:
            return dataclasses.replace(
                NO_HETEROGENEOUS_BEHAVIOR,
                skip_scalar_checks=True,
            )
        if self._record_strategy_active:
            return self._record_strategy.behavior
        if self._uses_cpp14_tuple_record_strategy:
            return self._tuple_record_strategy.behavior
        if self._tuple_strategy_active:
            return _CPP_TUPLE_BEHAVIOR
        return NO_HETEROGENEOUS_BEHAVIOR

    @cached_property
    def format_variable_declaration(
        self,
    ) -> Callable[[str, str, Value, frozenset[enum.Enum]], str]:
        """Callable that formats a new variable declaration.

        Closes over the chosen date/datetime ``type_produced`` so the
        ``const auto*`` vs ``auto`` decision can be driven by the parsed
        :class:`Value` rather than the rendered text.
        """
        if self._json_type_active:

            def _json_formatter(
                name: str,
                _value: str,
                data: Value,
                modifiers: frozenset[enum.Enum],
            ) -> str:
                """Render an ``auto``-deduced ``nlohmann::json``
                declaration
                via :func:`nlohmann::json::parse` over the inline JSON
                text.

                ``auto`` is used in place of the spelled-out
                ``nlohmann::json`` type so the binding is not analyzed by
                clang-tidy's ``misc-const-correctness`` check (which only
                considers explicitly-typed local variables); the deduced
                type is the same.
                """
                expr = _nlohmann_json_expression(data=data)
                prefix = _cpp_modifier_prefix(modifiers=modifiers)
                return f"{prefix}auto {name} = {expr};"

            return _json_formatter
        date_type = self._resolved_date_format.value.type_produced
        datetime_type = self._resolved_datetime_format.value.type_produced

        def _formatter(
            name: str,
            value: str,
            data: Value,
            modifiers: frozenset[enum.Enum],
        ) -> str:
            """Adapt :func:`_format_variable_declaration` to the
            positional formatter interface.
            """
            return _format_variable_declaration(
                name=name,
                value=value,
                data=data,
                modifiers=modifiers,
                date_type=date_type,
                datetime_type=datetime_type,
            )

        return _formatter

    @cached_property
    def scalar_preamble(self) -> dict[type, tuple[str, ...]]:
        """Per-instance scalar preamble computed from date/datetime format."""
        if self._json_type_active:
            return {}
        return date_scalar_preamble(
            date_format=self._resolved_date_format,
            datetime_format=self._resolved_datetime_format,
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
