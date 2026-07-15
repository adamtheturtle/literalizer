"""Scope detection and orchestration for the ``TUPLE`` heterogeneous
strategy.

The ``TUPLE`` strategy renders a fixed-length heterogeneous scalar
array as a native fixed-size tuple instead of rejecting it.  This
module owns the language-agnostic scope boundary -- which lists in a
data tree are tuple-eligible -- and the orchestration that composes
``TUPLE`` with ``RECORD`` (a record field whose value is such an array
becomes a tuple-typed field).

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

:func:`build_tuple_strategy` is the counterpart of
:func:`~literalizer._formatters.record_strategy.build_record_strategy`
for languages whose ``TUPLE`` strategy composes ``RECORD`` through the
shared record machinery: it wraps a :class:`RecordRenderer` so a
tuple-eligible record field is typed by a :class:`TupleRenderer`, adds
the tuple render hook, and validates each eligible array's length at
check time (raising :class:`TupleArityNotRepresentableError` for a
length the target language has no native tuple for, rather than
falling back to a homogeneous list).
"""

import dataclasses
from collections.abc import Callable, Sequence

from beartype import beartype

from literalizer._checks import scalar_type_bucket
from literalizer._formatters.record_strategy import (
    RecordFieldType,
    RecordRenderer,
    RecordStrategy,
    build_record_strategy,
)
from literalizer._language import RenderedTupleLiteral
from literalizer._types import Value
from literalizer.exceptions import TupleArityNotRepresentableError


@beartype
def is_tuple_eligible(*, value: list[Value]) -> bool:
    """Return whether *value* is a tuple-eligible heterogeneous array.

    Eligible when every element is a scalar and the elements span at
    least two distinct scalar type buckets.  An empty list, a list
    with any non-scalar element, and a homogeneous list (one bucket)
    are all ineligible.

    This is the structural half of tuple-eligibility (the positional
    half -- a list must be a dict value or the document root -- is
    enforced by :func:`collect_tuple_lists` and by the caller's
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
def _accumulate_tuple_lists(
    *,
    data: Value,
    out: list[list[Value]],
) -> None:
    """Walk *data* recording each tuple-eligible dict-value list.

    Only lists reached as a dict value are recorded here; lists
    reached as an element of another list are deliberately skipped
    (the nested-list / sibling-list shapes stay out of scope) while
    still being walked so deeper dict-value lists are found.
    """
    match data:
        case dict():
            for child in data.values():
                if isinstance(child, list) and is_tuple_eligible(
                    value=child,
                ):
                    out.append(child)
                _accumulate_tuple_lists(data=child, out=out)
        case list():
            for item in data:
                _accumulate_tuple_lists(data=item, out=out)
        case _:
            return


@beartype
def collect_tuple_lists(*, data: Value) -> list[list[Value]]:
    """Return every tuple-eligible list in *data*, in document order.

    The document root is eligible when it is itself a tuple-eligible
    heterogeneous scalar array; every other eligible list is a dict
    value reached during the walk.
    """
    out: list[list[Value]] = []
    if isinstance(data, list) and is_tuple_eligible(value=data):
        out.append(data)
    _accumulate_tuple_lists(data=data, out=out)
    return out


@beartype
def collect_tuple_list_ids(*, data: Value) -> frozenset[int]:
    """Return ``id(list)`` for every tuple-eligible list in *data*."""
    return frozenset(id(lst) for lst in collect_tuple_lists(data=data))


@dataclasses.dataclass(frozen=True)
class TupleRenderer:
    """Per-language syntax hooks for the ``TUPLE`` strategy.

    ``render_literal`` builds the tuple literal as a
    :class:`RenderedTupleLiteral` (structured pieces the shared
    :mod:`literalizer._literalize` layout code assembles into compact
    or multiline form) from the raw list and its pre-formatted
    elements -- the same signature as
    :attr:`HeterogeneousBehavior.render_tuple_literal`.  ``field_type``
    maps the per-position element values of a tuple-eligible
    ``RECORD`` field to the declared tuple type (e.g.
    ``Pair<Int, String>``).  ``representable_arity`` returns whether
    the language has a native fixed-size tuple of the given length;
    :func:`build_tuple_strategy` raises
    :class:`TupleArityNotRepresentableError` for an eligible array
    whose length it rejects rather than degrading to a homogeneous
    list.
    """

    render_literal: Callable[
        [list[Value], Sequence[str]],
        RenderedTupleLiteral,
    ]
    field_type: Callable[[list[Value]], str]
    representable_arity: Callable[[int], bool]


@beartype
def build_tuple_strategy(
    *,
    record_renderer: RecordRenderer,
    tuple_renderer: TupleRenderer,
) -> RecordStrategy:
    """Build the behavior + preamble for a ``TUPLE`` strategy that
    composes ``RECORD`` through the shared record machinery.

    Wraps *record_renderer* so a record field whose value is a
    tuple-eligible heterogeneous scalar array is typed by
    *tuple_renderer* (every record field is a dict value, so the
    structural :func:`is_tuple_eligible` predicate is exactly the
    field's tuple-eligibility), then adds the tuple render hook and a
    ``compute_tuple_list_ids`` hook that validates every eligible
    array's length at check time -- raising
    :class:`TupleArityNotRepresentableError` for a length the language
    has no native tuple for instead of falling back to a homogeneous
    list (which would re-trip the heterogeneity checks).
    """

    def _tuple_aware_field_type(request: RecordFieldType) -> str:
        """Type a tuple-eligible record field via *tuple_renderer*;
        defer every other field to *record_renderer*.
        """
        value = request.value
        if isinstance(value, list) and is_tuple_eligible(value=value):
            return tuple_renderer.field_type(value)
        return record_renderer.field_type(request)

    wrapped_renderer = dataclasses.replace(
        record_renderer,
        field_type=_tuple_aware_field_type,
    )
    # Field-type splitting (issue #2888) is a plain-``RECORD`` port; the
    # ``TUPLE`` composition (shared across languages) keeps its existing
    # behavior until ported in its own increment.
    record_strategy = build_record_strategy(
        renderer=wrapped_renderer,
        split_conflicting_field_types=False,
        widen_unrecordizable_nested_sibling_maps=False,
        derecordized_map_open=None,
    )

    def _compute_tuple_list_ids(data: Value, /) -> frozenset[int]:
        """Return the tuple-eligible list ids, raising for any whose
        length the language has no native tuple for.
        """
        lists = collect_tuple_lists(data=data)
        for lst in lists:
            if not tuple_renderer.representable_arity(len(lst)):
                raise TupleArityNotRepresentableError(arity=len(lst))
        return frozenset(id(lst) for lst in lists)

    behavior = dataclasses.replace(
        record_strategy.behavior,
        render_tuple_literal=tuple_renderer.render_literal,
        compute_tuple_list_ids=_compute_tuple_list_ids,
    )
    return RecordStrategy(behavior=behavior, preamble=record_strategy.preamble)
