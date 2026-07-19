"""Mojo language specification."""

import dataclasses
import datetime
import enum
import textwrap
from collections.abc import Callable, Sequence
from functools import cached_property, partial
from typing import ClassVar, assert_never

from beartype import beartype

from literalizer._formatters.collection_openers import (
    fixed_open,
    make_element_to_type,
    make_narrowed_empty_form,
    make_type_to_opener,
)
from literalizer._formatters.format_dates import (
    format_date_iso,
    format_datetime_epoch,
    format_datetime_iso,
    format_time_iso,
)
from literalizer._formatters.format_entries import (
    dict_entry_with_separator,
    format_bytes_base64,
    format_bytes_hex,
    passthrough_sequence_entry,
    passthrough_set_entry,
    variable_formatter,
)
from literalizer._formatters.format_factories import (
    dict_format_factory,
    set_format_factory,
)
from literalizer._formatters.format_floats import (
    format_float_fixed,
    format_float_repr,
    format_float_scientific,
)
from literalizer._formatters.format_strings import format_string_backslash
from literalizer._formatters.type_inference import infer_element_type
from literalizer._heterogeneous import (
    collect_heterogeneous_container_ids,
    collect_sibling_map_wrap_ids,
    iter_wrapped_scalars,
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
    LanguageCls,
    ModifierCombination,
    NestedMapWideningVariant,
    OrderedMapFormatConfig,
    PositionalCallStyle,
    SequenceFormatConfig,
    SetFormatConfig,
    StubReturn,
    TrailingCommaConfig,
    VariantMetadata,
    body_preamble_from_scalars,
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
    no_data_preamble,
    no_format_integer_beyond_i64,
    no_format_integer_widened,
    no_leading_preamble,
    no_type_hint_preamble,
    no_validate_call_arg,
    no_validate_spec_for_data,
    prepend_body_preamble,
)
from literalizer._types import Scalar, Value
from literalizer.exceptions import (
    HeterogeneousScalarCollectionError,
    NullInCollectionError,
)

_mojo_element_to_type = make_element_to_type(
    str_type="String",
    bool_type="Bool",
    int_type="Int",
    float_type="Float64",
    mixed_numeric_type="String",
    bytes_type="String",
    date_type="String",
    datetime_type="String",
    time_type="String",
    list_template="List[{inner}]",
    enable_list_type=True,
    dict_type_template="Dict[String, {inner}]",
    fallback_value_type="String",
    wide_int_type=None,
    beyond_i64_type=None,
)

# Strict resolver for call-argument typing: omits ``fallback_value_type``
# so an unresolvable dict-value type (e.g. a nested
# ``DictType(value_type=None)`` produced when the ``VARIANT``
# heterogeneous strategy lets a mixed-value dict reach the typed-stub
# helper) returns ``None`` instead of silently lying with
# ``Dict[String, String]``.
_mojo_call_arg_element_to_type = make_element_to_type(
    str_type="String",
    bool_type="Bool",
    int_type="Int",
    float_type="Float64",
    mixed_numeric_type="String",
    bytes_type="String",
    date_type="String",
    datetime_type="String",
    time_type="String",
    list_template="List[{inner}]",
    enable_list_type=True,
    dict_type_template="Dict[String, {inner}]",
    fallback_value_type=None,
    wide_int_type=None,
    beyond_i64_type=None,
)


@beartype
def _value_to_mojo_type(
    value: Value,
    /,
    *,
    heterogeneous_value_type: str | None,
    wrap_ids: frozenset[int],
) -> str | None:
    """Map one call-argument value to its Mojo type string.

    Routes list values through :func:`infer_element_type` so a list
    slot resolves to a recursive ``List[...]`` type (e.g.
    ``[1, 2, 3]`` -> ``List[Int]``).  Dicts route the same way so a
    homogeneous-value dict slot resolves to ``Dict[String, ...]``
    (e.g. ``{"a": 1}`` -> ``Dict[String, Int]``).  Uses the strict
    resolver so a dict whose values cannot be unified to a
    concrete Mojo type (an empty dict, or a nested heterogeneous dict
    that survives upstream checks under the ``VARIANT`` strategy)
    returns ``None`` and the slot falls back to the generic
    ``[*Ts: AnyType](*args: *Ts)`` form rather than fabricating a
    ``String`` value type.  When *heterogeneous_value_type* is given
    (the ``VARIANT`` strategy supplies the configured Variant alias
    name) a heterogeneous-value dict slot resolves to
    ``Dict[String, {alias}]`` instead of falling back.  Other values
    look up their Python ``type`` directly so only the scalar Mojo
    mappings are typed and any other shape (ordered maps, etc.) falls
    back to the same generic form.
    """
    match value:
        case list():
            return _mojo_call_arg_element_to_type(
                infer_element_type(items=[value]) or list,
            )
        case dict():
            if heterogeneous_value_type is not None and id(value) in wrap_ids:
                return f"Dict[String, {heterogeneous_value_type}]"
            return _mojo_call_arg_element_to_type(
                infer_element_type(items=[value]) or dict,
            )
        case _:
            return _mojo_call_arg_element_to_type(type(value))


@beartype
def _gather_mojo_call_slots(
    *,
    arg_values: Sequence[Value],
) -> list[list[Value]]:
    """Group per-call argument values by positional slot."""
    slots: list[list[Value]] = []
    for element in arg_values:
        match element:
            case list():
                per_arg: Sequence[Value] = element
            case _:
                per_arg = [element]
        for slot_index, arg_value in enumerate(iterable=per_arg):
            if slot_index >= len(slots):
                slots.append([])
            slots[slot_index].append(arg_value)
    return slots


@beartype
def _slot_is_all_scalars(*, slot_values: Sequence[Value]) -> bool:
    """Return ``True`` when every value at this slot is a scalar."""
    return all(not isinstance(v, list | dict | set) for v in slot_values)


@dataclasses.dataclass(frozen=True, kw_only=True)
class _MojoSlotSignature:
    """Per-slot resolved type info for a Mojo typed param list.

    ``known_types`` is the frozenset of concrete Mojo type strings
    resolved at this slot across calls; ``None`` entries (unresolvable
    values) are dropped, so a slot whose only values are unresolvable
    has an empty ``known_types``.
    """

    name: str
    known_types: frozenset[str]


@dataclasses.dataclass(frozen=True, kw_only=True)
class _MojoSlotInfo:
    """Aggregate result of computing Mojo per-slot signatures.

    ``typed_params`` is the formatted ``("name: Type", ...)`` tuple
    consumed by the call-stub typed-param emitter, or ``None`` when the
    caller must fall back to the generic
    ``[*Ts: AnyType](*args: *Ts)`` form.  ``slots`` carries per-slot
    metadata: aligned with ``params`` when ``typed_params`` is a tuple,
    a prefix up to and including the slot that triggered fallback when
    fallback happened mid-analysis, and empty when the input slot count
    does not match ``params``.
    """

    typed_params: tuple[str, ...] | None
    slots: tuple[_MojoSlotSignature, ...]


@beartype
def _mojo_compute_slot_signatures(
    *,
    params: Sequence[str],
    arg_values: Sequence[Value],
    heterogeneous_value_type: str | None,
) -> _MojoSlotInfo:
    """Compute Mojo slot signatures and the typed-param list.

    Returns a :class:`_MojoSlotInfo` whose ``typed_params`` mirrors the
    behavior previously implemented by ``_mojo_typed_param_list``: it
    is ``None`` to signal the caller should fall back to the generic
    ``[*Ts: AnyType](*args: *Ts)`` form.  Falls back when any per-call
    value at a parameter slot has no Mojo type (a ref-marker dict,
    ``None``, an inhomogeneous list, etc.) or when any slot has no
    values (e.g. transform-stub callers pass an empty ``arg_values``).
    A zero-parameter call returns ``()`` (typed, empty) so the caller
    emits a bare ``def name():`` form rather than the generic stub.

    When concrete Mojo types are known at every per-call value but
    diverge across calls at one slot, the behavior depends on the
    heterogeneous strategy: ``ERROR`` raises
    :exc:`HeterogeneousScalarCollectionError` so the call-stub path
    refuses input it cannot represent; ``VARIANT`` (signaled by a
    non-``None`` ``heterogeneous_value_type``) emits the configured
    Variant alias as the slot type regardless of whether the divergent
    values are scalars, lists, or a mix of the two.

    The ``slots`` field exposes the per-slot ``known_types`` set and
    ``all_scalars`` flag so future callers (e.g. a body-preamble
    builder that unions per-slot Variant alternatives with data-driven
    alternatives) can reuse this analysis without recomputing it.
    """
    if not params:
        return _MojoSlotInfo(typed_params=(), slots=())
    slots = _gather_mojo_call_slots(arg_values=arg_values)
    if len(slots) != len(params):
        return _MojoSlotInfo(typed_params=None, slots=())
    wrap_ids = (
        frozenset[int]().union(
            *(
                collect_heterogeneous_container_ids(data=slot_values)
                for slot_values in slots
            )
        )
        if heterogeneous_value_type is not None
        else frozenset[int]()
    )
    typed: list[str] = []
    slot_signatures: list[_MojoSlotSignature] = []
    for name, slot_values in zip(params, slots, strict=True):
        slot_types = [
            _value_to_mojo_type(
                v,
                heterogeneous_value_type=heterogeneous_value_type,
                wrap_ids=wrap_ids,
            )
            for v in slot_values
        ]
        known_types: frozenset[str] = frozenset(
            t for t in slot_types if t is not None
        )
        slot_signatures.append(
            _MojoSlotSignature(
                name=name,
                known_types=known_types,
            ),
        )
        if len(known_types) > 1 and heterogeneous_value_type is not None:
            typed.append(f"{name}: {heterogeneous_value_type}")
            continue
        if not slot_types or None in slot_types:
            return _MojoSlotInfo(
                typed_params=None,
                slots=tuple(slot_signatures),
            )
        if len(known_types) > 1:
            msg = (
                "Mojo call argument types diverge across calls at "
                f"parameter '{name}' "
                f"(got {sorted(known_types)}); "
                "the default ERROR heterogeneous_strategy cannot "
                "represent this input."
            )
            raise HeterogeneousScalarCollectionError(msg)
        (mojo_type,) = known_types
        typed.append(f"{name}: {mojo_type}")
    return _MojoSlotInfo(
        typed_params=tuple(typed),
        slots=tuple(slot_signatures),
    )


@beartype
def _mojo_typed_param_list(
    *,
    params: Sequence[str],
    arg_values: Sequence[Value],
    heterogeneous_value_type: str | None,
) -> tuple[str, ...] | None:
    """Return ``("name: Type", ...)`` for a typed Mojo signature.

    Thin wrapper over :func:`_mojo_compute_slot_signatures` that
    surfaces only the ``typed_params`` field.  See that function for
    the full contract (fallback conditions, divergent-slot handling
    under each heterogeneous strategy, zero-parameter behavior).
    """
    info = _mojo_compute_slot_signatures(
        params=params,
        arg_values=arg_values,
        heterogeneous_value_type=heterogeneous_value_type,
    )
    return info.typed_params


@beartype
def _mojo_cross_call_scalar_wrap_ids(
    slot_values: Sequence[Value],
) -> frozenset[int]:
    """Return ids of scalars in a cross-call divergent VARIANT slot.

    When *slot_values* are all scalars whose Mojo Variant buckets
    diverge across calls, return a ``frozenset`` of their ``id()`` so
    the call-argument formatter wraps each as ``Value(...)``.  Returns
    an empty ``frozenset`` for empty slots, homogeneous slots, and
    slots that mix scalars with lists, dicts, or sets — Mojo can
    construct the ``Variant`` implicitly from a moved typed variable
    in those cases, and an inline list / dict literal cannot be wrapped
    by ``Value(...)`` without an intermediate typed declaration that
    the call-argument formatter does not synthesize.
    """
    if not slot_values or not _slot_is_all_scalars(slot_values=slot_values):
        return frozenset()
    slot_types = {
        _value_to_mojo_type(
            value,
            heterogeneous_value_type=None,
            wrap_ids=frozenset[int](),
        )
        for value in slot_values
    }
    if len(slot_types) <= 1:
        return frozenset()
    return frozenset(id(value) for value in slot_values)


@beartype
def _mojo_init_expr(parts: Sequence[str]) -> str:
    """Return the constructor expression for a multi-part call target.

    For a 2-part target like ``throttler.check``, returns
    ``_ThrottlerType()``.  For a 3-part target like
    ``app.client.fetch``, returns ``_AppType(_ClientType())``.
    ``@fieldwise_init`` generates a field-by-field init, so each struct
    that holds a field is constructed by passing the inner instance.
    """
    root = parts[0]
    fields = parts[1:-1]
    root_type = f"_{root.capitalize()}Type"
    if not fields:
        return f"{root_type}()"
    inner_type = f"_{fields[-1].capitalize()}Type"
    expr = f"{inner_type}()"
    for i in range(len(fields) - 2, -1, -1):
        curr_type = f"_{fields[i].capitalize()}Type"
        expr = f"{curr_type}({expr})"
    return f"{root_type}({expr})"


@beartype
def _mojo_call_stub(
    parts: Sequence[str],
    _params: Sequence[str],
    _stub_return: StubReturn,
    _args: Sequence[Value],
    /,
) -> tuple[str, ...]:
    """Return Mojo body stub declarations for a call name.

    1-part names (e.g. ``process``) are handled entirely in the file-
    scope preamble stub; the body stub is empty.  Multi-part names
    (e.g. ``app.client.fetch``) need a ``var`` declaration inside
    ``def main()`` to instantiate the root object.
    """
    if len(parts) == 1:
        return ()
    root = parts[0]
    init_expr = _mojo_init_expr(parts=parts)
    return (f"var {root} = {init_expr}",)


@beartype
def _mojo_call_preamble_stub(
    parts: Sequence[str],
    params: Sequence[str],
    stub_return: StubReturn,
    args: Sequence[Value],
    /,
    *,
    indent: str,
    heterogeneous_value_type: str | None,
) -> tuple[str, ...]:
    """Return Mojo file-scope stubs for a call name.

    1-part names become a module-level ``def``; multi-part names become
    ``@fieldwise_init`` struct types whose innermost type holds the
    method.  Both stub kinds emit typed per-parameter signatures when
    every call's argument values at each slot resolve to the same
    Mojo type (a scalar, a recursive ``List[...]``, or a homogeneous
    ``Dict[String, ...]``), and the generic
    ``[*Ts: AnyType](*args: *Ts)`` form otherwise.

    When *stub_return* is :attr:`StubReturn.VALUE` (the call result feeds
    a surrounding ``call_transform`` wrapper), the inner stub is given
    an explicit ``-> None`` return annotation.  No per-call inference is
    available (the transform is a plain string wrapper), so ``None`` is
    used as a documented placeholder: it is always valid, the body stays
    ``pass``, and the surrounding generic ``[*Ts: AnyType]`` wrapper
    accepts it.  ``None`` also avoids ``-Werror`` ``value is unused``
    diagnostics when the transform is the identity (no outer wrapper),
    because the bare call has no value to leak.
    """
    typed_params = _mojo_typed_param_list(
        params=params,
        arg_values=args,
        heterogeneous_value_type=heterogeneous_value_type,
    )
    return_suffix = " -> None" if stub_return is StubReturn.VALUE else ""
    if len(parts) == 1:
        if typed_params is not None:
            param_list = ", ".join(typed_params)
            return (
                f"def {parts[0]}({param_list}){return_suffix}:\n{indent}pass",
            )
        return (
            f"def {parts[0]}[*Ts: AnyType](*args: *Ts)"
            f"{return_suffix}:\n{indent}pass",
        )
    root = parts[0]
    method = parts[-1]
    fields = parts[1:-1]
    struct_header = "(Copyable, Movable)"
    if typed_params is not None:
        method_param_list = ", ".join(("self", *typed_params))
        method_stub = (
            f"{indent}def {method}({method_param_list})"
            f"{return_suffix}:\n{indent}{indent}pass"
        )
    else:
        method_stub = (
            f"{indent}def {method}[*Ts: AnyType](self, *args: *Ts)"
            f"{return_suffix}:\n{indent}{indent}pass"
        )
    if not fields:
        type_name = f"_{root.capitalize()}Type"
        return (
            f"@fieldwise_init\n"
            f"struct {type_name}{struct_header}:\n"
            f"{method_stub}",
        )
    blocks: list[str] = []
    inner_type = f"_{fields[-1].capitalize()}Type"
    blocks.append(
        f"@fieldwise_init\nstruct {inner_type}{struct_header}:\n{method_stub}"
    )
    prev_type = inner_type
    for i in range(len(fields) - 2, -1, -1):
        curr_type = f"_{fields[i].capitalize()}Type"
        field = fields[i + 1]
        blocks.append(
            f"@fieldwise_init\n"
            f"struct {curr_type}{struct_header}:\n"
            f"{indent}var {field}: {prev_type}"
        )
        prev_type = curr_type
    root_type = f"_{root.capitalize()}Type"
    blocks.append(
        f"@fieldwise_init\n"
        f"struct {root_type}{struct_header}:\n"
        f"{indent}var {fields[0]}: {prev_type}"
    )
    return ("\n".join(blocks),)


_mojo_narrowed_empty_form = make_narrowed_empty_form(
    element_to_type=_mojo_element_to_type,
    template="List[{type}]()",
    fallback_type="String",
)


@beartype
def _format_mojo_ordered_map_entry(
    key: str,
    _raw_value: Value,
    formatted_value: str,
) -> str:
    """Format one Mojo ordered-map entry as a ``Tuple(key, value)``."""
    return f"Tuple({key}, {formatted_value})"


_VARIANT_PAYLOAD_VALUE_PLACEHOLDER = "{value}"


@dataclasses.dataclass(frozen=True)
class _VariantSignature:
    """Mojo ``Variant`` alternative for one scalar bucket.

    ``type_name`` is the Mojo type listed in the ``Variant[...]`` alias
    (e.g. ``"Bool"``, ``"Int"``, ``"String"``, ``"NoneType"``).
    ``payload_template`` is the expression rendered between the outer
    ``Value(...)`` parentheses; occurrences of ``{value}`` are replaced
    with the formatted scalar, and a template without the placeholder
    (e.g. ``"NoneType()"``) ignores the formatted scalar entirely.
    """

    type_name: str
    payload_template: str


_INT_VARIANT_SIGNATURE = _VariantSignature(
    type_name="Int",
    payload_template=_VARIANT_PAYLOAD_VALUE_PLACEHOLDER,
)
_STRING_VARIANT_SIGNATURE = _VariantSignature(
    type_name="String",
    payload_template="String({value})",
)


@beartype
def _mojo_variant_for_scalar(
    value: Scalar,
    /,
    *,
    datetime_type_produced: type,
) -> _VariantSignature:
    """Return the Mojo Variant alternative for *value*.

    Strings, bytes, dates, and times all map to ``String`` because
    those formatters produce ISO strings or hex/base64 strings.
    Datetimes follow the configured datetime format: ISO-rendered
    datetimes map to ``String`` while ``EPOCH`` datetimes map to
    ``Int``.  ``None`` maps to ``NoneType`` and renders as
    ``Value(NoneType())`` because the ``Variant`` constructor in Mojo
    cannot infer ``NoneType`` from the bare ``None`` literal.
    """
    match value:
        case bool():
            return _VariantSignature(
                type_name="Bool",
                payload_template=_VARIANT_PAYLOAD_VALUE_PLACEHOLDER,
            )
        case int():
            return _INT_VARIANT_SIGNATURE
        case float():
            return _VariantSignature(
                type_name="Float64",
                payload_template="Float64({value})",
            )
        case datetime.datetime() if datetime_type_produced is int:
            return _INT_VARIANT_SIGNATURE
        case (
            str()
            | bytes()
            | datetime.datetime()
            | datetime.date()
            | datetime.time()
        ):
            return _STRING_VARIANT_SIGNATURE
        case None:
            return _VariantSignature(
                type_name="NoneType",
                payload_template="NoneType()",
            )
        case _ as unreachable:
            assert_never(unreachable)


_REGISTER_TRIVIAL_VARIANT_TYPE_NAMES: frozenset[str] = frozenset(
    {"Bool", "Int", "Float64"},
)
"""Mojo ``Variant`` type-name buckets that map to register-trivial
scalars.  Applying the ``^`` transfer operator to one of these is a
hard error under ``--Werror`` in Mojo 0.26.1.0+.
"""


@beartype
def _mojo_value_inhibits_consuming_form(
    value: Value, /, *, datetime_type_produced: type
) -> bool:
    """Return ``True`` when ``^`` is illegal for *value*'s Mojo type.

    Non-scalar values (lists, dicts, sets) and scalars that map to
    non-trivial Mojo types (``String``, ``NoneType``) keep the existing
    consuming-form behavior.
    """
    if isinstance(value, (list, dict, set)):
        return False
    signature = _mojo_variant_for_scalar(
        value, datetime_type_produced=datetime_type_produced
    )
    return signature.type_name in _REGISTER_TRIVIAL_VARIANT_TYPE_NAMES


@dataclasses.dataclass(frozen=True)
class _HeterogeneousStrategyConfig:
    """Configuration for one Mojo heterogeneous-values strategy.

    ``build_behavior`` produces the
    :class:`~literalizer._language.HeterogeneousBehavior` exposed on a
    Mojo instance.  ``build_preamble`` produces the data-dependent
    preamble callable (e.g. the ``Variant`` alias declaration).  Both
    receive the Mojo instance's configurable variant-type name so the
    resulting functions can close over it.
    """

    build_behavior: Callable[[str, type], HeterogeneousBehavior]
    build_preamble: Callable[[str, type], Callable[[Value], tuple[str, ...]]]


@beartype
def _build_error_behavior(
    _variant_name: str, _datetime_type_produced: type, /
) -> HeterogeneousBehavior:
    """ERROR strategy: no wrapping, no skipping of checks."""
    return NO_HETEROGENEOUS_BEHAVIOR


@beartype
def _build_error_preamble(
    _variant_name: str,
    _datetime_type_produced: type,
    /,
) -> Callable[[Value], tuple[str, ...]]:
    """ERROR strategy: no data-dependent preamble."""
    return no_data_preamble


_VARIANT_IMPORT_LINE = "from std.utils.variant import Variant"


@beartype
def _build_variant_behavior(
    variant_name: str,
    datetime_type_produced: type,
    /,
) -> HeterogeneousBehavior:
    """VARIANT strategy: wrap scalars and skip scalar checks."""

    def _compute(data: Value) -> frozenset[int]:
        """Return container ids whose scalar children should wrap."""
        return collect_heterogeneous_container_ids(
            data=data
        ) | collect_sibling_map_wrap_ids(data=data)

    def _wrap(raw_value: Scalar, formatted: str) -> str:
        """Wrap a scalar as ``{variant_name}({payload})`` where the
        payload comes from the signature's ``payload_template`` (with
        ``{value}`` substituted by the formatted scalar).
        """
        signature = _mojo_variant_for_scalar(
            raw_value, datetime_type_produced=datetime_type_produced
        )
        payload = signature.payload_template.replace(
            _VARIANT_PAYLOAD_VALUE_PLACEHOLDER,
            formatted,
        )
        return f"{variant_name}({payload})"

    return HeterogeneousBehavior(
        skip_scalar_checks=True,
        compute_wrap_ids=_compute,
        wrap_scalar=_wrap,
        wrap_non_scalar=None,
        wrap_empty_container=None,
        compute_call_slot_wrap_ids=_mojo_cross_call_scalar_wrap_ids,
        dict_open_for_wrap_ids=None,
        widens_nested_maps_by_wrapping_scalars=True,
        widens_unrecordizable_nested_sibling_maps=False,
        render_record_literal=None,
        compute_record_shapes=None,
        render_tuple_literal=None,
        compute_tuple_list_ids=None,
    )


@beartype
def _collect_variant_alternatives_from_data(
    data: Value, /, *, datetime_type_produced: type
) -> tuple[str, ...]:
    """Return Mojo ``Variant`` alternative type names found in *data*.

    The result is order-preserving and deduplicated.  Returns an empty
    tuple when *data* contains no heterogeneous containers.
    """
    wrap_ids = collect_heterogeneous_container_ids(
        data=data
    ) | collect_sibling_map_wrap_ids(data=data)
    if not wrap_ids:
        return ()
    scalars = iter_wrapped_scalars(data=data, wrap_ids=wrap_ids)
    type_names: list[str] = []
    seen: set[str] = set()
    for scalar in scalars:
        signature = _mojo_variant_for_scalar(
            scalar, datetime_type_produced=datetime_type_produced
        )
        if signature.type_name in seen:
            continue
        seen.add(signature.type_name)
        type_names.append(signature.type_name)
    return tuple(type_names)


@beartype
def _collect_variant_alternatives_from_slots(
    data: Value,
    /,
    *,
    heterogeneous_value_type: str,
) -> tuple[str, ...]:
    """Return Mojo ``Variant`` alternatives from cross-call divergent
    slots.

    Treats *data* as a sequence of per-element call argument lists and
    collects Mojo type names from slots whose resolved types diverge
    across the per-element calls (e.g. ``List[Int]`` vs ``List[String]``
    in slot 0, or ``Int`` vs ``List[Int]``).  Returns an empty tuple
    when *data* is not a list, contains no divergent slot, or every
    divergent slot has an unresolvable value.  The cross-call analysis
    runs unconditionally: a whole-call ``data`` whose top-level shape
    happens to look like a per-element call list will not produce a
    false positive because data-driven scalar-bucket detection covers
    every shape this analysis can flag.
    """
    match data:
        case list():
            slots = _gather_mojo_call_slots(arg_values=data)
        case _:
            return ()
    alternatives: list[str] = []
    seen: set[str] = set()
    for slot_values in slots:
        slot_types: list[str] = []
        for value in slot_values:
            mojo_type = _value_to_mojo_type(
                value,
                heterogeneous_value_type=heterogeneous_value_type,
                wrap_ids=frozenset[int](),
            )
            if mojo_type is not None:
                slot_types.append(mojo_type)
        if len(set(slot_types)) <= 1:
            continue
        for mojo_type in slot_types:
            if mojo_type in seen:
                continue
            seen.add(mojo_type)
            alternatives.append(mojo_type)
    return tuple(alternatives)


@beartype
def _render_variant_preamble(
    alternatives: Sequence[str],
    /,
    *,
    variant_name: str,
) -> tuple[str, ...]:
    """Render the ``Variant`` import + ``comptime`` declaration lines.

    Returns ``()`` when *alternatives* is empty.
    """
    if not alternatives:
        return ()
    joined = ", ".join(alternatives)
    return (
        _VARIANT_IMPORT_LINE,
        f"comptime {variant_name} = Variant[{joined}]",
    )


@beartype
def _build_variant_preamble(
    variant_name: str,
    datetime_type_produced: type,
    /,
) -> Callable[[Value], tuple[str, ...]]:
    """VARIANT strategy: emit the ``Variant`` declaration preamble."""

    def _preamble(data: Value, /) -> tuple[str, ...]:
        """Build the ``Variant`` import + ``comptime`` declaration for
        *data*.  Unions data-driven scalar alternatives with cross-call
        divergent-slot alternatives so call sites whose reference
        arguments carry diverging list or mixed shapes contribute their
        slot types (e.g. ``List[Int]``, ``List[String]``) to the alias.
        """
        data_alternatives = _collect_variant_alternatives_from_data(
            data, datetime_type_produced=datetime_type_produced
        )
        slot_alternatives = _collect_variant_alternatives_from_slots(
            data,
            heterogeneous_value_type=variant_name,
        )
        seen: set[str] = set()
        merged: list[str] = []
        for alternative in data_alternatives + slot_alternatives:
            if alternative in seen:
                continue
            seen.add(alternative)
            merged.append(alternative)
        return _render_variant_preamble(
            tuple(merged),
            variant_name=variant_name,
        )

    return _preamble


@beartype
def _mojo_list_open(items: list[Value]) -> str:
    """Return ``[`` after checking for null elements.

    Mojo cannot infer a list type from null-only elements.
    """
    if any(item is None for item in items):
        msg = (
            f"Mojo's list literal cannot contain null elements "
            f"(got {len(items)} items, including null)."
        )
        raise NullInCollectionError(msg)
    return "["


@beartype
def _mojo_format_variable_declaration(
    name: str,
    value: str,
    _data: Value,
    _modifiers: frozenset[enum.Enum],
) -> str:
    """Format a plain Mojo ``var name = value`` declaration."""
    return f"var {name} = {value}"


@beartype
def _mojo_element_renders_as_string(
    item: Value,
    *,
    date_renders_as_string: bool,
    datetime_renders_as_string: bool,
) -> bool:
    """Return whether *item* would render as a quoted ``String``.

    Used to decide when a Mojo list literal needs an explicit
    ``List[String]`` annotation: Mojo infers ``List[StringLiteral]`` from
    a bare ``["a", "b"]`` literal, which is rejected when assigned into
    a ``Variant`` slot expecting ``List[String]``.  ``str`` and ``bytes``
    always render quoted; ``datetime`` and ``date`` only when the
    configured formatter produces a string.
    """
    match item:
        case str() | bytes():
            return True
        case datetime.datetime():
            return datetime_renders_as_string
        case datetime.date():
            return date_renders_as_string
        case _:
            return False


@beartype
def _mojo_list_format(default_type: str, /) -> SequenceFormatConfig:
    """Build a Mojo LIST ``SequenceFormatConfig`` for the given type."""
    return SequenceFormatConfig(
        sequence_open=_mojo_list_open,
        close="]",
        supports_heterogeneity=False,
        single_element_trailing_comma=False,
        supports_trailing_comma=True,
        empty_sequence=f"List[{default_type}]()",
        preamble_lines=(),
        format_entry=passthrough_sequence_entry,
        typed_opener_fallback=None,
        uses_typed_literal_for_scalars=False,
        requires_uniform_record_shapes=False,
        declared_type=None,
        narrowed_empty_form=None,
    )


@beartype
@dataclasses.dataclass(frozen=True, kw_only=True)
class Mojo(metaclass=LanguageCls):
    """Mojo language specification.

    By default Mojo raises on heterogeneous input because its native
    collections require a single element type.  Opt into
    :attr:`HeterogeneousStrategies.VARIANT` to wrap mixed scalars in a
    generated ``comptime Value = Variant[...]`` and render each scalar
    as ``Value(...)`` so heterogeneous dicts and lists become
    homogeneous in the Variant type.
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

    leading_preamble = no_leading_preamble
    extension = ".mojo"
    pygments_name = "mojo"
    supports_special_floats = True
    supports_variable_names = True
    supports_no_variable_wrap_in_file = False
    dict_supports_heterogeneous_values = False
    supports_dotted_calls = True
    has_free_function_calls = True
    reserved_identifiers: ClassVar[frozenset[str]] = frozenset()
    reserved_variable_identifiers_case_sensitive: bool = True
    reserved_variable_identifiers: frozenset[str] = frozenset(
        {
            "False",
            "None",
            "True",
            "and",
            "as",
            "assert",
            "async",
            "await",
            "break",
            "class",
            "continue",
            "def",
            "del",
            "elif",
            "else",
            "except",
            "finally",
            "fn",
            "for",
            "from",
            "if",
            "import",
            "in",
            "is",
            "let",
            "not",
            "or",
            "pass",
            "raise",
            "return",
            "struct",
            "try",
            "while",
            "with",
            "yield",
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
    supports_default_sequence_element_type = True
    supports_default_set_element_type = True
    supports_default_ordered_map_value_type = False
    non_default_kwargs: ClassVar[dict[str, str]] = {
        "default_set_element_type": "Int",
        "default_sequence_element_type": "Int",
        "default_dict_value_type": "Int",
        "default_dict_key_type": "Int",
        "heterogeneous_value_variant_name": "JsonValue",
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
        record_variants=frozenset(),
        nested_map_widening=NestedMapWideningVariant.NONE,
        modifier_sequence_format_overrides={},
    )
    supports_record_struct_name_prefix = False
    supports_record_shape_names = False
    supports_non_string_dict_keys = True

    format_call_arg: ClassVar["staticmethod[[Value, str], str]"] = (
        staticmethod(
            identity_call_arg,
        )
    )
    """Callable that rewrites a formatted direct call argument."""

    class DateFormats(enum.Enum):
        """Date format options for Mojo."""

        ISO = DateFormatConfig(
            formatter=format_date_iso, type_produced=str, preamble_lines=()
        )

        def __call__(self, date_value: datetime.date, /) -> str:
            """Format a date."""
            return self.value.formatter(date_value)

    class DatetimeFormats(enum.Enum):
        """Datetime format options for Mojo."""

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
        """Sequence type options for Mojo."""

        LIST = enum.member(value=_mojo_list_format)

        def __call__(self, default_type: str) -> SequenceFormatConfig:
            """Create a sequence format config for the given type."""
            return self.value(default_type)

    class SetFormats(enum.Enum):
        """Set type options for Mojo."""

        SET = enum.member(
            value=set_format_factory(
                open_template="Set[{type}](",
                close=")",
                empty_template="Set[{type}]()",
                preamble_lines=("from std.collections import Set",),
                set_opener_template="Set[{type_name}](",
                supports_heterogeneity=True,
                supports_trailing_comma=True,
            )
        )

        def __call__(self, default_type: str) -> SetFormatConfig:
            """Create a set format config for the given type."""
            return self.value(default_type)

    class CommentFormats(enum.Enum):
        """Comment style options."""

        HASH = CommentConfig(
            prefix="#",
            suffix="",
        )

    class DeclarationStyles(enum.Enum):
        """Declaration style options."""

        ASSIGN = DeclarationStyleConfig(
            formatter=_mojo_format_variable_declaration,
            supports_redefinition=True,
        )

    class DictEntryStyles(enum.Enum):
        """Dict entry style options."""

        DEFAULT = enum.auto()

    class DictFormats(enum.Enum):
        """Dict/map format options."""

        DEFAULT = enum.member(
            value=dict_format_factory(
                open_template="{{",
                close="}",
                format_entry=dict_entry_with_separator(
                    separator=": ",
                    format_value=passthrough_sequence_entry,
                ),
                empty_template="Dict[{key_type}, {type}]()",
                preamble_lines=(),
                narrowed_open=None,
                supports_trailing_comma=True,
            )
        )

        def __call__(
            self,
            default_type: str,
            *,
            default_key_type: str = "String",
        ) -> DictFormatConfig:
            """Create a dict format config for the given type."""
            return self.value(
                default_type,
                default_key_type=default_key_type,
            )

    class EmptyDictKey(enum.Enum):
        """Empty dict key options."""

        ALLOW = enum.auto()

    class FloatFormats(
        FloatSpecialsMixin,
        enum.Enum,
        positive_infinity="std.math.inf[DType.float64]()",
        negative_infinity="-std.math.inf[DType.float64]()",
        nan="std.math.nan[DType.float64]()",
    ):
        """Float format options."""

        REPR = enum.member(value=format_float_repr)
        SCIENTIFIC = enum.member(value=format_float_scientific)
        FIXED = enum.member(value=format_float_fixed)

    class IntegerFormats(enum.Enum):
        """Integer format options."""

        DECIMAL = enum.auto()

    class NumericLiteralSuffixes(enum.Enum):
        """Numeric literal suffix options."""

        NONE = enum.auto()

    class NumericSeparators(enum.Enum):
        """Numeric separator options."""

        NONE = enum.auto()

    class NumericStyles(enum.Enum):
        """Numeric literal style options."""

        OVERLOADED = enum.auto()

    class StringFormats(enum.Enum):
        """String format options."""

        DOUBLE = enum.auto()

    class TrailingCommas(enum.Enum):
        """Trailing comma options."""

        YES = TrailingCommaConfig(multiline_trailing_comma=True)

    date_formats = DateFormats
    datetime_formats = DatetimeFormats
    bytes_formats = BytesFormats
    sequence_formats = SequenceFormats
    set_formats = SetFormats
    comment_formats = CommentFormats

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
        """Mojo call style options."""

        POSITIONAL = PositionalCallStyle(
            arg_separator=", ", parenthesize_each_arg=False
        )

    call_styles = CallStyles

    class Modifiers(enum.Enum):
        """C++/Java/C#-style declaration modifiers: this language has none."""

    modifiers = Modifiers

    class HeterogeneousStrategies(enum.Enum):
        """Strategy for representing dicts or lists whose scalar values
        span more than one Mojo type.
        """

        ERROR = _HeterogeneousStrategyConfig(
            build_behavior=_build_error_behavior,
            build_preamble=_build_error_preamble,
        )
        """Raise
        :exc:`~literalizer.exceptions.HeterogeneousScalarCollectionError`
        (or :exc:`~literalizer.exceptions.HeterogeneousSiblingListsError`)
        when scalar values of mixed types appear in a container that
        cannot represent them.  This is the default, matching the
        single-element-type convention of the Mojo ``List``, ``Dict``,
        and ``Set`` containers.
        """

        VARIANT = _HeterogeneousStrategyConfig(
            build_behavior=_build_variant_behavior,
            build_preamble=_build_variant_preamble,
        )
        """Auto-generate a ``comptime`` binding in the preamble for the
        configured name to a ``Variant[...]`` over only the Mojo types
        actually present in heterogeneous positions, together with a
        ``from std.utils.variant import Variant`` import, and wrap each
        such scalar as ``{Name}(value)`` (with an explicit ``String(...)``
        or ``Float64(...)`` cast when needed so the constructor resolves
        to the intended Variant alternative, and ``NoneType()`` for
        nulls).

        The alias name is configurable via
        :attr:`Mojo.heterogeneous_value_variant_name` (default
        ``"Value"``).
        """

    heterogeneous_strategies = HeterogeneousStrategies

    class JsonTypes(enum.Enum):
        """Empty: this language has no JSON value-type variants."""

    json_types = JsonTypes

    class BoolFormats(enum.Enum):
        """Empty: this language has no alternative boolean formats."""

    bool_formats = BoolFormats

    class VersionFormats(enum.Enum):
        """Version options for Mojo."""

        V24_5 = enum.auto()

    version_formats = VersionFormats

    modifier_combinations: ClassVar[tuple[ModifierCombination, ...]] = ()
    identifier_cases: ClassVar[tuple[IdentifierCase, ...]] = (
        IdentifierCase.SNAKE,
        IdentifierCase.UPPER_SNAKE,
    )
    supported_ref_cases: ClassVar[frozenset[IdentifierCase]] = (
        NON_KEBAB_REF_CASES
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

    def wrap_in_file(
        self,
        content: str,
        variable_name: str,
        body_preamble: tuple[str, ...],
    ) -> str:
        """Wrap a Mojo variable declaration in a main function."""
        content = prepend_body_preamble(
            content=content,
            body_preamble=body_preamble,
        )
        if variable_name:
            content = content + f"\n_ = {variable_name}"
        indented = textwrap.indent(text=content, prefix=self.indent)
        return f"def main():\n{indented}"

    def wrap_combined_in_file(
        self,
        declaration: str,
        assignment: str,
        variable_name: str,
        body_preamble: tuple[str, ...],
    ) -> str:
        """Wrap Mojo declaration and assignment in a main function."""
        declaration = prepend_body_preamble(
            content=declaration,
            body_preamble=body_preamble,
        )
        use = f"_ = {variable_name}"
        return self.wrap_in_file(
            content=declaration + f"\n{use}\n" + assignment,
            variable_name=variable_name,
            body_preamble=(),
        )

    date_format: DateFormats = DateFormats.ISO
    datetime_format: DatetimeFormats = DatetimeFormats.ISO
    bytes_format: BytesFormats = BytesFormats.HEX
    sequence_format: SequenceFormats = SequenceFormats.LIST
    set_format: SetFormats = SetFormats.SET
    default_set_element_type: str = "String"
    default_sequence_element_type: str = "String"
    default_dict_key_type: str = "String"
    default_dict_value_type: str = "String"
    variable_type_hints: VariableTypeHints = VariableTypeHints.NEVER
    comment_format: CommentFormats = CommentFormats.HASH
    declaration_style: DeclarationStyles = DeclarationStyles.ASSIGN
    dict_entry_style: DictEntryStyles = DictEntryStyles.DEFAULT
    dict_format: DictFormats = DictFormats.DEFAULT
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
    heterogeneous_strategy: HeterogeneousStrategies = (
        HeterogeneousStrategies.ERROR
    )
    heterogeneous_value_variant_name: str = "Value"
    # Keep in sync with the ``mojo-compiler`` pin in the ``lint-mojo``
    # job of ``.github/workflows/lint.yml``.
    language_version: VersionFormats = VersionFormats.V24_5
    indent: str = "    "

    null_literal: ClassVar[str] = "None"
    true_literal: ClassVar[str] = "True"
    false_literal: ClassVar[str] = "False"
    indent_closing_delimiter: ClassVar[bool] = False
    element_separator: ClassVar[str] = ", "
    supports_collection_comments: ClassVar[bool] = True
    supports_scalar_before_comments: ClassVar[bool] = False
    supports_scalar_inline_comments: ClassVar[bool] = True
    statement_terminator: ClassVar[str] = ""
    static_preamble: ClassVar[Sequence[str]] = ()
    static_body_preamble: ClassVar[Sequence[str]] = ()
    special_float_preamble: ClassVar[tuple[str, ...]] = ("import std.math",)
    call_style: CallStyles = CallStyles.POSITIONAL

    @cached_property
    def format_string(self) -> Callable[[str], str]:
        """Format a string value as a quoted literal."""
        return format_string_backslash

    @cached_property
    def format_integer(self) -> Callable[[int], str]:
        """Format an int value as a literal."""
        return str

    @cached_property
    def format_sequence_entry(self) -> Callable[[Value, str], str]:
        """Format a sequence entry."""
        return passthrough_sequence_entry

    @cached_property
    def format_set_entry(self) -> Callable[[Value, str], str]:
        """Format a set entry."""
        return passthrough_set_entry

    @cached_property
    def skip_null_dict_values(self) -> bool:
        """Drop ``None`` dict values for the default ERROR strategy so
        the homogeneous-dict rendering stays valid Mojo.

        ``VARIANT`` wraps every scalar as ``Value(...)``, so ``None``
        values must flow through unchanged to be wrapped as
        ``Value(None)`` against a ``NoneType`` Variant alternative.
        """
        cls = type(self.heterogeneous_strategy)
        return self.heterogeneous_strategy is cls.ERROR

    @cached_property
    def data_dependent_preamble(self) -> Callable[[Value], tuple[str, ...]]:
        """Return data-dependent preamble lines.

        For ``HeterogeneousStrategies.VARIANT`` emits an ``alias`` line
        declaring the ``Variant`` over only the Mojo types actually used
        in heterogeneous positions.  Other strategies produce no
        preamble.
        """
        return self.heterogeneous_strategy.value.build_preamble(
            self.heterogeneous_value_variant_name,
            self.datetime_format.value.type_produced,
        )

    @cached_property
    def heterogeneous_behavior(self) -> HeterogeneousBehavior:
        """Return the behavior for the chosen heterogeneous strategy."""
        return self.heterogeneous_strategy.value.build_behavior(
            self.heterogeneous_value_variant_name,
            self.datetime_format.value.type_produced,
        )

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
        return _mojo_call_stub

    @cached_property
    def format_call_preamble_stub(
        self,
    ) -> Callable[
        [Sequence[str], Sequence[str], StubReturn, Sequence[Value]],
        tuple[str, ...],
    ]:
        """Return file-scope stubs for a call expression."""
        cls = type(self.heterogeneous_strategy)
        heterogeneous_value_type = (
            self.heterogeneous_value_variant_name
            if self.heterogeneous_strategy is cls.VARIANT
            else None
        )
        return partial(
            _mojo_call_preamble_stub,
            indent=self.indent,
            heterogeneous_value_type=heterogeneous_value_type,
        )

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
        """Append ``^`` to trigger move/transfer semantics in Mojo,
        except for register-trivial scalars.

        Mojo ``Dict`` does not implement ``Copyable``, so a bare
        variable reference fails to compile and ``^`` transfers
        ownership instead.  Applying ``^`` to a register-trivial scalar
        (``Int``, ``Bool``, ``Float64``) is a hard error under
        ``--Werror``, so we drop the operator when the caller's
        ``ref_values`` identifies the ref as one of those types.  When
        the value is unknown we keep the historical ``^`` form.
        """
        datetime_type_produced = self.datetime_format.value.type_produced

        def _format_mojo_ref_identifier(
            name: str, value: Value | None, /
        ) -> str:
            """Append ``^`` unless *value* is register-trivial."""
            if value is not None and _mojo_value_inhibits_consuming_form(
                value, datetime_type_produced=datetime_type_produced
            ):
                return name
            return f"{name}^"

        return _format_mojo_ref_identifier

    @cached_property
    def format_call_arg_ref_identifier(
        self,
    ) -> Callable[[str, Value | None], str]:
        """Emit a call-argument ``$ref`` as the bare identifier.

        The Mojo transfer operator ``^`` consumes the variable, which
        is unsafe when the caller may use it again in a later call (or
        after the ``literalize_call`` block).  Callers opt in to
        transferring a specific ref by listing it in
        ``literalize_call``'s ``consumable_refs`` set; in that case
        :attr:`format_call_arg_ref_identifier_consumable` is used
        instead and appends ``^``.
        """
        return identity_call_ref_identifier

    @cached_property
    def format_call_arg_ref_identifier_consumable(
        self,
    ) -> Callable[[str, Value | None], str]:
        """Append ``^`` to a consumable call-argument ``$ref``.

        Used only for refs the caller declared as consumable on
        :func:`~literalizer.literalize_call` and that appear in just
        one call argument, so the transfer cannot strand a later use.
        Refs whose underlying value is a register-trivial scalar
        (``Int``, ``Bool``, ``Float64``) are routed away from this
        formatter at the call site (see
        :attr:`consumable_ref_value_inhibits_consuming_form`), because
        applying ``^`` to such a value is a hard error under ``--Werror``.
        """
        return self.format_call_ref_identifier

    @cached_property
    def consumable_ref_value_inhibits_consuming_form(
        self,
    ) -> Callable[[Value], bool]:
        """Return ``True`` for ref values whose Mojo type is register-
        trivial.

        Mojo 0.26.1.0+ rejects ``^`` on ``Int``, ``Bool``, and
        ``Float64`` values under ``--Werror`` because the transfer has
        no effect.  The trivial-register set is derived from
        :func:`_mojo_variant_for_scalar` so the formatter layer avoids
        hard-coded Mojo type-name strings.
        """
        datetime_type_produced = self.datetime_format.value.type_produced

        def _inhibits(value: Value, /) -> bool:
            """Closure binding the configured datetime type."""
            return _mojo_value_inhibits_consuming_form(
                value, datetime_type_produced=datetime_type_produced
            )

        return _inhibits

    @cached_property
    def call_style_config(self) -> CallStyle:
        """Configuration for the chosen call style."""
        config: CallStyle = self.call_style.value
        return config

    @cached_property
    def sequence_format_config(self) -> SequenceFormatConfig:
        """Configuration for the chosen sequence format."""
        base = self.sequence_format(
            default_type=self.default_sequence_element_type,
        )
        return dataclasses.replace(
            base,
            narrowed_empty_form=_mojo_narrowed_empty_form,
        )

    @cached_property
    def set_format_config(self) -> SetFormatConfig:
        """Configuration for the chosen set format."""
        base = self.set_format(default_type=self.default_set_element_type)
        return base.with_typed_opener(
            type_to_opener=make_type_to_opener(
                element_to_type=make_element_to_type(
                    str_type="String",
                    bool_type="Bool",
                    int_type="Int",
                    float_type="Float64",
                    mixed_numeric_type="String",
                    bytes_type=None,
                    date_type=None,
                    datetime_type=None,
                    time_type=None,
                    list_template="List[{inner}]",
                    enable_list_type=True,
                    dict_type_template=None,
                    fallback_value_type=None,
                    wide_int_type=None,
                    beyond_i64_type=None,
                ),
                opener_template="Set[{type_name}](",
            ),
            fallback=base.set_open([]),
        )

    @cached_property
    def sequence_open(self) -> Callable[[list[Value]], str]:
        """Callable that returns the opening delimiter for a sequence."""
        return self.sequence_format_config.sequence_open

    @cached_property
    def dict_format_config(self) -> DictFormatConfig:
        """Configuration for dict formatting."""
        return self.dict_format(
            default_type=self.default_dict_value_type,
            default_key_type=self.default_dict_key_type,
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
        return format_time_iso

    @cached_property
    def format_float(self) -> Callable[[float], str]:
        """Callable that formats a float value as a literal."""
        return self.float_format

    @cached_property
    def comment_config(self) -> CommentConfig:
        """Configuration for the language's comment syntax."""
        return self.comment_format.value

    @cached_property
    def ordered_map_format_config(self) -> OrderedMapFormatConfig:
        """Configuration for ordered-map formatting."""
        return OrderedMapFormatConfig(
            ordered_map_open=fixed_open(open_str="["),
            close="]",
            preamble_lines=(),
        )

    @cached_property
    def format_ordered_map_entry(self) -> Callable[[str, Value, str], str]:
        """Callable that formats one ordered-map entry."""
        return _format_mojo_ordered_map_entry

    @cached_property
    def format_variable_declaration(
        self,
    ) -> Callable[[str, str, Value, frozenset[enum.Enum]], str]:
        """Callable that formats a new variable declaration.

        Wraps the configured declaration formatter so a non-empty list of
        string-rendering elements gets an explicit ``List[String]``
        annotation.  Mojo infers ``List[StringLiteral]`` from a bare
        ``["a", "b"]`` literal, which is rejected when assigned into a
        ``Variant`` slot expecting ``List[String]``.
        """
        base_formatter = self.declaration_style.value.formatter
        date_renders_as_string = self.date_format.value.type_produced is str
        datetime_renders_as_string = (
            self.datetime_format.value.type_produced is str
        )

        def _format(
            name: str,
            value: str,
            data: Value,
            modifiers: frozenset[enum.Enum],
        ) -> str:
            """Format the declaration, annotating string lists."""
            if (
                isinstance(data, list)
                and data
                and all(
                    _mojo_element_renders_as_string(
                        item=item,
                        date_renders_as_string=date_renders_as_string,
                        datetime_renders_as_string=datetime_renders_as_string,
                    )
                    for item in data
                )
            ):
                return f"var {name}: List[String] = {value}"
            return base_formatter(name, value, data, modifiers)

        return _format

    @cached_property
    def format_variable_assignment(
        self,
    ) -> Callable[[str, str, Value], str]:
        """Callable that formats an assignment to an existing variable."""
        return variable_formatter(template="{name} = {value}")

    @cached_property
    def scalar_preamble(self) -> dict[type, tuple[str, ...]]:
        """Per-instance scalar preamble (Mojo needs none)."""
        return {}

    @cached_property
    def scalar_body_preamble(self) -> dict[type, tuple[str, ...]]:
        """Per-instance scalar body preamble (Mojo needs none)."""
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
