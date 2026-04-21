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

_SCALAR_BUCKETS: tuple[type, ...] = (
    bool,
    int,
    float,
    str,
    bytes,
    datetime.datetime,
    datetime.date,
)


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
    for bucket in _SCALAR_BUCKETS:
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
def _flag_if_siblings_mixed(
    *,
    siblings: Sequence[Value],
    total: int,
    combined: list[Value],
    ids: set[int],
) -> None:
    """Flag every sibling in *siblings* when *combined* has mixed
    scalar buckets.

    *total* is the parent list's element count: when the sibling count
    differs, the parent contains non-matching children and the rule
    does not apply.
    """
    if len(siblings) != total or len(siblings) <= 1:
        return
    if not _all_scalars_mixed_buckets(values=combined):
        return
    for sibling in siblings:
        ids.add(id(sibling))


@beartype
def _collect_from_dict(
    data: dict[str, Value],
    *,
    ids: set[int],
) -> None:
    """Collect ids for a dict and its children."""
    values: list[Value] = list(data.values())
    if _all_scalars_mixed_buckets(values=values):
        ids.add(id(data))
    for v in values:
        _collect_container_ids(data=v, ids=ids)


@beartype
def _collect_from_list(
    data: list[Value],
    *,
    ids: set[int],
) -> None:
    """Collect ids for a list, its sibling children, and descendants."""
    if _all_scalars_mixed_buckets(values=data):
        ids.add(id(data))
    sublists: list[list[Value]] = [v for v in data if isinstance(v, list)]
    _flag_if_siblings_mixed(
        siblings=sublists,
        total=len(data),
        combined=[e for sublist in sublists for e in sublist],
        ids=ids,
    )
    subdicts: list[dict[str, Value]] = [v for v in data if isinstance(v, dict)]
    _flag_if_siblings_mixed(
        siblings=subdicts,
        total=len(data),
        combined=[v for d in subdicts for v in d.values()],
        ids=ids,
    )
    for v in data:
        _collect_container_ids(data=v, ids=ids)


@beartype
def _collect_container_ids(
    data: Value,
    *,
    ids: set[int],
) -> None:
    """Populate *ids* with container ids whose scalar children need
    wrapping.

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
            _collect_from_dict(data=data, ids=ids)
        case list():
            _collect_from_list(data=data, ids=ids)
        case _:
            pass


@beartype
def collect_heterogeneous_container_ids(data: Value) -> frozenset[int]:
    """Return container ids whose scalar children need wrapping."""
    ids: set[int] = set()
    _collect_container_ids(data=data, ids=ids)
    return frozenset(ids)


@beartype
def iter_wrapped_scalars(
    data: Value,
    *,
    wrap_ids: frozenset[int],
) -> list[Scalar]:
    """Return scalars that will be wrapped when rendering *data*.

    Walks *data* and yields each scalar whose immediate container's id
    appears in *wrap_ids*.
    """
    out: list[Scalar] = []

    def _walk(value: Value) -> None:
        """Walk *value* and collect scalars that will be wrapped."""
        match value:
            case ordereddict() | dict():
                parent_wrapped = id(value) in wrap_ids
                dict_values: list[Value] = list(value.values())  # pyright: ignore[reportUnknownMemberType,reportUnknownArgumentType]
                for v in dict_values:
                    if parent_wrapped and not isinstance(
                        v,
                        (list, dict, set),
                    ):
                        out.append(v)
                    _walk(value=v)
            case list():
                parent_wrapped = id(value) in wrap_ids
                for v in value:
                    if parent_wrapped and not isinstance(
                        v,
                        (list, dict, set),
                    ):
                        out.append(v)
                    _walk(value=v)
            case _:
                pass

    _walk(value=data)
    return out
