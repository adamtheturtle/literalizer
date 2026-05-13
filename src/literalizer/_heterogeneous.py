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
from ruamel.yaml.compat import ordereddict

from literalizer._types import Scalar, Value


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
def _collect_from_dict(data: dict[str, Value]) -> frozenset[int]:
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
    subdicts: list[dict[str, Value]] = [v for v in data if isinstance(v, dict)]
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
        case ordereddict() | dict():
            return _collect_from_dict(data=data)
        case list():
            return _collect_from_list(data=data)
        case _:
            return frozenset()


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
        case ordereddict() | dict():
            children: list[Value] = list(data.values())  # pyright: ignore[reportUnknownMemberType,reportUnknownArgumentType]
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
