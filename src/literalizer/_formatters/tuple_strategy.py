"""Scope detection for the ``TUPLE`` heterogeneous strategy.

The ``TUPLE`` strategy renders a fixed-length heterogeneous scalar
array as a native fixed-size tuple instead of rejecting it.  This
module owns the language-agnostic scope boundary: which lists in a
data tree are tuple-eligible.

A list is tuple-eligible when it is a dict value (a record field
value is a dict value) or the document root, every element is a
scalar, and the elements span at least two scalar type buckets
(length is therefore at least two).  Lists nested directly inside
another list -- and the equivalent sibling-list shape -- are out of
scope: they keep raising as before because they have no single
representable element type and no unambiguous tuple parent.  Lists
containing any non-scalar element are likewise out of scope.

:func:`collect_tuple_list_ids` returns the ``id(list)`` of every
tuple-eligible list so :func:`~literalizer._checks.check_data` can
carve them out of the heterogeneous-scalar checks and
:mod:`literalizer._literalize` can render them as tuples.  It is the
counterpart of
:func:`~literalizer._formatters.type_inference.collect_record_shapes`,
keyed on list ids rather than dict ids (a heterogeneous array is a
``list``, invisible to record-shape detection).
"""

from beartype import beartype

from literalizer._checks import scalar_type_bucket
from literalizer._types import Value


@beartype
def is_tuple_eligible(*, value: list[Value]) -> bool:
    """Return whether *value* is a tuple-eligible heterogeneous array.

    Eligible when every element is a scalar and the elements span at
    least two distinct scalar type buckets.  An empty list, a list
    with any non-scalar element, and a homogeneous list (one bucket)
    are all ineligible.

    This is the structural half of tuple-eligibility (the positional
    half -- a list must be a dict value or the document root -- is
    enforced by :func:`collect_tuple_list_ids` and by the caller's
    position when a language's type inference reuses this predicate
    directly).
    """
    buckets: set[type] = set()
    for element in value:
        bucket = scalar_type_bucket(value=element)
        if bucket is None:
            return False
        buckets.add(bucket)
    # ``> 1`` (rather than ``>= 2``) mirrors
    # ``literalizer._checks._all_scalars_heterogeneous`` and keeps the
    # "spans more than one scalar bucket" rule in one phrasing.
    return len(buckets) > 1


@beartype
def _accumulate_tuple_list_ids(
    *,
    data: Value,
    out: set[int],
) -> None:
    """Walk *data* recording the ids of tuple-eligible dict-value lists.

    Only lists reached as a dict value are marked here; lists reached
    as an element of another list are deliberately skipped (the
    nested-list / sibling-list shapes stay out of scope) while still
    being walked so deeper dict-value lists are found.
    """
    match data:
        case dict():
            for child in data.values():
                if isinstance(child, list) and is_tuple_eligible(
                    value=child,
                ):
                    out.add(id(child))
                _accumulate_tuple_list_ids(data=child, out=out)
        case list():
            for item in data:
                _accumulate_tuple_list_ids(data=item, out=out)
        case _:
            return


@beartype
def collect_tuple_list_ids(*, data: Value) -> frozenset[int]:
    """Return ``id(list)`` for every tuple-eligible list in *data*.

    The document root is eligible when it is itself a tuple-eligible
    heterogeneous scalar array; every other eligible list is a dict
    value reached during the walk.
    """
    out: set[int] = set()
    if isinstance(data, list) and is_tuple_eligible(value=data):
        out.add(id(data))
    _accumulate_tuple_list_ids(data=data, out=out)
    return frozenset(out)
