"""Kotlin language specification."""

import dataclasses
import datetime
import enum
import functools
import json
import re
from collections.abc import Callable, Mapping, Sequence
from functools import cached_property
from types import MappingProxyType
from typing import ClassVar, assert_never

from beartype import beartype

from literalizer._formatters.collection_openers import (
    TypedOpenerConfig,
    fixed_open,
    make_type_to_opener,
    typed_collection_open,
    typed_dict_open,
)
from literalizer._formatters.format_dates import (
    date_ymd_formatter,
    datetime_epoch_seconds,
    datetime_ymdhms_formatter,
    format_date_iso,
    format_datetime_epoch,
    format_datetime_iso,
    format_time_local_time_of,
)
from literalizer._formatters.format_entries import (
    dict_entry_with_separator,
    dict_entry_with_template,
    format_bytes_base64,
    format_bytes_hex,
    passthrough_sequence_entry,
    passthrough_set_entry,
    variable_declaration_formatter,
    variable_formatter,
)
from literalizer._formatters.format_factories import set_format_factory
from literalizer._formatters.format_floats import (
    format_float_fixed,
    format_float_repr,
    format_float_scientific,
)
from literalizer._formatters.format_integers import (
    I64_MAX,
    I64_MIN,
    data_has_out_of_range_int,
    format_integer_binary,
    format_integer_hex,
    format_integer_underscore,
    make_long_suffix_formatter,
    make_overflow_fallback_formatter,
)
from literalizer._formatters.format_strings import (
    format_string_backslash_dollar,
)
from literalizer._formatters.record_strategy import (
    RecordDeclarationField,
    RecordFieldType,
    RecordLiteralField,
    RecordRenderer,
    RecordStrategy,
    build_record_strategy,
)
from literalizer._formatters.tuple_strategy import (
    TupleRenderer,
    build_tuple_strategy,
)
from literalizer._formatters.type_inference import (
    DictType,
    ListType,
    record_shape_for_dict,
)
from literalizer._language import (
    NO_CALL_PARAMETER_LIMIT,
    NO_HETEROGENEOUS_BEHAVIOR,
    NON_KEBAB_REF_CASES,
    BareIntegerWidthStrategies,
    CallStyle,
    CommentConfig,
    DateFormatConfig,
    DatetimeFormatConfig,
    DeclarationStyleConfig,
    DictFormatConfig,
    FloatSpecialsMixin,
    HeterogeneousBehavior,
    IdentifierCase,
    JsonType,
    KeywordCallStyle,
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
    never_inhibits_consuming_form,
    no_call_binding_body_preamble,
    no_call_binding_file_pragmas,
    no_call_stub,
    no_data_preamble,
    no_leading_preamble,
    no_type_hint_preamble,
    no_validate_call_arg,
    wrap_combined_in_file_noop,
    wrap_in_file_noop,
)
from literalizer._types import OrderedMap, Scalar, Value
from literalizer.exceptions import (
    IncompatibleFormatsError,
    InvalidRecordNameError,
    UnrepresentableInputError,
)

_PASCAL_CASE_IDENTIFIER = re.compile(pattern=r"^[A-Z][A-Za-z0-9_]*$")


@beartype
def _format_kotlin_biginteger_literal(value: int) -> str:
    """Format a value outside signed 64-bit range as a Kotlin
    ``java.math.BigInteger`` constructor call.

    The Kotlin ``Long`` type is signed 64-bit; values outside that
    range must use ``java.math.BigInteger`` (with a matching ``import``
    statement emitted via the data-dependent preamble).
    """
    return f'BigInteger("{value}")'


@beartype
def _kotlin_biginteger_preamble(data: Value, /) -> tuple[str, ...]:
    """Return ``import java.math.BigInteger`` if *data* contains a
    very-large integer.
    """
    if data_has_out_of_range_int(data=data):
        return ("import java.math.BigInteger",)
    return ()


@beartype
def _kotlin_tuple_open(items: list[Value]) -> str:
    """Return the Kotlin tuple opener based on element count."""
    openers: dict[int, str] = {
        2: "Pair(",
        3: "Triple(",
    }
    return openers.get(len(items), "listOf<Any?>(")


@beartype
def _kotlin_list_sequence_open(
    *,
    cfg: TypedOpenerConfig,
    date_type: str | None,
    datetime_type: str | None,
    dict_key_type: str,
) -> Callable[[list[Value]], str]:
    """Build a typed sequence opener for the Kotlin List format.

    Delegates to ``_kotlin_type_to_opener`` for scalars and lists
    (preserving specialized openers like ``intArrayOf``), and falls
    through to the config resolver for ``DictType`` so that nested
    types and date/datetime formats are handled correctly.
    """
    dict_resolver = cfg.element_to_type(
        list_template="List<{inner}>",
        enable_list_type=True,
        date_type=date_type,
        datetime_type=datetime_type,
        enable_dict_type=True,
        dict_key_type=dict_key_type,
    )

    def _combined_opener(
        element_type: type | ListType | DictType,
    ) -> str | None:
        """Delegate to module-level implementation."""
        return _apply_kotlin_combined_opener(
            element_type=element_type, dict_resolver=dict_resolver
        )

    return typed_collection_open(
        type_to_opener=_combined_opener,
        fallback="listOf<Any?>(",
    )


@beartype
def _apply_kotlin_combined_opener(
    element_type: type | ListType | DictType,
    dict_resolver: Callable[[type | ListType | DictType], str | None],
) -> str | None:
    """Resolve element type, preferring specialized Kotlin openers."""
    if isinstance(element_type, DictType):
        return f"listOf<{dict_resolver(element_type)}>("
    return _kotlin_type_to_opener(element_type=element_type)


@beartype
def _kotlin_type_to_opener(
    element_type: type | ListType | DictType,
) -> str | None:
    """Map a Python element type to a Kotlin collection opener.

    Used as the scalar/list fallback for the LIST format (via
    :func:`_kotlin_list_sequence_open`).  Returns ``None`` for
    ``DictType`` — the LIST format handles dicts via the config
    resolver before calling this function.
    """
    scalar_openers: dict[type, str] = {
        str: "arrayOf(",
        bool: "booleanArrayOf(",
        int: "intArrayOf(",
        float: "doubleArrayOf(",
        bytes: "arrayOf(",
        datetime.date: "arrayOf(",
        datetime.datetime: "arrayOf(",
        datetime.time: "arrayOf(",
    }
    match element_type:
        case DictType():
            return None
        case ListType():
            inner = _kotlin_type_to_opener(element_type=element_type.inner)
            return "arrayOf(" if inner is not None else None
        case _:
            return scalar_openers.get(element_type)


@beartype
def _kotlin_dict_value_type_name(
    element_type: type | ListType | DictType,
    *,
    base_resolver: Callable[[type | ListType | DictType], str | None],
    key_type: str,
    fallback: str,
) -> str | None:
    """Resolve a dict value's Kotlin type name to match the renderer.

    Narrows only ``DictType`` values, to ``Map<key, ...>`` recursively
    (``Map`` is covariant in its value type, so a narrower rendered map
    is still accepted), and defers every other element type to
    *base_resolver*, which keeps the prior ``Array``/``Any?`` list
    typing.  See :meth:`Kotlin._kotlin_dict_value_type` for why list
    values are left to *base_resolver* rather than narrowed (#2890).
    """
    if not isinstance(element_type, DictType):
        return base_resolver(element_type)
    value_type = element_type.value_type
    if value_type is None:
        return f"Map<{key_type}, {fallback}>"
    inner = _kotlin_dict_value_type_name(
        element_type=value_type,
        base_resolver=base_resolver,
        key_type=key_type,
        fallback=fallback,
    )
    return f"Map<{key_type}, {inner if inner is not None else fallback}>"


_KOTLIN_I32_MIN = -(2**31)
_KOTLIN_I32_MAX = 2**31 - 1


@beartype
def _kotlin_scalar_hint(
    *,
    data: Scalar,
    date_hint: str,
    datetime_hint: str,
) -> str:
    """Derive the Kotlin annotation for a scalar value."""
    match data:
        case bool():
            hint = "Boolean"
        case int():
            hint = (
                "Long"
                if not _KOTLIN_I32_MIN <= data <= _KOTLIN_I32_MAX
                else "Int"
            )
        case float():
            hint = "Double"
        case str() | bytes():
            hint = "String"
        case datetime.datetime():
            hint = datetime_hint
        case datetime.date():
            hint = date_hint
        case datetime.time():
            hint = "LocalTime"
        case None:
            hint = "Nothing?"
        case _ as unreachable:
            assert_never(unreachable)
    return hint


@beartype
def _kotlin_dict_hint(
    *,
    is_empty: bool,
    is_ordered: bool,
    val_types: list[str],
    default_dict_key_type: str,
    default_dict_value_type: str,
    dict_outer: str,
) -> str:
    """Derive a Kotlin map type annotation."""
    outer = "LinkedHashMap" if is_ordered else dict_outer
    if is_empty:
        return f"{outer}<{default_dict_key_type}, {default_dict_value_type}>"
    unique = list(dict.fromkeys(val_types))
    val_type = unique[0] if len(unique) == 1 else "Any?"
    return f"{outer}<{default_dict_key_type}, {val_type}>"


@beartype
def _kotlin_set_hint(
    *,
    elem_types_sorted: list[str],
    is_empty: bool,
    default_set_element_type: str,
    set_outer: str,
) -> str:
    """Derive a Kotlin set type annotation."""
    if is_empty:
        return f"{set_outer}<{default_set_element_type}>"
    unique = set(elem_types_sorted)
    match unique:
        case _ if unique == {"Int", "Long"}:
            elem_type = "Long"
        case _ if len(unique) == 1:
            elem_type = elem_types_sorted[0]
        case _:
            elem_type = "Any?"
    return f"{set_outer}<{elem_type}>"


@beartype
def _kotlin_tuple_hint(*, elem_types: list[str]) -> str:
    """Derive a Kotlin tuple-shaped annotation."""
    match elem_types:
        case [_, _]:
            return f"Pair<{', '.join(elem_types)}>"
        case [_, _, _]:
            return f"Triple<{', '.join(elem_types)}>"
        case _:
            return "List<Any?>"


@beartype
def _kotlin_array_or_list_hint(*, elem_types: list[str]) -> str:
    """Derive a Kotlin array/list annotation for the ``LIST`` format."""
    unique = list(dict.fromkeys(elem_types))
    if len(unique) != 1:
        return "List<Any?>"
    elem_type = unique[0]
    kotlin_prim = {
        "Boolean": "BooleanArray",
        "Int": "IntArray",
        "Double": "DoubleArray",
    }
    if elem_type in kotlin_prim:
        return kotlin_prim[elem_type]
    # Generic element types (e.g. Map<…>) use listOf, not arrayOf, so
    # the container type is List, not Array.
    if "<" in elem_type:
        return f"List<{elem_type}>"
    return f"Array<{elem_type}>"


@beartype
def _kotlin_list_hint(
    *,
    data: list[Value],
    recurse: Callable[..., str],
    sequence_format_name: str,
) -> str:
    """Derive a Kotlin sequence type annotation."""
    if not data:
        return (
            "Array<Any?>" if sequence_format_name == "ARRAY" else "List<Any?>"
        )
    if sequence_format_name == "ARRAY":
        return "Array<Any?>"
    elem_types = [recurse(data=e) for e in data]
    if sequence_format_name == "TUPLE":
        return _kotlin_tuple_hint(elem_types=elem_types)
    return _kotlin_array_or_list_hint(elem_types=elem_types)


@beartype
def _kotlin_type_hint(
    *,
    data: Value,
    date_hint: str,
    datetime_hint: str,
    default_set_element_type: str,
    default_dict_key_type: str,
    default_dict_value_type: str,
    dict_outer: str,
    set_outer: str,
    sequence_format_name: str,
) -> str:
    """Derive a Kotlin type annotation from *data*."""
    recurse = functools.partial(
        _kotlin_type_hint,
        date_hint=date_hint,
        datetime_hint=datetime_hint,
        default_set_element_type=default_set_element_type,
        default_dict_key_type=default_dict_key_type,
        default_dict_value_type=default_dict_value_type,
        dict_outer=dict_outer,
        set_outer=set_outer,
        sequence_format_name=sequence_format_name,
    )
    match data:
        case dict():
            hint = _kotlin_dict_hint(
                is_empty=not data,
                is_ordered=isinstance(data, OrderedMap),
                val_types=[recurse(data=v) for v in data.values()],
                default_dict_key_type=default_dict_key_type,
                default_dict_value_type=default_dict_value_type,
                dict_outer=dict_outer,
            )
        case set():
            hint = _kotlin_set_hint(
                elem_types_sorted=sorted({recurse(data=e) for e in data}),
                is_empty=not data,
                default_set_element_type=default_set_element_type,
                set_outer=set_outer,
            )
        case list():
            hint = _kotlin_list_hint(
                data=data,
                recurse=recurse,
                sequence_format_name=sequence_format_name,
            )
        case _:
            hint = _kotlin_scalar_hint(
                data=data,
                date_hint=date_hint,
                datetime_hint=datetime_hint,
            )
    return hint


@beartype
def _format_kotlin_typed_declaration(
    *,
    name: str,
    value: str,
    data: Value,
    _modifiers: frozenset[enum.Enum],
    keyword: str,
    date_hint: str,
    datetime_hint: str,
    default_set_element_type: str,
    default_dict_key_type: str,
    default_dict_value_type: str,
    dict_outer: str,
    set_outer: str,
    sequence_format_name: str,
) -> str:
    """Format a Kotlin variable declaration with an explicit type."""
    hint = _kotlin_type_hint(
        data=data,
        date_hint=date_hint,
        datetime_hint=datetime_hint,
        default_set_element_type=default_set_element_type,
        default_dict_key_type=default_dict_key_type,
        default_dict_value_type=default_dict_value_type,
        dict_outer=dict_outer,
        set_outer=set_outer,
        sequence_format_name=sequence_format_name,
    )
    return f"{keyword} {name}: {hint} = {value}"


@dataclasses.dataclass(frozen=True)
class _KotlinDictSpec:
    """Per-format dict config pieces resolved at init time."""

    opener_template: str


@beartype
def _kotlin_call_stub(
    parts: Sequence[str],
    params: Sequence[str],
    _stub_return: StubReturn,
    _args: Sequence[Value],
    /,
) -> tuple[str, ...]:
    """Return Kotlin stub declarations for a call name."""
    param_list = ", ".join(f"{p}: Any? = null" for p in params)
    if len(parts) == 1:
        return (f"fun {parts[0]}({param_list}): Any? = null",)
    root = parts[0]
    method = parts[-1]
    fields = parts[1:-1]
    if not fields:
        cls = f"_{root.title()}Type"
        return (
            f"class {cls} {{ fun {method}({param_list}): Any? = null }}",
            f"val {root} = {cls}()",
        )
    lines: list[str] = []
    inner_cls = f"_{fields[-1].title()}Type"
    lines.append(
        f"class {inner_cls} {{ fun {method}({param_list}): Any? = null }}"
    )
    prev_cls = inner_cls
    for i in range(len(fields) - 2, -1, -1):
        cls = f"_{fields[i].title()}Type"
        lines.append(f"class {cls} {{ val {fields[i + 1]} = {prev_cls}() }}")
        prev_cls = cls
    root_cls = f"_{root.title()}Type"
    lines.append(f"class {root_cls} {{ val {fields[0]} = {prev_cls}() }}")
    lines.append(f"val {root} = {root_cls}()")
    return tuple(lines)


# Kotlin collection-constructor call names mapped to the declared type
# they produce, used to derive a ``RECORD`` field's type from the
# generic collection opener the value formatter emits (e.g.
# ``linkedMapOf<String, Any?>(`` -> ``LinkedHashMap<String, Any?>``).
_KOTLIN_COLLECTION_TYPE: dict[str, str] = {
    "listOf": "List",
    "mapOf": "Map",
    "hashMapOf": "HashMap",
    "linkedMapOf": "LinkedHashMap",
    "setOf": "Set",
}


@beartype
def _kotlin_opener_to_type(opener: str, /) -> str:
    """Map a Kotlin collection opener to its declared field type.

    ``intArrayOf(`` is the primitive ``IntArray``; every other opener
    is a generic constructor call whose ``<...>`` segment is the
    declared type (``listOf<Any?>(`` -> ``List<Any?>``,
    ``linkedMapOf<String, Any?>(`` -> ``LinkedHashMap<String, Any?>``).
    ``arrayOf(`` carries no element type in the opener and is handled
    by the caller.
    """
    if opener == "intArrayOf(":
        return "IntArray"
    name = opener[: opener.index("<")]
    generics = opener[opener.index("<") : opener.rindex(">") + 1]
    return f"{_KOTLIN_COLLECTION_TYPE[name]}{generics}"


@beartype
def _kotlin_record_field_identifier(key: str, /) -> str:
    """Return the Kotlin record field name for a dict *key*.

    Kotlin allows the original (possibly snake_case) key verbatim as a
    ``data class`` property name, so the mapping is the identity.
    """
    return key


@beartype
def _kotlin_render_declaration(
    name: str,
    fields: Sequence[RecordDeclarationField],
    /,
) -> str:
    """Render a Kotlin ``data class Name(val f: T, ...)`` declaration."""
    params = ", ".join(
        f"val {field.identifier}: {field.type_name}" for field in fields
    )
    return f"data class {name}({params})"


@beartype
def _kotlin_record_literal(
    name: str,
    fields: Sequence[RecordLiteralField],
    /,
) -> RenderedRecordLiteral:
    """Render a Kotlin ``Name(field = value, ...)`` literal as
    structured pieces for the shared compact/multiline layout code.
    """
    return RenderedRecordLiteral(
        head=f"{name}(",
        entries=tuple(
            f"{field.identifier} = {field.formatted}" for field in fields
        ),
        closer=")",
        compact_pad="",
    )


@beartype
def _kotlin_tuple_literal(
    value: list[Value],
    elements: Sequence[str],
    /,
) -> RenderedTupleLiteral:
    """Render a heterogeneous scalar array as a Kotlin two-element
    ``Pair(...)`` or three-element ``Triple(...)`` literal as
    structured pieces for the shared compact/multiline layout code.

    :func:`~literalizer._formatters.tuple_strategy.build_tuple_strategy`
    validates the length at check time (Kotlin has no fixed-size tuple
    of any other length), so *value* is always length 2 or 3 here; it
    selects the constructor and is otherwise unused because every
    element arrives already formatted.
    """
    head = {2: "Pair(", 3: "Triple("}[len(value)]
    return RenderedTupleLiteral(
        head=head,
        entries=tuple(elements),
        closer=")",
        compact_pad="",
        # ``Pair(a,\n    b,\n)`` is valid Kotlin -- a trailing comma is
        # allowed in an argument list -- so keep the language-wide
        # trailing-comma policy for the multiline form.
        multiline_trailing_comma=True,
    )


@beartype
def _kotlin_tuple_arity_representable(arity: int, /) -> bool:
    """Return whether Kotlin has a native fixed-size tuple of the
    given element count.

    Kotlin only ships ``Pair`` (two elements) and ``Triple`` (three
    elements); any other length has no typed tuple, so the ``TUPLE``
    strategy raises rather than dropping the per-position types.
    """
    return arity in {2, 3}


_KOTLINX_JSON_ELEMENT_PREAMBLE: tuple[str, ...] = (
    "import kotlinx.serialization.json.Json",
    "import kotlinx.serialization.json.JsonElement",
)


# Sequence/dict format definitions used while ``json_type`` is active.
# The framework still walks the data to compute a formatted ``value``,
# but that string is discarded by
# :func:`_make_format_kotlin_json_declaration` and friends in favor of a
# fresh ``json.dumps`` of the raw data.  These definitions only need to
# be permissive enough that the formatting pass does not error on
# heterogeneous data or nulls inside containers.
_JSON_NODE_SEQUENCE_CONFIG = SequenceFormatConfig(
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

_JSON_NODE_SET_CONFIG = SetFormatConfig(
    set_open=fixed_open(open_str="["),
    close="]",
    empty_set="[]",
    preamble_lines=(),
    set_opener_template="",
    supports_heterogeneity=True,
    supports_trailing_comma=True,
)

_JSON_NODE_DICT_CONFIG = DictFormatConfig(
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

_JSON_NODE_ORDERED_MAP_CONFIG = OrderedMapFormatConfig(
    ordered_map_open=fixed_open(open_str="{"),
    close="}",
    preamble_lines=(),
)


@beartype
def _kotlin_temporal_to_iso(data: datetime.date | datetime.time) -> str:
    """Return ISO-8601 text for a date / datetime / time value."""
    return data.isoformat()


@beartype
def _kotlin_to_jsonable(data: Value) -> object:
    """Convert *data* into a value :func:`json.dumps` can serialize.

    Dates, datetimes, and times become ISO-8601 strings (JSON has no
    temporal type).  Bytes become a hex-encoded string.  Sets and
    :class:`OrderedMap` are folded into list/dict respectively.  Non-
    string dict keys are not handled here; the caller validates first.
    """
    match data:
        case datetime.datetime() | datetime.date() | datetime.time():
            return _kotlin_temporal_to_iso(data=data)
        case bytes():
            return data.hex()
        case OrderedMap() | dict():
            return {
                key: _kotlin_to_jsonable(data=value)
                for key, value in data.items()
            }
        case set():
            items = [_kotlin_to_jsonable(data=item) for item in data]
            items.sort(key=repr)
            return items
        case list():
            return [_kotlin_to_jsonable(data=item) for item in data]
        case _:
            return data


@beartype
def _format_kotlin_json_value(data: Value) -> str:
    """Serialize *data* as a single-line JSON expression."""
    return json.dumps(
        obj=_kotlin_to_jsonable(data=data),
        ensure_ascii=False,
    )


@beartype
def _kotlin_parse_to_json_element_expression(data: Value) -> str:
    """Render ``Json.parseToJsonElement("...")`` for *data*."""
    json_text = _format_kotlin_json_value(data=data)
    kotlin_literal = format_string_backslash_dollar(value=json_text)
    return f"Json.parseToJsonElement({kotlin_literal})"


@beartype
def _make_format_kotlin_json_declaration(
    *,
    keyword: str,
) -> Callable[[str, str, Value, frozenset[enum.Enum]], str]:
    """Build a JsonElement declaration formatter for ``val`` or ``var``.

    The keyword tracks ``declaration_style`` so the combined
    declaration + assignment form stays valid Kotlin (``var`` lets the
    later assignment rebind the variable).
    """

    @beartype
    def _format(
        name: str,
        _value: str,
        data: Value,
        _modifiers: frozenset[enum.Enum],
    ) -> str:
        """Format the declaration with the bound *keyword*."""
        expression = _kotlin_parse_to_json_element_expression(data=data)
        return f"{keyword} {name}: JsonElement = {expression}"

    return _format


@beartype
def _format_kotlin_json_assignment(
    name: str,
    _value: str,
    data: Value,
) -> str:
    """Format a JsonElement assignment backed by
    ``parseToJsonElement``.
    """
    return f"{name} = {_kotlin_parse_to_json_element_expression(data=data)}"


@beartype
def _format_kotlin_json_call_arg(raw_value: Value, _formatted: str) -> str:
    """Format a direct call argument as a JsonElement literal."""
    return _kotlin_parse_to_json_element_expression(data=raw_value)


@beartype
@dataclasses.dataclass(frozen=True, kw_only=True)
class Kotlin(metaclass=LanguageCls):
    """Kotlin language specification.

    Args:
        date_format: How to format :class:`datetime.date` values.

            * ``date_formats.KOTLIN`` — ``LocalDate.of(...)`` call,
              e.g. ``LocalDate.of(2024, 1, 15)``.
            * ``date_formats.ISO`` — ISO 8601 quoted string,
              e.g. ``"2024-01-15"``.

        datetime_format: How to format :class:`datetime.datetime` values.

            * ``datetime_formats.KOTLIN`` — ``LocalDateTime.of(...)`` call,
              e.g. ``LocalDateTime.of(2024, 1, 15, 12, 30, 0)``.
            * ``datetime_formats.ISO`` — ISO 8601 quoted string,
              e.g. ``"2024-01-15T12:30:00"``.

        sequence_format: Which Kotlin sequence type to use.

            * ``sequence_formats.LIST`` — typed array calls
              (e.g. ``intArrayOf(1, 2, 3)``).  Heterogeneous
              sequences fall back to ``listOf<Any?>(…)``.
            * ``sequence_formats.TUPLE`` — ``Pair(…)`` for two-element
              sequences, ``Triple(…)`` for three-element sequences,
              e.g. ``Pair("a", 1)``.  Other sizes fall back to
              ``listOf<Any?>(…)``.

        json_type: When set to ``json_types.KOTLINX_JSON_ELEMENT``,
            render values through ``Json.parseToJsonElement(...)`` so
            the output produces a ``kotlinx.serialization.json.JsonElement``
            instead of Kotlin's narrow ``List`` / ``Map`` / array types.
    """

    format_call_variable_declaration = default_format_call_variable_declaration
    format_call_variable_assignment = default_format_call_variable_assignment
    format_constructor_target: ClassVar["staticmethod[[str], str]"] = (
        staticmethod(identity_constructor_target)
    )
    sequence_binding_declarations = default_sequence_binding_declarations
    format_call_binding_body_preamble = no_call_binding_body_preamble
    format_call_binding_file_pragmas = no_call_binding_file_pragmas

    leading_preamble = no_leading_preamble
    extension = ".kts"
    pygments_name = "kotlin"
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
            "as",
            "break",
            "class",
            "continue",
            "do",
            "else",
            "false",
            "for",
            "fun",
            "if",
            "in",
            "interface",
            "is",
            "null",
            "object",
            "package",
            "return",
            "super",
            "this",
            "throw",
            "true",
            "try",
            "typealias",
            "typeof",
            "val",
            "var",
            "when",
            "while",
        }
    )
    allows_empty_call_parens = True
    supports_dotted_call_stub = True
    call_returns_expression = True
    supports_zero_parameter_calls = True
    max_call_parameters = NO_CALL_PARAMETER_LIMIT
    supports_inline_multiline_dict_args = True
    supports_standalone_comments_in_wrapped_calls = True
    supports_multi_param_call_wrapper_stub = True
    supports_dict_literal_as_free_expression = True
    supports_module_name = False
    supports_empty_dict_key = False
    supports_call_style = True
    supports_default_dict_key_type = True
    supports_default_dict_value_type = True
    supports_default_sequence_element_type = False
    supports_default_set_element_type = True
    supports_default_ordered_map_value_type = False
    non_default_kwargs: ClassVar[dict[str, str]] = {
        "default_set_element_type": "String",
        "default_dict_value_type": "Comparable<*>?",
        "default_dict_key_type": "Any",
    }
    declaration_style_sequence_format_overrides: ClassVar[dict[str, str]] = {}
    json_type_variant_name_suffix: ClassVar[str | None] = None
    supports_non_ascii_string_literals = True
    variant_metadata: ClassVar[VariantMetadata] = VariantMetadata(
        string_literals_escape_null_byte=False,
        pre_indent_comment_scalar_variant=False,
        fixture_module_name_template=None,
        fixture_module_name_lowercase=False,
        golden_filename_lowercase=False,
        collection_layout_category="collection_layout",
        record_variants=frozenset({RecordVariant.FIELD_TYPE_SPLIT}),
        nested_map_widening=NestedMapWideningVariant.DEFAULT,
        modifier_sequence_format_overrides={},
    )
    supports_record_struct_name_prefix = True
    supports_record_shape_names = True
    supports_non_string_dict_keys = False

    _opener_config = TypedOpenerConfig(
        str_type="String",
        bool_type="Boolean",
        int_type="Int",
        wide_int_type="Long",
        beyond_i64_type="BigInteger",
        float_type="Double",
        bytes_type="String",
        mixed_numeric_type=None,
        date_type="LocalDate",
        datetime_type="LocalDateTime",
        time_type="LocalTime",
        list_template="Array<{inner}>",
        sequence_opener_template="arrayOf(",
        dict_opener_template="mapOf<{key_type}, {type_name}>(",
        set_opener_template="setOf<{type_name}>(",
        dict_type_template="Map<{key_type}, {inner}>",
        fallback_value_type="Any?",
    )

    class DateFormats(enum.Enum):
        """Date format options for Kotlin."""

        KOTLIN = DateFormatConfig(
            formatter=date_ymd_formatter(
                template="LocalDate.of({year}, {month}, {day})",
            ),
            preamble_lines=("import java.time.LocalDate",),
            type_produced=datetime.date,
        )
        ISO = DateFormatConfig(
            formatter=format_date_iso, type_produced=str, preamble_lines=()
        )

        def __call__(self, date_value: datetime.date, /) -> str:
            """Format a date."""
            return self.value.formatter(date_value)

    class DatetimeFormats(enum.Enum):
        """Datetime format options for Kotlin."""

        KOTLIN = DatetimeFormatConfig(
            formatter=datetime_ymdhms_formatter(
                template="LocalDateTime.of({year}, {month}, {day}, "
                "{hour}, {minute}, {second})",
            ),
            preamble_lines=("import java.time.LocalDateTime",),
            type_produced=datetime.datetime,
        )
        ISO = DatetimeFormatConfig(
            formatter=format_datetime_iso,
            type_produced=str,
            preamble_lines=(),
        )

        EPOCH = DatetimeFormatConfig(
            formatter=format_datetime_epoch,
            type_produced=int,
            preamble_lines=(),
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
        """Sequence type options for Kotlin."""

        LIST = SequenceFormatConfig(
            sequence_open=typed_collection_open(
                type_to_opener=_kotlin_type_to_opener,
                fallback="listOf<Any?>(",
            ),
            close=")",
            supports_heterogeneity=True,
            single_element_trailing_comma=False,
            supports_trailing_comma=True,
            empty_sequence=None,
            preamble_lines=(),
            format_entry=passthrough_sequence_entry,
            typed_opener_fallback="listOf<Any?>(",
            uses_typed_literal_for_scalars=False,
            requires_uniform_record_shapes=False,
            declared_type=None,
            narrowed_empty_form=None,
        )
        ARRAY = SequenceFormatConfig(
            sequence_open=fixed_open(open_str="arrayOf<Any?>("),
            close=")",
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
            narrowed_empty_form=None,
        )
        TUPLE = SequenceFormatConfig(
            sequence_open=_kotlin_tuple_open,
            format_entry=passthrough_sequence_entry,
            typed_opener_fallback=None,
            uses_typed_literal_for_scalars=False,
            requires_uniform_record_shapes=False,
            close=")",
            supports_heterogeneity=True,
            single_element_trailing_comma=False,
            supports_trailing_comma=True,
            empty_sequence=None,
            preamble_lines=(),
            declared_type=None,
            narrowed_empty_form=None,
        )

    class SetFormats(enum.Enum):
        """Set type options for Kotlin."""

        SET = enum.member(
            value=set_format_factory(
                open_template="setOf<{type}>(",
                close=")",
                empty_template=None,
                preamble_lines=(),
                set_opener_template="",
                supports_heterogeneity=True,
                supports_trailing_comma=True,
            )
        )
        SORTED_SET = enum.member(
            value=set_format_factory(
                open_template="sortedSetOf<{type}>(",
                close=")",
                empty_template=None,
                preamble_lines=(),
                set_opener_template="sortedSetOf<{type_name}>(",
                supports_heterogeneity=False,
                supports_trailing_comma=True,
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

        VAL = DeclarationStyleConfig(
            formatter=variable_declaration_formatter(
                template="val {name} = {value}"
            ),
            supports_redefinition=False,
        )
        VAR = DeclarationStyleConfig(
            formatter=variable_declaration_formatter(
                template="var {name} = {value}"
            ),
            supports_redefinition=True,
        )

    class DictEntryStyles(enum.Enum):
        """Dict entry style options."""

        DEFAULT = enum.auto()

    class DictFormats(enum.Enum):
        """Dict/map format options."""

        MAP = _KotlinDictSpec(
            opener_template="mapOf<{key_type}, {type_name}>(",
        )
        HASH_MAP = _KotlinDictSpec(
            opener_template="hashMapOf<{key_type}, {type_name}>(",
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

        DOUBLE = enum.auto()

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

        NEVER = enum.auto()
        ALWAYS = enum.auto()
        SAFE = enum.auto()

        def formatter(
            self,
            *,
            auto_formatter: Callable[
                [str, str, Value, frozenset[enum.Enum]], str
            ],
            keyword: str,
            date_hint: str,
            datetime_hint: str,
            default_set_element_type: str,
            default_dict_key_type: str,
            default_dict_value_type: str,
            dict_outer: str,
            set_outer: str,
            sequence_format_name: str,
        ) -> Callable[[str, str, Value, frozenset[enum.Enum]], str]:
            """Return the variable declaration formatter."""
            if self.name in {"NEVER", "SAFE"}:
                return auto_formatter

            def _typed_formatter(
                name: str,
                value: str,
                data: Value,
                modifiers: frozenset[enum.Enum],
            ) -> str:
                """Adapt :func:`_format_kotlin_typed_declaration` to the
                positional formatter interface.
                """
                return _format_kotlin_typed_declaration(
                    name=name,
                    value=value,
                    data=data,
                    _modifiers=modifiers,
                    keyword=keyword,
                    date_hint=date_hint,
                    datetime_hint=datetime_hint,
                    default_set_element_type=default_set_element_type,
                    default_dict_key_type=default_dict_key_type,
                    default_dict_value_type=default_dict_value_type,
                    dict_outer=dict_outer,
                    set_outer=set_outer,
                    sequence_format_name=sequence_format_name,
                )

            return _typed_formatter

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
        """Kotlin call style options."""

        KEYWORD = KeywordCallStyle(separator=" = ")
        POSITIONAL = PositionalCallStyle(
            arg_separator=", ", parenthesize_each_arg=False
        )

    call_styles = CallStyles

    class Modifiers(enum.Enum):
        """C++/Java/C#-style declaration modifiers: this language has none."""

    modifiers = Modifiers

    class HeterogeneousStrategies(enum.Enum):
        """Strategy for dicts whose values span more than one Kotlin
        type.

        ``ERROR`` keeps Kotlin's strict-typing behavior (mixed-value
        dicts that cannot be represented raise).  ``RECORD`` renders
        each record-shaped dict (non-empty, string-keyed) as a generated
        ``data class`` declared in the preamble plus a matching
        constructor-call literal, so fields may legitimately mix scalars
        and containers.  ``TUPLE`` composes ``RECORD`` and additionally
        renders a fixed-length heterogeneous scalar array that is a
        dict value or the document root as a two-element ``Pair(...)``
        or three-element ``Triple(...)`` typed ``Pair<...>`` /
        ``Triple<...>`` -- a record field whose value is such an array
        becomes a tuple-typed field.  Kotlin has no general N-tuple, so
        an array of any other length raises
        :class:`~literalizer.exceptions.TupleArityNotRepresentableError`
        rather than degrading to a homogeneous list.
        """

        ERROR = enum.auto()
        RECORD = enum.auto()
        TUPLE = enum.auto()

    heterogeneous_strategies = HeterogeneousStrategies

    class BoolFormats(enum.Enum):
        """Empty: this language has no alternative boolean formats."""

    bool_formats = BoolFormats

    class JsonTypes(JsonType):
        """JSON value type options for Kotlin."""

        KOTLINX_JSON_ELEMENT = "kotlinx.serialization.json.JsonElement"
        """Dynamic JSON value type from ``kotlinx.serialization.json``."""

    json_types = JsonTypes

    class VersionFormats(enum.Enum):
        """Version options for Kotlin."""

        V1_9 = enum.auto()

    version_formats = VersionFormats

    modifier_combinations: ClassVar[tuple[ModifierCombination, ...]] = ()
    identifier_cases: ClassVar[tuple[IdentifierCase, ...]] = (
        IdentifierCase.CAMEL,
        IdentifierCase.PASCAL,
        IdentifierCase.UPPER_SNAKE,
    )
    supported_ref_cases: ClassVar[frozenset[IdentifierCase]] = (
        NON_KEBAB_REF_CASES
    )

    @cached_property
    def validate_call_arg(self) -> Callable[[Value], None]:
        """Return call-argument validation for this language."""
        return no_validate_call_arg

    @cached_property
    def format_call_statement(self) -> Callable[[str], str]:
        """Return call-statement formatting for this language."""
        return identity_call_statement

    wrap_calls_with_declarations = default_wrap_calls_with_declarations

    @staticmethod
    def wrap_in_file(
        content: str,
        variable_name: str,
        body_preamble: tuple[str, ...],
    ) -> str:
        """Wrap code in a valid file (no-op)."""
        return wrap_in_file_noop(
            content=content,
            variable_name=variable_name,
            body_preamble=body_preamble,
        )

    @staticmethod
    def wrap_combined_in_file(
        declaration: str,
        assignment: str,
        variable_name: str,
        body_preamble: tuple[str, ...],
    ) -> str:
        """Wrap declaration and assignment in a valid file (no-op)."""
        return wrap_combined_in_file_noop(
            declaration=declaration,
            assignment=assignment,
            variable_name=variable_name,
            body_preamble=body_preamble,
        )

    date_format: DateFormats = DateFormats.KOTLIN
    datetime_format: DatetimeFormats = DatetimeFormats.KOTLIN
    bytes_format: BytesFormats = BytesFormats.HEX
    sequence_format: SequenceFormats = SequenceFormats.LIST
    set_format: SetFormats = SetFormats.SET
    default_set_element_type: str = "Any?"
    default_dict_key_type: str = "String"
    default_dict_value_type: str = "Any?"
    variable_type_hints: VariableTypeHints = VariableTypeHints.NEVER
    comment_format: CommentFormats = CommentFormats.DOUBLE_SLASH
    declaration_style: DeclarationStyles = DeclarationStyles.VAL
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
    call_style: CallStyles = CallStyles.KEYWORD
    heterogeneous_strategy: HeterogeneousStrategies = (
        HeterogeneousStrategies.ERROR
    )
    json_type: JsonTypes | None = None
    record_struct_name_prefix: str = "Record"
    record_shape_names: Mapping[frozenset[str], str] = dataclasses.field(
        default_factory=lambda: MappingProxyType(mapping={}),
        hash=False,
    )
    # Keep in sync with the version flags passed to the Kotlin lint host in
    # `scripts/lint-kotlin.main.kts`.
    language_version: VersionFormats = VersionFormats.V1_9
    indent: str = "    "

    null_literal: ClassVar[str] = "null"
    true_literal: ClassVar[str] = "true"
    false_literal: ClassVar[str] = "false"
    indent_closing_delimiter: ClassVar[bool] = False
    element_separator: ClassVar[str] = ", "
    skip_null_dict_values: ClassVar[bool] = False
    supports_collection_comments: ClassVar[bool] = True
    supports_scalar_before_comments: ClassVar[bool] = True
    supports_scalar_inline_comments: ClassVar[bool] = True
    statement_terminator: ClassVar[str] = ""
    static_body_preamble: ClassVar[Sequence[str]] = ()
    special_float_preamble: ClassVar[tuple[str, ...]] = ()

    def __post_init__(self) -> None:
        """Validate ``record_shape_names`` after construction."""
        self._validate_record_naming()
        self._validate_json_type_spec()

    @cached_property
    def _json_type_active(self) -> bool:
        """Return whether Kotlin should render via ``JsonElement``."""
        return self.json_type is not None

    @cached_property
    def static_preamble(self) -> Sequence[str]:
        """Static preamble lines emitted once per file.

        When :attr:`json_type` is active the ``Json`` and ``JsonElement``
        imports are emitted here so every fixture has them in scope
        regardless of the rendered data.
        """
        if self._json_type_active:
            return _KOTLINX_JSON_ELEMENT_PREAMBLE
        return ()

    @cached_property
    def format_call_arg(self) -> Callable[[Value, str], str]:
        """Callable that rewrites a formatted direct call argument."""
        if self._json_type_active:
            return _format_kotlin_json_call_arg
        return identity_call_arg

    def _validate_json_type_spec(self) -> None:
        """Reject ``json_type`` combinations the generator cannot emit.

        ``Json.parseToJsonElement(...)`` produces a single
        ``JsonElement`` value; a ``RECORD`` or ``TUPLE`` heterogeneous
        strategy would generate ``data class`` declarations and
        ``Pair``/``Triple`` literals that have no place inside that
        single JSON value, so both are rejected up front.
        """
        if not self._json_type_active:
            return
        cls = type(self.heterogeneous_strategy)
        if self.heterogeneous_strategy is not cls.ERROR:
            msg = (
                "Kotlin json_type renders data through "
                "Json.parseToJsonElement(...) and is incompatible with "
                f"heterogeneous_strategy={self.heterogeneous_strategy.name}, "
                "which generates typed declarations. Use "
                "heterogeneous_strategy=ERROR."
            )
            raise IncompatibleFormatsError(msg)

    def _validate_json_value_keys(self, data: Value, /) -> None:
        """Reject non-string object keys for ``JsonElement``."""
        match data:
            case OrderedMap() | dict():
                for key, value in data.items():
                    if not isinstance(key, str):
                        msg = (
                            "Kotlin json_type can only represent dict "
                            "keys as JSON object strings, not "
                            f"{type(key).__name__}"
                        )
                        raise UnrepresentableInputError(msg)
                    self._validate_json_value_keys(value)
            case list() | set():
                for item in data:
                    self._validate_json_value_keys(item)
            case _:
                return

    def validate_spec_for_data(self, data: Value) -> None:
        """Validate the spec against the data.

        When :attr:`json_type` is active, walk *data* to reject non-
        string dict keys, which JSON objects cannot represent.
        """
        if self._json_type_active:
            self._validate_json_value_keys(data)

    def _validate_record_naming(self) -> None:
        """Validate ``record_shape_names`` for PascalCase identifier
        shape, collisions with the auto-generated ``{prefix}{N}``
        struct names, and duplicate target names.

        Ported from
        :meth:`literalizer.languages.Rust._validate_record_naming`.
        Kotlin has no ``heterogeneous_value_enum_name`` so that
        collision check does not apply, and Rust's reserved-keyword
        check is unnecessary here: every Kotlin keyword is lowercase,
        so the PascalCase requirement already rejects every one of
        them.
        """
        prefix = self.record_struct_name_prefix
        auto_name_pattern = re.compile(
            pattern=rf"^{re.escape(pattern=prefix)}\d+$",
        )
        seen_names: set[str] = set()
        for keys, name in self.record_shape_names.items():
            if not _PASCAL_CASE_IDENTIFIER.match(string=name):
                msg = (
                    f"record_shape_names entry for keys {sorted(keys)!r} "
                    f"maps to {name!r}, which is not a PascalCase Kotlin "
                    f"identifier."
                )
                raise InvalidRecordNameError(msg)
            if auto_name_pattern.match(string=name):
                msg = (
                    f"record_shape_names entry for keys {sorted(keys)!r} "
                    f"maps to {name!r}, which collides with the "
                    f"auto-generated {prefix!r}-prefixed struct names."
                )
                raise InvalidRecordNameError(msg)
            if name in seen_names:
                msg = (
                    f"record_shape_names maps multiple key-sets to "
                    f"{name!r}; struct names must be unique."
                )
                raise InvalidRecordNameError(msg)
            seen_names.add(name)

    @cached_property
    def format_string(self) -> Callable[[str], str]:
        """Format a string value as a quoted literal."""
        return format_string_backslash_dollar

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
            return _format_kotlin_json_assignment
        return variable_formatter(template="{name} = {value}")

    @cached_property
    def _kotlin_record_scalar_resolver(
        self,
    ) -> Callable[[type | ListType | DictType], str | None]:
        """Type-only scalar resolver (the mapping the typed openers are
        built on); returns ``None`` for a type it does not cover so
        callers can fall back to the ``Any?`` top type.
        """
        return self._opener_config.element_to_type(
            list_template=None,
            enable_list_type=False,
            date_type=None,
            datetime_type=None,
            enable_dict_type=False,
            dict_key_type="",
        )

    def _kotlin_record_datetime_type(
        self,
        value: datetime.datetime,
        /,
    ) -> str:
        """Kotlin type for a :class:`datetime.datetime` record field.

        A record component must match the literal the formatter emits,
        so it is driven by the chosen datetime format: ``ISO`` renders a
        quoted string (``String``); ``EPOCH`` renders the epoch seconds
        as a bare integer that overflows Kotlin's signed 32-bit ``Int``
        after 2038-01-19, so the component widens to ``Long`` exactly
        when the value leaves that range (the same ``Int``/``Long``
        formula a plain integer field uses); the default ``KOTLIN``
        format renders a ``LocalDateTime.of(...)`` call.  It stays
        value-driven rather than a pure ``cached_property``.
        """
        produced = self.datetime_format.value.type_produced
        if produced is str:
            return "String"
        if produced is int:
            epoch = datetime_epoch_seconds(value=value)
            in_i32 = _KOTLIN_I32_MIN <= epoch <= _KOTLIN_I32_MAX
            return "Int" if in_i32 else "Long"
        return "LocalDateTime"

    def _kotlin_record_field_type(self, request: RecordFieldType, /) -> str:
        """Return the Kotlin ``data class`` field type for a record
        field, derived structurally from the raw value.

        A field whose value is itself a nested record-shaped dict uses
        that record's generated name.  A list or ordered-map field
        derives its type from the very collection opener the value
        formatter uses for that value (a record field is formatted with
        no sibling override, so the opener equals the one emitted),
        resolved by :func:`_kotlin_opener_to_type`.  ``Int`` magnitude
        (``Int`` vs ``Long``) and the format-dependent ``datetime`` type
        are value- and spec-driven, so they are resolved explicitly;
        every other scalar (including ``date`` -> ``LocalDate`` and
        ``bytes`` -> ``String``) goes through the shared type-only
        resolver.

        A record-eligible dict with no ``record_name`` was widened out
        of record inference because its nested sibling maps cannot
        share one shape.  Type that field as ``Map<String, Any?>`` so
        the uniform enclosing record survives (#2914).  A set or a
        genuinely non-record dict (empty or non-string-keyed) still has
        no precise component type; per the cross-language decision in
        #2317, Kotlin folds it into the ``Any?`` top type.
        """
        if request.record_name is not None:
            return request.record_name
        return self._kotlin_value_field_type(request.value)

    def _kotlin_value_field_type(  # noqa: PLR0911  # pylint: disable=too-complex
        self,
        value: Value,
        /,
    ) -> str:
        """Resolve the Kotlin field type for a raw (non-nested-record)
        value, descending into an ``arrayOf(`` element type.
        """
        match value:
            case None:
                return "Any?"
            case bool():
                return "Boolean"
            case int() if not I64_MIN <= value <= I64_MAX:
                return "BigInteger"
            case int():
                in_i32 = _KOTLIN_I32_MIN <= value <= _KOTLIN_I32_MAX
                return "Int" if in_i32 else "Long"
            case datetime.datetime():
                return self._kotlin_record_datetime_type(value)
            case OrderedMap():
                return _kotlin_opener_to_type(
                    self.ordered_map_format_config.ordered_map_open(value),
                )
            case dict() if record_shape_for_dict(value=value) is not None:
                return "Map<String, Any?>"
            case list():
                opener = self.sequence_open(value)
                if opener == "arrayOf(":
                    element = self._kotlin_value_field_type(value[0])
                    return f"Array<{element}>"
                return _kotlin_opener_to_type(opener)
            case _:
                return self._kotlin_record_scalar_resolver(type(value)) or (
                    "Any?"
                )

    def _kotlin_tuple_field_type(self, elements: list[Value], /) -> str:
        """Return the Kotlin ``Pair``/``Triple`` type for a
        tuple-eligible ``RECORD`` field, one type parameter per
        position.

        The length is validated at check time, so *elements* is length
        2 or 3; each position's type reuses
        :meth:`_kotlin_value_field_type` (the same scalar resolution a
        plain field value uses), so e.g. ``[1, "email"]`` types
        ``Pair<Int, String>``.
        """
        elem_types = [self._kotlin_value_field_type(e) for e in elements]
        constructor = {2: "Pair", 3: "Triple"}[len(elements)]
        return f"{constructor}<{', '.join(elem_types)}>"

    @cached_property
    def _record_renderer(self) -> RecordRenderer:
        """Kotlin syntax hooks for the ``RECORD`` strategy."""
        return RecordRenderer(
            name_prefix=self.record_struct_name_prefix,
            record_shape_names=self.record_shape_names,
            field_identifier=_kotlin_record_field_identifier,
            field_type=self._kotlin_record_field_type,
            render_declaration=_kotlin_render_declaration,
            render_literal=_kotlin_record_literal,
        )

    @cached_property
    def _tuple_renderer(self) -> TupleRenderer:
        """Kotlin syntax hooks for the ``TUPLE`` strategy."""
        return TupleRenderer(
            render_literal=_kotlin_tuple_literal,
            field_type=self._kotlin_tuple_field_type,
            representable_arity=_kotlin_tuple_arity_representable,
        )

    @cached_property
    def _record_strategy(self) -> RecordStrategy:
        """Resolve the active strategy to its behavior + preamble."""
        cls = type(self.heterogeneous_strategy)
        if self.heterogeneous_strategy is cls.RECORD:
            return build_record_strategy(
                renderer=self._record_renderer,
                split_conflicting_field_types=True,
                widen_unrecordizable_nested_sibling_maps=True,
                derecordized_map_open="mapOf<String, Any?>(",
            )
        if self.heterogeneous_strategy is cls.TUPLE:
            return build_tuple_strategy(
                record_renderer=self._record_renderer,
                tuple_renderer=self._tuple_renderer,
            )
        return RecordStrategy(
            behavior=NO_HETEROGENEOUS_BEHAVIOR,
            preamble=no_data_preamble,
        )

    @cached_property
    def data_dependent_preamble(self) -> Callable[[Value], tuple[str, ...]]:
        """Return data-dependent preamble lines.

        Always emits ``import java.math.BigInteger`` when the data
        carries an out-of-range integer; under
        ``HeterogeneousStrategies.RECORD`` additionally emits one
        ``data class`` declaration per record shape present in the data.
        When :attr:`json_type` is active neither applies: integers
        outside the 64-bit range ride inside the JSON text, and the
        data flows through a single ``Json.parseToJsonElement`` call
        instead of typed records.
        """
        if self._json_type_active:
            return no_data_preamble
        record_preamble = self._record_strategy.preamble

        def _preamble(data: Value, /) -> tuple[str, ...]:
            """Combine the BigInteger import with record declarations."""
            return _kotlin_biginteger_preamble(data) + record_preamble(data)

        return _preamble

    @cached_property
    def heterogeneous_behavior(self) -> HeterogeneousBehavior:
        """Return the behavior for the chosen heterogeneous strategy."""
        if self._json_type_active:
            return dataclasses.replace(
                NO_HETEROGENEOUS_BEHAVIOR,
                skip_scalar_checks=True,
            )
        return self._record_strategy.behavior

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
        return _kotlin_call_stub

    @cached_property
    def format_call_preamble_stub(
        self,
    ) -> Callable[
        [Sequence[str], Sequence[str], StubReturn, Sequence[Value]],
        tuple[str, ...],
    ]:
        """Return file-scope stubs for a call expression."""
        return no_call_stub

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
        """Rewrite a ``{"$ref": "name"}`` identifier into the
        language's call expression syntax.
        """
        return identity_call_ref_identifier

    @cached_property
    def format_call_arg_ref_identifier(
        self,
    ) -> Callable[[str, Value | None], str]:
        """Rewrite a ``{"$ref": "name"}`` identifier in a call-argument
        context.

        Delegates to :attr:`format_call_ref_identifier`.  Override this to
        allow call-argument ``$ref`` values that would otherwise be rejected.
        """
        return self.format_call_ref_identifier

    @cached_property
    def format_call_arg_ref_identifier_consumable(
        self,
    ) -> Callable[[str, Value | None], str]:
        """Format a ``$ref`` the caller authorized as consumable.

        Delegates to :attr:`format_call_arg_ref_identifier`.  Override
        this to opt into a consuming form (e.g. C++ ``std::move``).
        """
        return self.format_call_arg_ref_identifier

    @cached_property
    def consumable_ref_value_inhibits_consuming_form(
        self,
    ) -> Callable[[Value], bool]:
        """Predicate deciding whether a ref's underlying value type
        inhibits the consume form.

        Delegates to :data:`never_inhibits_consuming_form`.  Languages
        whose consume operator rejects certain value types (notably
        the Mojo ``^`` on register-trivial scalars) override this.
        """
        return never_inhibits_consuming_form

    @cached_property
    def _date_type_name(self) -> str | None:
        """Resolved Kotlin type name for the chosen date format."""
        return self._opener_config.type_name(
            py_type=self.date_format.value.type_produced,
        )

    @cached_property
    def _dt_type_name(self) -> str | None:
        """Resolved Kotlin type name for the chosen datetime format."""
        return self._opener_config.type_name(
            py_type=self.datetime_format.value.type_produced,
        )

    @cached_property
    def sequence_format_config(self) -> SequenceFormatConfig:
        """Configuration for the chosen sequence format."""
        if self._json_type_active:
            return _JSON_NODE_SEQUENCE_CONFIG
        return self.sequence_format.value

    @cached_property
    def sequence_open(self) -> Callable[[list[Value]], str]:
        """Callable that returns the opening delimiter for a sequence.

        Under any record-rendering strategy (``RECORD``, or ``TUPLE``
        which composes it) a list whose elements are record-shaped
        dicts opens as ``listOf<Any?>(`` (the elements format as
        ``RecordN(...)`` literals, not the ``Map<...>`` the typed
        opener would otherwise infer).
        """
        if self._json_type_active:
            return _JSON_NODE_SEQUENCE_CONFIG.sequence_open
        fmt = self.sequence_format.value
        if fmt.typed_opener_fallback is None:
            base = fmt.sequence_open
        else:
            base = _kotlin_list_sequence_open(
                cfg=self._opener_config,
                date_type=self._date_type_name,
                datetime_type=self._dt_type_name,
                dict_key_type=self.default_dict_key_type,
            )
        # ``RECORD`` and ``TUPLE`` (which composes ``RECORD``) both set
        # ``render_record_literal``; ``ERROR`` does not.  Keying off the
        # behavior rather than the enum member keeps the two
        # record-rendering strategies in step.
        if self.heterogeneous_behavior.render_record_literal is None:
            return base
        any_open = "listOf<Any?>("

        def _open(items: list[Value], /) -> str:
            """Use ``listOf<Any?>(`` for lists of record-shaped dicts."""
            if any(
                isinstance(item, dict) and not isinstance(item, OrderedMap)
                for item in items
            ):
                return any_open
            return base(items)

        return _open

    @cached_property
    def set_format_config(self) -> SetFormatConfig:
        """Configuration for the chosen set format."""
        if self._json_type_active:
            return _JSON_NODE_SET_CONFIG
        base = self.set_format(default_type=self.default_set_element_type)
        openers = self._opener_config.build(
            date_type=self._date_type_name,
            datetime_type=self._dt_type_name,
            set_opener_template=base.set_opener_template or None,
            narrow_dict_values=False,
            dict_key_type=self.default_dict_key_type,
        )
        return base.with_typed_opener(
            type_to_opener=openers.set,
            fallback=base.set_open([]),
        )

    @cached_property
    def _kotlin_dict_value_type(
        self,
    ) -> Callable[[type | ListType | DictType], str | None]:
        """Resolve a dict value's Kotlin type name to match the renderer.

        Kotlin's dict opener previously disabled value narrowing entirely
        (its base list template renders as an ``Array`` type, which does
        not match the real ``List`` sequence rendering, so narrowing list
        values would give them the wrong type).  That left a map value
        typed ``Any?`` where a nested ``Map<...>`` was declared, so a map
        used as e.g. a sequence element did not compile (#2890).

        Delegates to :func:`_kotlin_dict_value_type_name`, which narrows
        only ``DictType`` values and keeps the prior ``Array``/``Any?``
        list typing for everything else.
        """
        base_resolver = self._opener_config.element_to_type(
            list_template=None,
            enable_list_type=True,
            date_type=self._date_type_name,
            datetime_type=self._dt_type_name,
            enable_dict_type=False,
            dict_key_type=self.default_dict_key_type,
        )
        key_type = self.default_dict_key_type
        fallback = self.default_dict_value_type

        def resolve(element_type: type | ListType | DictType) -> str | None:
            """Map an element type to its rendered Kotlin type name."""
            return _kotlin_dict_value_type_name(
                element_type=element_type,
                base_resolver=base_resolver,
                key_type=key_type,
                fallback=fallback,
            )

        return resolve

    @cached_property
    def dict_format_config(self) -> DictFormatConfig:
        """Configuration for dict formatting."""
        if self._json_type_active:
            return _JSON_NODE_DICT_CONFIG
        resolved_dict_opener = self.dict_format.value.opener_template.replace(
            "{key_type}",
            self.default_dict_key_type,
        )
        return DictFormatConfig(
            dict_open=typed_dict_open(
                type_to_opener=make_type_to_opener(
                    # A dict value that is itself a map keeps its
                    # ``Map<String, ...>`` type instead of collapsing to
                    # the ``Any?`` fallback, so a map used where a nested
                    # map type is declared (e.g. a sequence element)
                    # matches that type (#2890); other value types keep
                    # their prior typing.  See
                    # :meth:`_kotlin_dict_value_type`.
                    element_to_type=self._kotlin_dict_value_type,
                    opener_template=resolved_dict_opener,
                ),
                fallback=resolved_dict_opener.format(
                    type_name=self.default_dict_value_type,
                ),
            ),
            narrowed_open=None,
            supports_trailing_comma=True,
            close=")",
            format_entry=dict_entry_with_separator(
                separator=" to ",
                format_value=passthrough_sequence_entry,
            ),
            empty_dict=None,
            preamble_lines=(),
            narrowed_empty_form=None,
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
    def format_time(self) -> Callable[[datetime.time], str]:
        """Callable that formats a time as a string literal."""
        return format_time_local_time_of

    @cached_property
    def format_float(self) -> Callable[[float], str]:
        """Callable that formats a float value as a literal."""
        return self.float_format

    @cached_property
    def format_integer(self) -> Callable[[int], str]:
        """Callable that formats an int value as a literal."""
        return make_overflow_fallback_formatter(
            base=self.integer_format.get_formatter(
                numeric_separator=self.numeric_separator,
            ),
            fallback=_format_kotlin_biginteger_literal,
            min_value=I64_MIN,
            max_value=I64_MAX,
        )

    @cached_property
    def format_integer_widened(self) -> Callable[[int], str]:
        """Always-``L``-suffixed integer formatter for widened
        collections (mixed-magnitude int sets/lists).
        """
        base = self.integer_format.get_formatter(
            numeric_separator=self.numeric_separator,
        )
        return make_overflow_fallback_formatter(
            base=make_long_suffix_formatter(base=base),
            fallback=_format_kotlin_biginteger_literal,
            min_value=I64_MIN,
            max_value=I64_MAX,
        )

    @cached_property
    def format_integer_beyond_i64(self) -> Callable[[int], str]:
        """Always-``BigInteger`` formatter for collections that exceed
        signed 64-bit range.
        """
        return _format_kotlin_biginteger_literal

    @cached_property
    def comment_config(self) -> CommentConfig:
        """Configuration for the language's comment syntax."""
        return self.comment_format.value

    @cached_property
    def ordered_map_format_config(self) -> OrderedMapFormatConfig:
        """Configuration for ordered-map formatting."""
        if self._json_type_active:
            return _JSON_NODE_ORDERED_MAP_CONFIG
        return OrderedMapFormatConfig(
            ordered_map_open=fixed_open(
                open_str=(
                    f"linkedMapOf<{self.default_dict_key_type}"
                    f", {self.default_dict_value_type}>("
                )
            ),
            close=")",
            preamble_lines=(),
        )

    @cached_property
    def format_ordered_map_entry(self) -> Callable[[str, Value, str], str]:
        """Callable that formats one ordered-map entry."""
        return dict_entry_with_separator(
            separator=" to ",
            format_value=passthrough_sequence_entry,
        )

    @cached_property
    def format_variable_declaration(
        self,
    ) -> Callable[[str, str, Value, frozenset[enum.Enum]], str]:
        """Callable that formats a new variable declaration."""
        if self._json_type_active:
            return _make_format_kotlin_json_declaration(
                keyword=self.declaration_style.name.lower(),
            )
        return self.variable_type_hints.formatter(
            auto_formatter=self.declaration_style.value.formatter,
            keyword=self.declaration_style.name.lower(),
            date_hint=(
                "String"
                if self.date_format.value.type_produced is str
                else "LocalDate"
            ),
            datetime_hint=(
                "Long"
                if self.datetime_format.value.type_produced is int
                else (
                    "String"
                    if self.datetime_format.value.type_produced is str
                    else "LocalDateTime"
                )
            ),
            default_set_element_type=self.default_set_element_type,
            default_dict_key_type=self.default_dict_key_type,
            default_dict_value_type=self.default_dict_value_type,
            dict_outer=(
                "HashMap" if self.dict_format.name == "HASH_MAP" else "Map"
            ),
            set_outer=(
                "MutableSet" if self.set_format.name == "SORTED_SET" else "Set"
            ),
            sequence_format_name=self.sequence_format.name,
        )

    @cached_property
    def scalar_preamble(self) -> dict[type, tuple[str, ...]]:
        """Per-instance scalar preamble computed from date/datetime format.

        Under :attr:`json_type` every temporal value is folded into the
        JSON text as an ISO-8601 string, so the temporal Kotlin imports
        that the configured ``date_format`` / ``datetime_format`` would
        otherwise add do not apply.
        """
        if self._json_type_active:
            return {}
        return date_scalar_preamble(
            date_format=self.date_format,
            datetime_format=self.datetime_format,
            extra={datetime.time: ("import java.time.LocalTime",)},
        )

    @cached_property
    def scalar_body_preamble(self) -> dict[type, tuple[str, ...]]:
        """Per-instance scalar body preamble (Kotlin needs none)."""
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
        config: CallStyle = self.call_style.value
        return config
