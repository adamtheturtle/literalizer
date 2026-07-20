"""Type aliases used across the literalizer package."""

import datetime
from collections.abc import Iterable, Sequence
from typing import Protocol, runtime_checkable

type Scalar = (
    str
    | int
    | float
    | bool
    | None
    | datetime.date
    | datetime.datetime
    | datetime.time
    | bytes
)
type Value = Scalar | list[Value] | dict[Scalar, Value] | set[Scalar]


class CallPreambleData(list[Value]):
    """Call-rendering preamble input with its rendered arguments.

    ``literalize_call(per_element=True)`` uses its outer list and any
    nested row lists as call structure, rather than rendering those
    containers as literals.  ``argument_values`` retains the values that
    actually appear in the generated calls for language preambles whose
    type discovery depends on container structure.  ``argument_slots``
    also preserves positional grouping across calls for strategies that
    widen siblings in the same parameter slot.
    """

    def __init__(
        self,
        data: list[Value],
        *,
        argument_values: tuple[Value, ...],
        argument_slots: tuple[list[Value], ...],
    ) -> None:
        """Store the original preamble data and rendered arguments."""
        super().__init__(data)
        self.argument_values = argument_values
        self.argument_slots = argument_slots


@runtime_checkable
class ValueItemsMap[K, V](Protocol):
    """Covariant-key read-only view of the mapping arm of ``ValueInput``.

    A plain :class:`~collections.abc.Mapping`'s key parameter is
    invariant, so an inline ``dict`` literal -- inferred with a narrow
    key type such as ``str`` or ``int`` -- is not assignable to
    ``Mapping[Scalar, ValueInput]`` even though every concrete scalar
    key type *is* a ``Scalar``.  The only operation literalizer
    performs on this arm is iterating ``items()`` (see
    ``_materialize_value_input``), so representing it as a read-only
    ``items()`` view places ``K``/``V`` solely in an output position;
    PEP 695 then infers them covariant, and any scalar-keyed mapping
    literal is accepted without an explicit annotation.
    """

    def items(self) -> Iterable[tuple[K, V]]:
        """Yield the key/value pairs."""
        ...  # pylint: disable=unnecessary-ellipsis


type ValueInput = (
    Scalar
    | Sequence[ValueInput]
    | ValueItemsMap[Scalar, ValueInput]
    | set[Scalar]
)


class OrderedMap(dict[Scalar, Value]):
    """An order-significant mapping (a YAML ``!!omap``).

    Literalizer treats a plain :class:`dict` as unordered and therefore
    record-eligible, while an ``OrderedMap`` is always rendered
    positionally and never collapsed into a record. This is the only
    distinction the type carries: it is a bare :class:`dict` subclass
    (every ``dict`` is insertion-ordered since Python 3.7) used purely
    as a nominal tag, so it stays a valid ``Value`` and ``ValueInput``
    while keeping plain ``dict`` equality semantics.

    This type is owned by literalizer so that ordered-map detection does
    not depend on a third-party YAML library's class hierarchy. The YAML
    parser (the only ruamel boundary) converts ``!!omap`` nodes into
    ``OrderedMap``; everything downstream dispatches on this type alone.
    """
