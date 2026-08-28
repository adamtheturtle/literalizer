"""Compute preamble lines for the types present in literalized data."""

import dataclasses
import datetime
from typing import Final, assert_never, get_args

from beartype import beartype

from literalizer._checks import scalar_type_bucket
from literalizer._formatters.format_floats import data_has_special_float
from literalizer._formatters.type_inference import collect_record_shapes
from literalizer._language import Language
from literalizer._types import OrderedMap, Scalar, Value


class HeterogeneousElements:
    """Sentinel added to ``annotated_collection_types`` when the data
    contains annotated collections whose element types produce a union
    (i.e. ``Union[A, B]`` or ``A | B`` in the generated type hint).

    Languages that need to import a union-type helper only when it is
    actually used (e.g. Python 3.8's ``from typing import Union``) can
    check for this sentinel in their
    ``type_hint_collection_preamble_lines`` callable.
    """


_ALL_VALUE_TYPES: Final[frozenset[type]] = frozenset(
    # pylint does not model PEP 695 aliases, so it does not see the
    # ``__value__`` every ``type`` statement defines.
    get_args(tp=Scalar.__value__)  # pylint: disable=no-member
) | {OrderedMap, dict, list, set}
"""Every type :func:`_collect_value_types` can report.

Once all of them have been observed there is nothing left to learn, so
the walk stops early.  The scalar half is derived from :data:`Scalar`
rather than listed by hand: a scalar type added there but missed here
would let the walk stop before observing it.
"""


@beartype
def _collect_value_types(
    *,
    data: Value,
    recordized_dict_ids: frozenset[int],
) -> frozenset[type]:
    """Return the set of Python types present in *data*.

    The document is walked with an explicit stack, and the walk stops
    as soon as every type in :data:`_ALL_VALUE_TYPES` has been seen, so
    a large document costs no more than the point at which its type set
    saturates.
    """
    found: set[type] = set()
    pending: list[Value] = [data]
    while pending and len(found) != len(_ALL_VALUE_TYPES):
        value = pending.pop()
        match value:
            case OrderedMap():
                # ``str`` is included unconditionally because typed-map
                # languages whose dict opener hard-codes the default key
                # type (e.g. ``std::map<std::string, ...>`` in C++)
                # still need the string preamble even when the data has
                # no string keys or values.  The actual rendered code
                # references ``std::string`` regardless of payload.
                found.update((OrderedMap, str))
                pending.extend(value)
                pending.extend(value.values())
            case dict():
                # A dict the RECORD strategy turns into a struct is
                # rendered as a struct literal rather than a map, so it
                # does not pull in the map type's preamble.  Its keys
                # become field names rather than string values, but
                # ``str`` stays: a language may still name the string
                # type in a field declaration (issue #4496).
                found.add(str)
                if id(value) not in recordized_dict_ids:
                    found.add(dict)
                pending.extend(value)
                pending.extend(value.values())
            case set():
                found.add(set)
                pending.extend(value)
            case list():
                found.add(list)
                pending.extend(value)
            case _ if type(value) in found:
                # ``found`` only ever holds the canonical types, so an
                # exact-type hit means :func:`_preamble_scalar_type`
                # would return a type already recorded.  A scalar of a
                # subclass type misses here and takes the slow path.
                pass
            case _:
                found.add(_preamble_scalar_type(value=value))
    return frozenset(found)


@beartype
def _needs_annotation(val: Value) -> bool:
    """Return True if *val* requires a type annotation.

    A collection needs annotation when it is empty (so type-checkers can
    infer element types) or contains an element/value that itself needs
    annotation.
    """
    match val:
        case dict():
            return not val or any(
                _needs_annotation(val=v) for v in val.values()
            )
        case set():
            return not val
        case list():
            return not val or any(_needs_annotation(val=v) for v in val)
        case _:
            return False


@beartype
def _add_collection_type(*, val: Value, result: set[type]) -> None:
    """Add the collection type named by a containing annotation."""
    match val:
        case OrderedMap():
            result.add(OrderedMap)
        case dict():
            result.add(dict)
        case set():
            result.add(set)
        case list():
            result.add(list)
        case _:
            pass


@beartype
def _walk_annotated_collections(  # noqa: C901  # pylint: disable=too-complex
    *,
    val: Value,
    result: set[type],
) -> None:
    """Walk *val* and add collection types that appear in type annotations."""
    match val:
        case OrderedMap():
            if _needs_annotation(val=val):
                result.add(OrderedMap)
                for v in val.values():
                    _walk_annotated_collections(val=v, result=result)
                    _add_collection_type(val=v, result=result)
        case dict():
            if _needs_annotation(val=val):
                result.add(dict)
                for v in val.values():
                    _walk_annotated_collections(val=v, result=result)
                    _add_collection_type(val=v, result=result)
        case set():
            if not val:
                result.add(set)
        case list():
            if _needs_annotation(val=val):
                result.add(list)
                for v in val:
                    _walk_annotated_collections(val=v, result=result)
                    _add_collection_type(val=v, result=result)
        case _:
            pass


@beartype
def _collect_annotated_collection_types(*, data: Value) -> frozenset[type]:
    """Return the set of collection types that appear in type annotations.

    This is a superset of empty collection types: it also includes
    non-empty containers that wrap annotated children.
    """
    result: set[type] = set()
    _walk_annotated_collections(val=data, result=result)
    return frozenset(result)


@beartype
def _preamble_scalar_type(*, value: Scalar) -> type:
    """Return the preamble-relevant type for a scalar.

    Like :func:`scalar_type_bucket` but distinguishes
    ``datetime.datetime`` from ``datetime.date`` (they need different
    preamble lines).
    """
    match value:
        case datetime.datetime():
            return datetime.datetime
        case datetime.date():
            return datetime.date
        case _:
            return scalar_type_bucket(value=value)


@beartype
def _recordized_dict_ids(*, data: Value, language: Language) -> frozenset[int]:
    """Return the ids of dicts the RECORD strategy renders as structs.

    ``collect_record_shapes`` is the pure eligibility pass, and
    ``compute_wrap_ids`` names the nested sibling maps the strategy
    drops back to plain maps, so the difference is what actually
    becomes a struct.  The strategy's own ``compute_record_shapes``
    is deliberately not called here: it reassigns document-order names
    as a side effect, and the preamble walks the ref-resolved tree
    rather than the rendered one (issue #4496).
    """
    behavior = language.heterogeneous_behavior
    if behavior.render_record_literal is None:
        return frozenset()
    return frozenset(
        collect_record_shapes(data=data)
    ) - behavior.compute_wrap_ids(data)


@beartype
def _collection_preamble(
    *,
    types: frozenset[type],
    language: Language,
) -> tuple[str, ...]:
    """Return collection-config preamble lines for present types."""
    lines: list[str] = []
    if dict in types:
        lines.extend(language.dict_format_config.preamble_lines)
    if set in types:
        lines.extend(language.set_format_config.preamble_lines)
    if list in types:
        lines.extend(language.sequence_format_config.preamble_lines)
    if OrderedMap in types:
        lines.extend(language.ordered_map_format_config.preamble_lines)
    return tuple(lines)


@beartype
def deduplicate_preamble_entries(
    *,
    entries: tuple[str, ...],
) -> tuple[str, ...]:
    """Remove duplicate preamble entries preserving first-seen order.

    An entry is usually one source line, but callers may also represent
    a multi-line preamble block as one string.
    """
    seen: set[str] = set()
    result: list[str] = []
    for entry in entries:
        if entry not in seen:
            seen.add(entry)
            result.append(entry)
    return tuple(result)


@beartype
def _list_merge_dicts(*, elements: list[Value]) -> list[Value]:
    """Return *elements* with plain dicts pooled and ordered dicts pooled.

    Mirrors the ``merge_dicts=True`` behavior used by Python's
    ``_collection_element_union`` for sequence elements: all plain-dict
    siblings are merged into a single representative dict (likewise for
    ordered-dict siblings) so that the element-type union is computed on
    the merged result rather than on each individual dict.
    """
    plain_vals: list[Value] = []
    ordered_vals: list[Value] = []
    non_dict: list[Value] = []
    has_plain = False
    has_ordered = False
    for elem in elements:
        match elem:
            case OrderedMap():
                has_ordered = True
                ordered_vals.extend(elem.values())
            case dict():
                has_plain = True
                plain_vals.extend(elem.values())
            case _:
                non_dict.append(elem)
    merged: list[Value] = list(non_dict)
    if has_plain:
        merged_plain: dict[Scalar, Value] = {
            str(object=i): v for i, v in enumerate(iterable=plain_vals)
        }
        merged.append(merged_plain)
    if has_ordered:
        ordered_src: dict[Scalar, Value] = {
            str(object=i): v for i, v in enumerate(iterable=ordered_vals)
        }
        merged.append(OrderedMap(ordered_src))
    return merged


@beartype
def _structural_type_id(  # noqa: C901, PLR0911, PLR0912  # pylint: disable=too-complex,too-many-branches,too-many-return-statements
    *,
    value: Value,
) -> str:
    """Return a structural type identifier for *value*.

    Two values produce the same ID if and only if Python's
    ``_python_type_hint`` would return the same string for them
    (regardless of the concrete type-hint names configured for the
    language, e.g. ``Tuple`` vs ``tuple``).

    This is used by :func:`_has_union_in_type_hints` to detect whether
    element types are heterogeneous without actually running the full
    type-hint formatter.
    """
    match value:
        case bool():
            return "bool"
        case int():
            return "int"
        case float():
            return "float"
        case str():
            return "str"
        case bytes():
            return "bytes"
        case datetime.datetime():
            return "datetime"
        case datetime.time():
            return "time"
        case datetime.date():
            return "date"
        case None:
            return "None"
        case list() if not value:
            return "empty_list"
        case list():
            merged = _list_merge_dicts(elements=value)
            elem_ids = list(
                dict.fromkeys(_structural_type_id(value=e) for e in merged)
            )
            return f"list({','.join(elem_ids)})"
        case set() if not value:
            return "empty_set"
        case set():
            elem_ids = sorted({_structural_type_id(value=e) for e in value})
            return f"set({','.join(elem_ids)})"
        case OrderedMap() if not value:
            return "empty_odict"
        case OrderedMap():
            val_set: set[str] = set()
            for ov in value.values():
                val_set.add(_structural_type_id(value=ov))
            val_ids = sorted(val_set)
            return f"odict({','.join(val_ids)})"
        case dict() if not value:
            return "empty_dict"
        case dict():
            val_ids = sorted(
                {_structural_type_id(value=v) for v in value.values()}
            )
            return f"dict({','.join(val_ids)})"
        case _ as unreachable:
            assert_never(unreachable)


@beartype
def _has_union_in_type_hints(*, data: Value) -> bool:
    """Return ``True`` if the Python type hints for *data* would contain
    a union (``Union[A, B]`` or ``A | B``).

    Walks *data* recursively and applies the same ``merge_dicts=True``
    logic that Python's sequence type-hint formatter uses, so the result
    is accurate without running the full formatter.
    """
    match data:
        case list():
            merged = _list_merge_dicts(elements=data)
            type_ids = list(
                dict.fromkeys(_structural_type_id(value=e) for e in merged)
            )
            if len(type_ids) > 1:
                return True
            return any(_has_union_in_type_hints(data=e) for e in merged)
        case dict():
            if data:
                val_ids = list(
                    dict.fromkeys(
                        _structural_type_id(value=v) for v in data.values()
                    )
                )
                if len(val_ids) > 1:
                    return True
            return any(_has_union_in_type_hints(data=v) for v in data.values())
        case _:
            return False


@dataclasses.dataclass(frozen=True)
class _PreambleResult:
    """Header and body preamble lines."""

    leading: tuple[str, ...]
    header: tuple[str, ...]
    body: tuple[str, ...]
    types_present: frozenset[type]


@beartype
def compute_preamble(
    *,
    data: Value,
    language: Language,
    has_variable_declaration: bool,
) -> _PreambleResult:
    """Compute preamble lines from the data types present and the
    language configuration.
    """
    recordized_dict_ids = _recordized_dict_ids(data=data, language=language)
    types = _collect_value_types(
        data=data,
        recordized_dict_ids=recordized_dict_ids,
    )

    scalar = tuple(
        line
        for scalar_type, preamble in language.scalar_preamble.items()
        if scalar_type in types
        for line in preamble
    )
    special_float = (
        language.special_float_preamble
        if float in types and data_has_special_float(data=data)
        else ()
    )
    collection = _collection_preamble(types=types, language=language)
    annotated_collection_types: frozenset[type] = (
        _collect_annotated_collection_types(data=data)
        if has_variable_declaration and types & {dict, list, set, OrderedMap}
        else frozenset()
    )
    if has_variable_declaration and _has_union_in_type_hints(data=data):
        annotated_collection_types = annotated_collection_types | frozenset(
            {HeterogeneousElements}
        )
    type_hint = (
        language.type_hint_collection_preamble_lines(
            annotated_collection_types
        )
        if annotated_collection_types
        else ()
    )
    body = language.compute_body_preamble(types, data)
    leading = tuple(
        language.leading_preamble(
            data, has_variable_declaration=has_variable_declaration
        )
    )
    return _PreambleResult(
        leading=leading,
        header=deduplicate_preamble_entries(
            entries=scalar + special_float + collection + type_hint,
        )
        + tuple(language.static_body_preamble),
        body=body,
        types_present=types,
    )
