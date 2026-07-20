"""Checks that raise when data is incompatible with a language's
collection-shape constraints.
"""

import datetime
from collections.abc import Mapping, Sequence
from typing import TYPE_CHECKING

from beartype import beartype

from literalizer._language import Language
from literalizer._types import OrderedMap, Scalar, Value
from literalizer.exceptions import (
    HeterogeneousCollectionError,
    HeterogeneousScalarCollectionError,
    HeterogeneousSetError,
    HeterogeneousSiblingListsError,
    HeterogeneousSiblingMapsError,
    MixedDictKeysError,
    MixedDictShapesError,
    MixedDictValuesError,
    MixedListValuesError,
    UnrepresentableInputError,
)

if TYPE_CHECKING:
    from literalizer._formatters.type_inference import RecordShape


@beartype
def scalar_type_bucket(*, value: Value) -> type | None:  # noqa: PLR0911
    """Return the type bucket for a scalar, or ``None`` for
    collections.
    """
    # Check bool before int (bool is a subclass of int), and
    # datetime before date (datetime is a subclass of date).
    match value:
        case None:
            return type(None)
        case bool():
            return bool
        case int():
            return int
        case float():
            return float
        case str():
            return str
        case bytes():
            return bytes
        case datetime.date():
            return datetime.date
        case datetime.time():
            return datetime.time
        case _:
            return None


@beartype
def _scalar_type_buckets(
    *,
    values: Sequence[Value],
) -> set[type] | None:
    """Return the set of scalar type buckets for *values*.

    Returns ``None`` if any value is not a scalar.
    """
    buckets: set[type] = set()
    for v in values:
        bucket = scalar_type_bucket(value=v)
        if bucket is None:
            return None
        buckets.add(bucket)
    return buckets


@beartype
def _all_scalars_heterogeneous(
    *,
    values: Sequence[Value],
) -> bool:
    """Check whether values are all scalars with more than one type."""
    buckets = _scalar_type_buckets(values=values)
    return buckets is not None and len(buckets) > 1


@beartype
def _value_type_family(  # noqa: C901, PLR0911, PLR0912
    *,
    value: Value,
) -> str:
    # pylint: disable=too-complex,too-many-branches
    """Return a broad type family label for a value."""
    # Check bool before int (bool is a subclass of int), datetime
    # before date (datetime is a subclass of date), and OrderedMap
    # before dict (OrderedMap is a subclass of dict).
    match value:
        case None:
            return "none"
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
        case datetime.date():
            return "date"
        case datetime.time():
            return "time"
        case list():
            return "list"
        case OrderedMap():
            return "dict"
        case dict():
            return "dict"
        case _:
            return "set"


@beartype
def _values_mixed_types(*, values: Sequence[Value]) -> bool:
    """Check whether values span more than one type family."""
    if len(values) <= 1:
        return False
    families: set[str] = set()
    for v in values:
        families.add(_value_type_family(value=v))
    return len(families) > 1


@beartype
def _collect_scalar_type_names(*, data: Value) -> set[str]:
    """Collect the names of scalar type buckets found in *data*."""
    names: set[str] = set()
    match data:
        case dict():
            for v in data.values():
                names |= _collect_scalar_type_names(data=v)
        case list():
            for v in data:
                names |= _collect_scalar_type_names(data=v)
        case set():
            for v in data:
                names |= _collect_scalar_type_names(data=v)
        case _:
            names.add(_value_type_family(value=data))
    return names


@beartype
def _describe_heterogeneous_types(*, data: Value) -> str:
    """Return a sorted, comma-separated string of scalar type names in
    *data*.
    """
    return ", ".join(sorted(_collect_scalar_type_names(data=data)))


@beartype
def _find_first_mixed_values(
    *,
    data: Value,
    container_type: type,
) -> Sequence[Value]:
    """Return the first collection of children in *data* that spans
    multiple type families.
    """
    children: Sequence[Value]
    match data:
        case dict():
            children = list(data.values())
            if container_type is dict and _values_mixed_types(
                values=children,
            ):
                return children
        case list():
            children = data
            if container_type is list and _values_mixed_types(
                values=children,
            ):
                return children
        case _:
            return []
    for child in children:
        result = _find_first_mixed_values(
            data=child,
            container_type=container_type,
        )
        if result:
            return result
    return []


@beartype
def _describe_mixed_type_families(
    *,
    data: Value,
    container_type: type,
) -> str:
    """Return a sorted, comma-separated string of type families for the
    first collection in *data* whose children span multiple families.
    """
    values = _find_first_mixed_values(
        data=data,
        container_type=container_type,
    )
    return ", ".join(sorted({_value_type_family(value=v) for v in values}))


@beartype
def _has_heterogeneous(
    *,
    data: Value,
    record_dict_ids: frozenset[int],
    tuple_list_ids: frozenset[int],
) -> bool:
    """Recursively check whether data contains any heterogeneous
    all-scalar collections.

    Dicts whose ``id`` is in *record_dict_ids* are skipped — they are
    carved out by the active RECORD heterogeneous strategy.  Lists
    whose ``id`` is in *tuple_list_ids* are skipped — they are carved
    out by the active TUPLE heterogeneous strategy, which renders them
    as a fixed-size tuple rather than a homogeneous sequence.
    """
    match data:
        case dict():
            children: list[Value] = list(data.values())
            own_mixed = id(
                data
            ) not in record_dict_ids and _all_scalars_heterogeneous(
                values=children
            )
        case list():
            children = data
            own_mixed = id(
                data
            ) not in tuple_list_ids and _all_scalars_heterogeneous(
                values=children
            )
        case set():
            return _all_scalars_heterogeneous(values=list(data))
        case _:
            return False

    return own_mixed or any(
        _has_heterogeneous(
            data=v,
            record_dict_ids=record_dict_ids,
            tuple_list_ids=tuple_list_ids,
        )
        for v in children
    )


@beartype
def _has_heterogeneous_sibling_lists(
    *,
    data: Value,
    tuple_list_ids: frozenset[int],
) -> bool:
    """Recursively check whether data contains sibling lists whose
    combined scalar elements are heterogeneous.

    Sibling lists are detected both as the direct children of a list
    and as the values of a dict.

    Lists whose ``id`` is in *tuple_list_ids* are carved out by the
    active TUPLE heterogeneous strategy: each is rendered as its own
    fixed-size tuple type rather than the sequence type shared by the
    remaining sibling lists, so its elements do not join the shared
    element pool and it does not count as a sibling sequence.  Such a
    list still counts as a list value for the "all values are lists"
    gate, so a genuine heterogeneous pair of sibling sequences beside a
    tuple-eligible list is still rejected.
    """
    match data:
        case dict():
            values = list(data.values())
            if any(
                _has_heterogeneous_sibling_lists(
                    data=v,
                    tuple_list_ids=tuple_list_ids,
                )
                for v in values
            ):
                return True
            all_lists: list[list[Value]] = [
                v for v in values if isinstance(v, list)
            ]
            seq_lists = [v for v in all_lists if id(v) not in tuple_list_ids]
            return (
                len(all_lists) == len(values)
                and len(seq_lists) > 1
                and _all_scalars_heterogeneous(
                    values=[e for sub in seq_lists for e in sub],
                )
            )
        case list():
            if any(
                _has_heterogeneous_sibling_lists(
                    data=v,
                    tuple_list_ids=tuple_list_ids,
                )
                for v in data
            ):
                return True
            all_list_children: list[list[Value]] = [
                v for v in data if isinstance(v, list)
            ]
            seq_list_children = [
                v for v in all_list_children if id(v) not in tuple_list_ids
            ]
            return (
                len(all_list_children) == len(data)
                and len(seq_list_children) > 1
                and _all_scalars_heterogeneous(
                    values=[e for sub in seq_list_children for e in sub],
                )
            )
        case _:
            return False


@beartype
def _has_mixed_dict_shapes(*, data: Value) -> bool:
    """Recursively check whether data contains any list of dicts
    with different key sets.
    """
    match data:
        case dict():
            return any(_has_mixed_dict_shapes(data=v) for v in data.values())
        case list():
            dicts_in_list = [v for v in data if isinstance(v, dict)]
            key_sets = {frozenset(d.keys()) for d in dicts_in_list}
            has_mixed = (
                not all(ks == next(iter(key_sets)) for ks in key_sets)
                if key_sets
                else False
            )
            if has_mixed:
                return True
            return any(_has_mixed_dict_shapes(data=v) for v in data)
        case _:
            return False


def _has_mixed_record_shapes(
    *,
    data: Value,
    shapes_by_id: "Mapping[int, RecordShape]",
) -> bool:
    """Recursively check whether sibling dicts in *data* resolve to
    different :class:`RecordShape` values.

    Record-eligible dicts compare equal when their entry in
    *shapes_by_id* matches, so shapes that have been unified by the
    strategy are treated as compatible siblings.  Non-record-eligible
    dicts (e.g. ordered maps, empty dicts, dicts with non-string keys)
    are compared by raw key set as a conservative fallback.
    """
    match data:
        case dict():
            return any(
                _has_mixed_record_shapes(data=v, shapes_by_id=shapes_by_id)
                for v in data.values()
            )
        case list():
            dicts_in_list = [v for v in data if isinstance(v, dict)]
            signatures: set[object] = {
                shapes_by_id.get(id(d), frozenset(d.keys()))
                for d in dicts_in_list
            }
            if len(signatures) > 1:
                return True
            return any(
                _has_mixed_record_shapes(data=v, shapes_by_id=shapes_by_id)
                for v in data
            )
        case _:
            return False


@beartype
def _has_mixed_dict_keys(*, data: Value) -> bool:
    """Recursively check whether data contains any dict whose keys span
    multiple type families.
    """
    match data:
        case dict():
            keys: list[Value] = list(data.keys())
            if _values_mixed_types(values=keys):
                return True
            return any(_has_mixed_dict_keys(data=v) for v in data.values())
        case list():
            return any(_has_mixed_dict_keys(data=v) for v in data)
        case _:
            return False


@beartype
def _find_first_mixed_keys(*, data: Value) -> Sequence[Value]:
    """Return the keys of the first dict in *data* whose keys span
    multiple type families.
    """
    children: Sequence[Value]
    match data:
        case dict():
            keys: list[Value] = list(data.keys())
            if _values_mixed_types(values=keys):
                return keys
            children = list(data.values())
        case list():
            children = data
        case _:
            return []
    for child in children:
        result = _find_first_mixed_keys(data=child)
        if result:
            return result
    return []


@beartype
def _has_mixed_dict_values(
    *,
    data: Value,
    record_dict_ids: frozenset[int],
    tuple_list_ids: frozenset[int],
) -> bool:
    """Recursively check whether data contains any dict whose values span
    multiple type families.

    Dicts whose ``id`` is in *record_dict_ids* are skipped — they are
    carved out by the active RECORD heterogeneous strategy.  A value
    whose ``id`` is in *tuple_list_ids* is excluded from the
    type-family span of its parent dict: the TUPLE strategy renders
    that heterogeneous array as a single fixed-size tuple field, so it
    does not force the surrounding map to a heterogeneous value type.
    """
    match data:
        case dict():
            values: list[Value] = list(data.values())
            considered = [v for v in values if id(v) not in tuple_list_ids]
            if id(data) not in record_dict_ids and _values_mixed_types(
                values=considered
            ):
                return True
            return any(
                _has_mixed_dict_values(
                    data=v,
                    record_dict_ids=record_dict_ids,
                    tuple_list_ids=tuple_list_ids,
                )
                for v in values
            )
        case list():
            return any(
                _has_mixed_dict_values(
                    data=v,
                    record_dict_ids=record_dict_ids,
                    tuple_list_ids=tuple_list_ids,
                )
                for v in data
            )
        case _:
            return False


@beartype
def _has_dict_with_unwrappable_value_mix(
    *,
    data: Value,
    record_dict_ids: frozenset[int],
) -> bool:
    """Recursively check whether data contains any dict whose values span
    multiple type families and at least one value is a container.

    Wrapping strategies that only wrap scalars (tagged-enum / variant
    payload with no list/dict member) cannot uniformly type such a
    dict — scalar values would render wrapped while container values
    stay raw, and any two distinct non-scalar families (e.g. ``dict``
    and ``list``) cannot share a single map value type even after the
    wrapping.  The static-typed target rejects the resulting
    heterogeneous map.

    Dicts whose ``id`` is in *record_dict_ids* are skipped — they are
    carved out by the active RECORD heterogeneous strategy.
    """
    match data:
        case dict():
            values: list[Value] = list(data.values())
            has_container = any(
                isinstance(v, (list, dict, set)) for v in values
            )
            if (
                id(data) not in record_dict_ids
                and has_container
                and _values_mixed_types(values=values)
            ):
                return True
            return any(
                _has_dict_with_unwrappable_value_mix(
                    data=v,
                    record_dict_ids=record_dict_ids,
                )
                for v in values
            )
        case list():
            return any(
                _has_dict_with_unwrappable_value_mix(
                    data=v,
                    record_dict_ids=record_dict_ids,
                )
                for v in data
            )
        case _:
            return False


@beartype
def _has_mixed_list_values(
    *,
    data: Value,
    tuple_list_ids: frozenset[int],
) -> bool:
    """Recursively check whether data contains any list whose elements span
    multiple type families.

    Lists whose ``id`` is in *tuple_list_ids* are skipped — they are
    carved out by the active TUPLE heterogeneous strategy, which
    renders them as a fixed-size tuple whose positions may differ in
    type.
    """
    match data:
        case dict():
            return any(
                _has_mixed_list_values(data=v, tuple_list_ids=tuple_list_ids)
                for v in data.values()
            )
        case list():
            if id(data) not in tuple_list_ids and _values_mixed_types(
                values=data
            ):
                return True
            return any(
                _has_mixed_list_values(data=v, tuple_list_ids=tuple_list_ids)
                for v in data
            )
        case _:
            return False


@beartype
def _has_heterogeneous_set(*, data: Value) -> bool:
    """Recursively check whether data contains any set with
    heterogeneous scalar elements.
    """
    match data:
        case set():
            return _all_scalars_heterogeneous(values=list(data))
        case dict():
            return any(_has_heterogeneous_set(data=v) for v in data.values())
        case list():
            return any(_has_heterogeneous_set(data=v) for v in data)
        case _:
            return False


@beartype
def _check_heterogeneous(
    *,
    data: Value,
    record_dict_ids: frozenset[int],
    tuple_list_ids: frozenset[int],
) -> None:
    """Raise if data contains heterogeneous all-scalar collections."""
    if _has_heterogeneous(
        data=data,
        record_dict_ids=record_dict_ids,
        tuple_list_ids=tuple_list_ids,
    ):
        types = _describe_heterogeneous_types(data=data)
        msg = (
            "Collection contains heterogeneous scalar types that cannot "
            "be represented in the target language "
            f"(found types: {types})"
        )
        raise HeterogeneousScalarCollectionError(msg)


@beartype
def _check_heterogeneous_sibling_lists(
    *,
    data: Value,
    tuple_list_ids: frozenset[int],
) -> None:
    """Raise if sibling lists have heterogeneous scalar types."""
    if _has_heterogeneous_sibling_lists(
        data=data,
        tuple_list_ids=tuple_list_ids,
    ):
        types = _describe_heterogeneous_types(data=data)
        msg = (
            "Sibling lists contain heterogeneous scalar types that "
            "cannot be represented in the target language "
            f"(found types: {types})"
        )
        raise HeterogeneousSiblingListsError(msg)


@beartype
def _check_mixed_dict_shapes(*, data: Value) -> None:
    """Raise if data contains dicts with different key sets."""
    if _has_mixed_dict_shapes(data=data):
        msg = (
            "List contains dicts with different key sets that cannot "
            "be represented in the target language"
        )
        raise MixedDictShapesError(msg)


@beartype
def _check_mixed_dict_keys(*, data: Value) -> None:
    """Raise if any dict has keys spanning multiple type families."""
    if _has_mixed_dict_keys(data=data):
        keys = _find_first_mixed_keys(data=data)
        types = ", ".join(
            sorted({_value_type_family(value=k) for k in keys}),
        )
        msg = (
            "Dict contains keys of mixed types that cannot be "
            "represented in the target language "
            f"(found types: {types})"
        )
        raise MixedDictKeysError(msg)


@beartype
def _check_mixed_dict_values(
    *,
    data: Value,
    record_dict_ids: frozenset[int],
    tuple_list_ids: frozenset[int],
) -> None:
    """Raise if any dict has values spanning multiple type families."""
    if _has_mixed_dict_values(
        data=data,
        record_dict_ids=record_dict_ids,
        tuple_list_ids=tuple_list_ids,
    ):
        types = _describe_mixed_type_families(
            data=data,
            container_type=dict,
        )
        msg = (
            "Dict contains values of mixed types that cannot be "
            "represented in the target language "
            f"(found types: {types})"
        )
        raise MixedDictValuesError(msg)


@beartype
def _check_mixed_list_values(
    *,
    data: Value,
    tuple_list_ids: frozenset[int],
) -> None:
    """Raise if any list has elements spanning multiple type families."""
    if _has_mixed_list_values(data=data, tuple_list_ids=tuple_list_ids):
        types = _describe_mixed_type_families(
            data=data,
            container_type=list,
        )
        msg = (
            "List contains elements of mixed types that cannot be "
            "represented in the target language "
            f"(found types: {types})"
        )
        raise MixedListValuesError(msg)


@beartype
def _check_heterogeneous_set(*, data: Value) -> None:
    """Raise if data contains a set with heterogeneous scalar elements."""
    if _has_heterogeneous_set(data=data):
        msg = (
            "Set contains heterogeneous scalar elements that cannot be "
            "represented in the target language"
        )
        raise HeterogeneousSetError(msg)


# Two dicts whose values mix disjoint scalar types, used to probe whether
# a language's dict opener collapses mixed values to a stable
# "accepts anything" fallback or builds a content-specific type.  When
# the two openers differ the language uses variant/union typing (e.g.
# C++'s ``std::variant``) with no single value type that every sibling
# map converts to, so divergent sibling maps cannot be widened and must
# be rejected.  Both probes are non-empty and string-keyed so no
# language's opener depends on an empty-dict opener (which some
# strategies, e.g. D's ``RECORD``, reject).  Mirrors
# :data:`literalizer._literalize._DICT_FALLBACK_PROBE_A` / ``_B``.
_MIXED_VALUE_PROBE_A: dict[Scalar, Value] = {"_probe_a": 1, "_probe_b": "s"}
_MIXED_VALUE_PROBE_B: dict[Scalar, Value] = {
    "_probe_a": 1.5,
    "_probe_b": False,
}


@beartype
def _dict_slot_uses_variant_typing(*, spec: Language) -> bool:
    """Return whether *spec*'s dict opener builds a content-specific
    value type with no single type accepting every sibling map.

    True only for languages whose opener derives the value type from the
    values (variant/union typing, e.g. C++), so two dicts with different
    value content yield different openers; those have no "accepts
    anything" value type to widen a narrower sibling map into.  False for
    languages with a stable fallback (Go's ``map[string]any``, Kotlin's
    ``Any?``) and for dynamic languages whose opener ignores the values.

    A language whose opener rejects a heterogeneous-valued dict outright
    (e.g. D's narrow-typed mode) already raises on the real data through
    its own path, so the probe failure maps to ``False`` here.
    """
    dict_open = spec.dict_format_config.dict_open
    try:
        return dict_open(_MIXED_VALUE_PROBE_A) != dict_open(
            _MIXED_VALUE_PROBE_B
        )
    except (UnrepresentableInputError, HeterogeneousCollectionError):
        return False


@beartype
def _sibling_maps_diverge(
    *,
    pool: list[Value],
    spec: Language,
    record_dict_ids: frozenset[int],
) -> bool:
    """Return whether two or more maps sharing one declared value slot
    infer different dict openers.

    *pool* are the sibling values occupying a single declared value slot.
    Dicts rendered as records (``record_dict_ids``) are excluded because
    they render as their own struct type rather than a shared map slot.
    When the remaining maps' openers disagree, the enclosing container
    declares a widened map slot that the narrower inner maps do not fit.
    """
    dict_open = spec.dict_format_config.dict_open
    maps: list[dict[Scalar, Value]] = [
        item
        for item in pool
        if isinstance(item, dict)
        and not isinstance(item, OrderedMap)
        and id(item) not in record_dict_ids
    ]
    min_maps_for_divergence = 2
    if len(maps) < min_maps_for_divergence:
        return False
    filtered = [
        {
            k: v
            for k, v in d.items()
            if not (spec.skip_null_dict_values and v is None)
        }
        for d in maps
    ]
    return len({dict_open(d) for d in filtered}) > 1


@beartype
def _has_unrepresentable_sibling_maps(
    *,
    data: Value,
    spec: Language,
    record_dict_ids: frozenset[int],
    tuple_list_ids: frozenset[int],
) -> bool:
    """Return whether *data* holds sibling maps whose value types force a
    widened dict slot *spec* cannot represent.

    Walks *data* pooling sibling map values exactly as
    :func:`~literalizer._formatters.type_inference.infer_element_type`
    derives a container's declared type: a plain dict pools its own
    values, and a list of two or more plain dicts pools every element's
    values into one shared slot.  A pool whose maps disagree on their
    opener (see :func:`_sibling_maps_diverge`) declares a widened slot
    the language cannot represent.
    """
    match data:
        case OrderedMap():
            return any(
                _has_unrepresentable_sibling_maps(
                    data=value,
                    spec=spec,
                    record_dict_ids=record_dict_ids,
                    tuple_list_ids=tuple_list_ids,
                )
                for value in data.values()
            )
        case dict():
            if _sibling_maps_diverge(
                pool=list(data.values()),
                spec=spec,
                record_dict_ids=record_dict_ids,
            ):
                return True
            return any(
                _has_unrepresentable_sibling_maps(
                    data=value,
                    spec=spec,
                    record_dict_ids=record_dict_ids,
                    tuple_list_ids=tuple_list_ids,
                )
                for value in data.values()
            )
        case list():
            min_dicts_for_pooling = 2
            plain_dicts = [
                item
                for item in data
                if isinstance(item, dict) and not isinstance(item, OrderedMap)
            ]
            if (
                id(data) not in tuple_list_ids
                and len(plain_dicts) == len(data) >= min_dicts_for_pooling
            ):
                pooled = [
                    value
                    for element in plain_dicts
                    for value in element.values()
                ]
                if _sibling_maps_diverge(
                    pool=pooled,
                    spec=spec,
                    record_dict_ids=record_dict_ids,
                ):
                    return True
            return any(
                _has_unrepresentable_sibling_maps(
                    data=item,
                    spec=spec,
                    record_dict_ids=record_dict_ids,
                    tuple_list_ids=tuple_list_ids,
                )
                for item in data
            )
        case _:
            return False


@beartype
def _check_unrepresentable_sibling_maps(
    *,
    data: Value,
    spec: Language,
    record_dict_ids: frozenset[int],
    tuple_list_ids: frozenset[int],
) -> None:
    """Raise if *data* holds sibling maps whose widened dict slot *spec*
    cannot represent.

    *record_dict_ids* also includes maps whose selected strategy wraps
    every scalar child into one shared value carrier; those maps no
    longer rely on their content-specific normal opener and are equally
    safe to exclude from the divergence probe.
    """
    if _dict_slot_uses_variant_typing(spec=spec) and (
        _has_unrepresentable_sibling_maps(
            data=data,
            spec=spec,
            record_dict_ids=record_dict_ids,
            tuple_list_ids=tuple_list_ids,
        )
    ):
        msg = (
            "Container holds sibling maps whose value types force a "
            "widened dict slot that the target language cannot "
            "represent"
        )
        raise HeterogeneousSiblingMapsError(msg)


@beartype
def check_data(  # noqa: C901  # pylint: disable=too-complex
    *,
    data: Value,
    spec: Language,
) -> None:
    """Check that *data* fits the language's collection-shape
    constraints.

    Raises a subclass of
    :exc:`~literalizer.exceptions.HeterogeneousCollectionError` when the
    data cannot be represented in the target language's collection
    formats.
    """
    if spec.sequence_format_config.requires_uniform_record_shapes:
        _check_mixed_dict_shapes(data=data)

    seq_supports_het = spec.sequence_format_config.supports_heterogeneity
    dict_supports_het = spec.dict_supports_heterogeneous_values
    set_supports_het = spec.set_format_config.supports_heterogeneity
    behavior = spec.heterogeneous_behavior
    # Validate tuple arity before record-shape refinement asks the
    # tuple-aware field-type hook to derive a native tuple type.  In
    # particular, Kotlin only has Pair and Triple, and its hook cannot
    # type an otherwise eligible four-element tuple.
    compute_tuple_list_ids = behavior.compute_tuple_list_ids
    tuple_list_ids: frozenset[int] = (
        compute_tuple_list_ids(data)
        if compute_tuple_list_ids is not None
        else frozenset()
    )
    compute_record_shapes = behavior.compute_record_shapes
    record_shapes_by_id: Mapping[int, RecordShape] = (
        compute_record_shapes(data)
        if compute_record_shapes is not None
        else {}
    )
    record_dict_ids: frozenset[int] = frozenset(record_shapes_by_id)
    _check_unrepresentable_sibling_maps(
        data=data,
        spec=spec,
        record_dict_ids=(record_dict_ids | behavior.compute_wrap_ids(data)),
        tuple_list_ids=tuple_list_ids,
    )
    if behavior.render_record_literal is not None and _has_mixed_record_shapes(
        data=data,
        shapes_by_id=record_shapes_by_id,
    ):
        msg = (
            "Sibling list contains dicts with different record shapes; "
            "the RECORD heterogeneous strategy cannot represent a "
            "heterogeneous sequence of record shapes"
        )
        raise HeterogeneousSiblingListsError(msg)
    if not dict_supports_het:
        _check_mixed_dict_keys(data=data)
    if not behavior.skip_scalar_checks:
        # A scalar-wrapping or top-type-widening strategy (RECORD
        # widening a nested sibling map to a plain map, issue #2910)
        # makes the scalar children of each marked container
        # representable by one declared value type, so those containers
        # are exempt from the scalar-family checks -- the same carve-out
        # ``record_dict_ids`` grants.
        wrapped_dict_ids = record_dict_ids | behavior.compute_wrap_ids(data)
        if not seq_supports_het:
            _check_heterogeneous(
                data=data,
                record_dict_ids=wrapped_dict_ids,
                tuple_list_ids=tuple_list_ids,
            )
            _check_heterogeneous_sibling_lists(
                data=data,
                tuple_list_ids=tuple_list_ids,
            )
        if not dict_supports_het:
            _check_mixed_dict_values(
                data=data,
                record_dict_ids=wrapped_dict_ids,
                tuple_list_ids=tuple_list_ids,
            )
        if not seq_supports_het:
            _check_mixed_list_values(
                data=data,
                tuple_list_ids=tuple_list_ids,
            )
        if not set_supports_het:
            _check_heterogeneous_set(data=data)
    elif behavior.wrap_non_scalar is None:
        # A wrapping strategy that only wraps scalars cannot uniformly
        # represent a dict whose values span multiple type families and
        # include at least one container — the tagged-enum / variant
        # payload has no member that fits the container, and two
        # distinct non-scalar families share no map value type either.
        if not dict_supports_het and _has_dict_with_unwrappable_value_mix(
            data=data,
            record_dict_ids=record_dict_ids,
        ):
            msg = (
                "Dict has values of mixed type families including a "
                "container, which this heterogeneous strategy cannot "
                "represent"
            )
            raise MixedDictValuesError(msg)
