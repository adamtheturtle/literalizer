"""Shared helpers for heterogeneous-scalar wrapping strategies.

Languages that opt into a render-time wrapping strategy (e.g.
``Rust.HeterogeneousStrategies.TAGGED_ENUM``,
``Dhall.HeterogeneousStrategies.UNION_TYPE``) use these pure
data-shape walks to identify which container ids need their scalar
children wrapped and to iterate those scalars when building the
type declaration.
"""

import datetime
from collections.abc import Sequence

from beartype import beartype

from literalizer._types import OrderedMap, Scalar, Value


@beartype
def _scalar_bucket(value: Value) -> type | None:
    """Return the scalar-bucket type for *value*, or ``None`` for
    non-scalars.

    More specific subclasses (``bool`` before ``int``,
    ``datetime.datetime`` before ``datetime.date``) are checked first.
    ``None`` values return ``type(None)``.
    """
    if value is None:
        return type(None)
    buckets: tuple[type, ...] = (
        bool,
        int,
        float,
        str,
        bytes,
        datetime.datetime,
        datetime.date,
        datetime.time,
    )
    for bucket in buckets:
        if isinstance(value, bucket):
            return bucket
    return None


@beartype
def _all_scalars_mixed_buckets(values: Sequence[Value]) -> bool:
    """Return ``True`` when *values* are all scalars spanning more than
    one type bucket.
    """
    buckets: set[type] = set()
    for v in values:
        bucket = _scalar_bucket(value=v)
        if bucket is None:
            return False
        buckets.add(bucket)
    return len(buckets) > 1


@beartype
def _siblings_mixed_ids(
    *,
    siblings: Sequence[Value],
    total: int,
    combined: list[Value],
) -> frozenset[int]:
    """Return ids for *siblings* when *combined* spans mixed scalar
    buckets.

    *total* is the parent list's element count: when the sibling count
    differs, the parent contains non-matching children and the rule
    does not apply.
    """
    if len(siblings) != total or len(siblings) <= 1:
        return frozenset()
    if not _all_scalars_mixed_buckets(values=combined):
        return frozenset()
    return frozenset(id(sibling) for sibling in siblings)


@beartype
def _collect_from_dict(data: dict[Scalar, Value]) -> frozenset[int]:
    """Return container ids for a dict, its sibling-list values, and
    descendants.
    """
    values: list[Value] = list(data.values())
    own: frozenset[int] = (
        frozenset({id(data)})
        if _all_scalars_mixed_buckets(values=values)
        else frozenset()
    )
    sublists: list[list[Value]] = [v for v in values if isinstance(v, list)]
    sublist_ids = _siblings_mixed_ids(
        siblings=sublists,
        total=len(values),
        combined=[e for sublist in sublists for e in sublist],
    )
    descendants = frozenset[int]().union(
        *(collect_heterogeneous_container_ids(data=v) for v in values)
    )
    return own | sublist_ids | descendants


@beartype
def _collect_from_list(data: list[Value]) -> frozenset[int]:
    """Return container ids for a list, its sibling children, and
    descendants.
    """
    own: frozenset[int] = (
        frozenset({id(data)})
        if _all_scalars_mixed_buckets(values=data)
        else frozenset()
    )
    sublists: list[list[Value]] = [v for v in data if isinstance(v, list)]
    sublist_ids = _siblings_mixed_ids(
        siblings=sublists,
        total=len(data),
        combined=[e for sublist in sublists for e in sublist],
    )
    subdicts: list[dict[Scalar, Value]] = [
        v for v in data if isinstance(v, dict)
    ]
    subdict_ids = _siblings_mixed_ids(
        siblings=subdicts,
        total=len(data),
        combined=[v for d in subdicts for v in d.values()],
    )
    descendants = frozenset[int]().union(
        *(collect_heterogeneous_container_ids(data=v) for v in data)
    )
    return own | sublist_ids | subdict_ids | descendants


@beartype
def collect_heterogeneous_container_ids(*, data: Value) -> frozenset[int]:
    """Return container ids whose scalar children need wrapping.

    A container is a target when:

    * it is a dict whose values are all scalars of mixed buckets; or
    * it is a list whose elements are all scalars of mixed buckets; or
    * it is a list that is a child of another list whose children are
      all lists and whose combined leaf scalars are heterogeneous
      (sibling-list heterogeneity); or
    * it is a dict in a list of sibling dicts whose combined scalar
      values are heterogeneous (sibling-dict heterogeneity).
    """
    match data:
        case dict():
            return _collect_from_dict(data=data)
        case list():
            return _collect_from_list(data=data)
        case _:
            return frozenset()


@beartype
def _widen_sibling_map_wrap_ids(*, pool: Sequence[Value]) -> frozenset[int]:
    """Return sibling maps sharing one value slot that must widen.

    *pool* are the sibling values occupying a single declared value slot
    (every value of an enclosing dict, or every value pooled across a
    list of sibling dicts).  When two or more of them are plain maps
    those maps must share one value type.  If the maps' own values are
    all scalars spanning more than one bucket that shared type is the
    tagged-enum ``Value``, so every map in the group -- including any
    whose values are individually homogeneous -- has its scalar children
    wrapped.  Otherwise the shared slot is itself a map type and the
    maps' pooled values form the next slot, widened in turn so nesting
    deeper than one level widens too.
    """
    maps: list[dict[Scalar, Value]] = [
        item
        for item in pool
        if isinstance(item, dict) and not isinstance(item, OrderedMap)
    ]
    min_maps_for_widening = 2
    if len(maps) < min_maps_for_widening:
        return frozenset()
    child_pool: list[Value] = [value for m in maps for value in m.values()]
    if _all_scalars_mixed_buckets(values=child_pool):
        return frozenset(id(m) for m in maps)
    return _widen_sibling_map_wrap_ids(pool=child_pool)


@beartype
def collect_sibling_map_wrap_ids(*, data: Value) -> frozenset[int]:
    """Return map ids needing scalar wrapping from sibling widening.

    Sibling dict values that are themselves maps share one declared
    value type in the enclosing container, but each inner map otherwise
    renders with its own value type, so a map whose values are narrower
    than the widened slot type does not compile (issue #2879; the
    scalar-wrapping analogue of the sibling widening #1471/#1472 applied
    to call arguments and sequence elements).

    The values of a plain dict share one declared value slot; a list of
    two or more plain dicts makes those dicts one shared type, so their
    values share a single slot pooled across every element.  Both are
    handed to :func:`_widen_sibling_map_wrap_ids`, which descends nested
    levels.  ``OrderedMap`` values are record fields with independent
    types, so they are only descended into, never pooled.

    The returned ids are additional to
    :func:`collect_heterogeneous_container_ids`: they cover maps that are
    individually homogeneous yet must widen because a sibling map at the
    same slot does.
    """
    match data:
        case OrderedMap():
            own: frozenset[int] = frozenset()
            children: list[Value] = list(data.values())
        case dict():
            own = _widen_sibling_map_wrap_ids(pool=list(data.values()))
            children = list(data.values())
        case list():
            min_dicts_for_widening = 2
            plain_dicts = [
                item
                for item in data
                if isinstance(item, dict) and not isinstance(item, OrderedMap)
            ]
            pooled: list[Value] = [
                value for element in plain_dicts for value in element.values()
            ]
            own = (
                _widen_sibling_map_wrap_ids(pool=pooled)
                if len(plain_dicts) == len(data) >= min_dicts_for_widening
                else frozenset()
            )
            children = list(data)
        case _:
            return frozenset()
    descendants = frozenset[int]().union(
        *(collect_sibling_map_wrap_ids(data=child) for child in children)
    )
    return own | descendants


@beartype
def iter_wrapped_scalars(
    *,
    data: Value,
    wrap_ids: frozenset[int],
) -> list[Scalar]:
    """Return scalars that will be wrapped when rendering *data*.

    Walks *data* and yields each scalar whose immediate container's id
    appears in *wrap_ids*.
    """
    match data:
        case dict():
            children: list[Value] = list(data.values())
        case list():
            children = list(data)
        case _:
            return []
    parent_wrapped = id(data) in wrap_ids
    out: list[Scalar] = []
    for child in children:
        if parent_wrapped and not isinstance(child, (list, dict, set)):
            out.append(child)
        out.extend(iter_wrapped_scalars(data=child, wrap_ids=wrap_ids))
    return out
