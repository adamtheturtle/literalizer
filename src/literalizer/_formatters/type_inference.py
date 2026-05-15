"""Type inference for homogeneous collections."""

from collections.abc import Mapping, Sequence
from dataclasses import dataclass, field

from beartype import beartype
from ruamel.yaml.compat import ordereddict as _ordereddict

from literalizer._types import Scalar, Value


@dataclass(frozen=True)
class ListType:
    """Represents a homogeneous list element type for type inference.

    For nested lists, ``inner`` is another ``ListType``.
    For leaf lists, ``inner`` is a Python ``type``.
    """

    inner: "type | ListType | DictType"


@dataclass(frozen=True)
class DictType:
    """Represents a homogeneous dict element type for type inference.

    ``value_type`` is the inferred common value type across all dicts
    in a sequence, or ``None`` when values are empty or mixed.
    ``values`` is the flattened sequence of dict values used to infer
    ``value_type``; callers can reuse it to derive a language-specific
    type (e.g. ``std::variant``) without re-walking the source items.
    """

    value_type: "type | ListType | DictType | None"
    values: "tuple[Value, ...]" = field(compare=False)


class MixedNumeric:
    """Sentinel class representing mixed int/float element types.

    Used as a key in scalar type mapping dicts so each language can
    decide how to handle collections containing both int and float
    values.
    """


class WideInt:
    """Sentinel class for int collections containing values outside the
    signed 32-bit range.

    Used as a key in scalar type mapping dicts so each language can
    decide what wider integer type (e.g. ``long``, ``i64``) the
    collection's element type should be annotated as.
    """


_I32_MIN = -(2**31)
_I32_MAX = 2**31 - 1


def _int_needs_widening(items: list[Value]) -> bool:
    """Return ``True`` if any int in *items* is outside i32 range."""
    return any(
        isinstance(item, int)
        and not isinstance(item, bool)
        and not _I32_MIN <= item <= _I32_MAX
        for item in items
    )


@dataclass(frozen=True)
class _Collected:
    """Per-item type buckets gathered for ``infer_element_type``."""

    element_types: set[type | ListType]
    dict_values: list[Value]


_INFER_FAILED = object()


def _collect_element_types(
    items: list[Value],
) -> _Collected | object:
    """Collect element types for ``items`` or signal hard inference
    failure.

    Empty inner lists are skipped so they do not poison inference of
    homogeneous siblings.  When every list item is empty (and there
    are no other items contributing a ``ListType``), ``_INFER_FAILED``
    is returned because no concrete inner type could be derived.
    """
    element_types: set[type | ListType] = set()
    dict_values: list[Value] = []
    saw_empty_list = False
    for item in items:
        match item:
            case []:
                saw_empty_list = True
            case list():
                inner = infer_element_type(items=item)
                if inner is None:
                    return _INFER_FAILED
                element_types.add(ListType(inner=inner))
            case dict() if not isinstance(item, _ordereddict):
                dict_values.extend(item.values())
                element_types.add(dict)
            case _:
                element_types.add(type(item))
    if saw_empty_list and not any(
        isinstance(t, ListType) for t in element_types
    ):
        return _INFER_FAILED
    return _Collected(element_types=element_types, dict_values=dict_values)


@beartype
def _resolve_single_type(
    *,
    the_type: type | ListType,
    items: list[Value],
    all_dict_values: list[Value],
) -> type | ListType | DictType:
    """Resolve a unique element type to its inferred return value.

    Handles the ``dict`` -> :class:`DictType` and the int-widening to
    :class:`WideInt` branches; falls through to ``the_type`` itself
    otherwise.
    """
    if the_type is dict:
        value_type = infer_element_type(items=all_dict_values)
        return DictType(
            value_type=value_type,
            values=tuple(all_dict_values),
        )
    if the_type is int and _int_needs_widening(items=items):
        return WideInt
    return the_type


@beartype
def infer_element_type(
    items: list[Value],
) -> type | ListType | DictType | None:
    """Infer the common element type from a list of values.

    Returns ``None`` when the list is empty or contains mixed types
    that cannot be unified.  Returns ``MixedNumeric`` when the list
    contains a mix of ``int`` and ``float`` values.  Returns a
    ``DictType`` when all items are plain dicts (not ordered maps).
    """
    if not items:
        return None
    collected = _collect_element_types(items=items)
    if not isinstance(collected, _Collected):
        return None
    element_types = collected.element_types
    if len(element_types) == 1:
        return _resolve_single_type(
            the_type=next(iter(element_types)),
            items=items,
            all_dict_values=collected.dict_values,
        )
    if element_types == {int, float}:
        return MixedNumeric
    return None


@dataclass(frozen=True)
class RecordShape:
    """Immutable signature of a record-shaped dict, suitable for use
    as a dict key.

    Used by the ``RECORD`` heterogeneous strategy to render
    record-shaped dicts as generated struct literals rather than
    homogeneous maps.  Two dicts share a shape when their ordered key
    tuples are equal; per-key value-type rendering is decided at
    preamble-build time by each per-language target.

    ``optional_keys`` is empty for the raw per-dict shapes returned by
    :func:`record_shape_for_dict`.  After unification (see
    :func:`unify_record_shapes`) it identifies the keys whose value
    must be wrapped in an optional type (e.g. Rust's ``Option``) and
    rendered as a "missing" placeholder for dict instances that lack
    the key.
    """

    keys: tuple[str, ...]
    optional_keys: frozenset[str] = frozenset()


@beartype
def record_shape_for_dict(
    *,
    value: dict[Scalar, Value],
) -> RecordShape | None:
    """Return the :class:`RecordShape` of *value*, or ``None`` if the
    dict is not record-eligible.

    A dict is record-eligible when it is non-empty and every key is a
    ``str``.  Callers must filter out ruamel ordered maps before
    calling this helper.
    """
    # Defensive branches: every Rust RECORD fixture passes non-empty
    # string-keyed dicts here, but the walker also calls this helper
    # on nested dicts of arbitrary shape that may not be record-eligible.
    if not value:  # pragma: no cover
        return None
    str_keys: list[str] = []
    for key in value:
        if not isinstance(key, str):  # pragma: no cover
            return None
        str_keys.append(key)
    return RecordShape(keys=tuple(str_keys))


@beartype
def collect_record_shapes(*, data: Value) -> dict[int, RecordShape]:
    """Walk *data* and return a mapping from ``id(dict)`` to its
    :class:`RecordShape` for every record-eligible dict.
    """
    result: dict[int, RecordShape] = {}
    _accumulate_record_shapes(data=data, out=result)
    return result


@beartype
def unify_record_shapes(
    *,
    data: Value,
    shapes_by_id: dict[int, RecordShape],
) -> dict[int, RecordShape]:
    """Merge near-identical sibling shapes into shared unified shapes.

    Two record shapes are placed in the same unification group when
    their key sets share at least one key; groups are formed
    transitively (union-find on the shared-key relation).  Within a
    group the unified key tuple is the keys' first-encounter order in
    *data* and ``optional_keys`` contains every key not present in
    every member.  Shapes with no shared key relative to all others
    remain as singleton groups, returned with empty ``optional_keys``.

    Returns a fresh mapping from ``id(dict)`` to its unified
    :class:`RecordShape`.  Input *shapes_by_id* is not mutated.
    """
    raw_shapes = _ordered_unique_shapes(
        data=data,
        shapes_by_id=shapes_by_id,
    )
    groups = _partition_shapes_by_shared_keys(raw_shapes=raw_shapes)
    unified_for_raw: dict[RecordShape, RecordShape] = {}
    key_order = _key_order_from_shapes(raw_shapes=raw_shapes)
    for group in groups:
        unified = _build_unified_shape(group=group, key_order=key_order)
        for raw in group:
            unified_for_raw[raw] = unified
    return {
        dict_id: unified_for_raw[raw] for dict_id, raw in shapes_by_id.items()
    }


def _ordered_unique_shapes(
    *,
    data: Value,
    shapes_by_id: Mapping[int, RecordShape],
) -> list[RecordShape]:
    """Return raw record shapes in document order, deduplicated."""
    ordered: list[RecordShape] = []
    seen: set[RecordShape] = set()

    def walk(node: Value) -> None:
        """Walk *node* and append each newly-seen raw shape."""
        match node:
            case dict():
                raw = shapes_by_id.get(id(node))
                if raw is not None and raw not in seen:
                    seen.add(raw)
                    ordered.append(raw)
                for v in node.values():
                    walk(node=v)
            case list():
                for item in node:
                    walk(node=item)
            case _:
                return

    walk(node=data)
    return ordered


def _key_order_from_shapes(
    *,
    raw_shapes: Sequence[RecordShape],
) -> dict[str, int]:
    """Return a mapping from key to its first-appearance index across
    *raw_shapes*.

    *raw_shapes* must already be in document order (see
    :func:`_ordered_unique_shapes`).
    """
    order: dict[str, int] = {}
    for shape in raw_shapes:
        for key in shape.keys:
            if key not in order:
                order[key] = len(order)
    return order


def _partition_shapes_by_shared_keys(
    *,
    raw_shapes: Sequence[RecordShape],
) -> list[list[RecordShape]]:
    """Partition *raw_shapes* into groups connected by shared keys.

    Uses union-find: shapes A and B share a group whenever any key in
    ``A.keys`` also appears in ``B.keys``, transitively.
    """
    parent = list(range(len(raw_shapes)))

    def find(index: int) -> int:
        """Return the root index for *index* in the union-find."""
        while parent[index] != index:
            parent[index] = parent[parent[index]]
            index = parent[index]
        return index

    def union(left: int, right: int) -> None:
        """Merge the groups containing *left* and *right*."""
        root_left = find(index=left)
        root_right = find(index=right)
        # Self-assignment is harmless when both indices already share a
        # root, so no equality guard is needed.
        parent[root_right] = root_left

    key_to_first: dict[str, int] = {}
    for shape_index, shape in enumerate(iterable=raw_shapes):
        for key in shape.keys:
            existing = key_to_first.get(key)
            if existing is None:
                key_to_first[key] = shape_index
            else:
                union(left=existing, right=shape_index)

    groups: dict[int, list[RecordShape]] = {}
    for shape_index, shape in enumerate(iterable=raw_shapes):
        root = find(index=shape_index)
        groups.setdefault(root, []).append(shape)
    return [groups[root] for root in sorted(groups)]


def _build_unified_shape(
    *,
    group: Sequence[RecordShape],
    key_order: Mapping[str, int],
) -> RecordShape:
    """Return the unified shape for *group*.

    The unified key tuple lists every key that appears in any member,
    ordered by ``key_order`` (first appearance in document order).
    ``optional_keys`` are the keys missing from at least one member.
    """
    member_key_sets: list[frozenset[str]] = [
        frozenset(shape.keys) for shape in group
    ]
    all_keys: set[str] = set()
    for member_keys in member_key_sets:
        all_keys.update(member_keys)
    required_keys: set[str] = set(member_key_sets[0])
    for member_keys in member_key_sets[1:]:
        required_keys.intersection_update(member_keys)
    ordered_keys: tuple[str, ...] = tuple(
        sorted(all_keys, key=lambda key: key_order[key])
    )
    optional_keys: frozenset[str] = frozenset(all_keys - required_keys)
    return RecordShape(keys=ordered_keys, optional_keys=optional_keys)


def _accumulate_record_shapes(
    *,
    data: Value,
    out: dict[int, RecordShape],
) -> None:
    """Recursively add record shapes for record-eligible dicts in
    *data*.
    """
    # ``Value``-typed sets only contain scalars (see ``literalizer._types``)
    # so there's no need to walk into them.
    match data:
        case dict() if not isinstance(data, _ordereddict):
            shape = record_shape_for_dict(value=data)
            if shape is not None:  # pragma: no branch
                out[id(data)] = shape
            for v in data.values():
                _accumulate_record_shapes(data=v, out=out)
        case dict():
            for v in data.values():
                _accumulate_record_shapes(data=v, out=out)
        case list():
            for v in data:
                _accumulate_record_shapes(data=v, out=out)
        case _:
            return
