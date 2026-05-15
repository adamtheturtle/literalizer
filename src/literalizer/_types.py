"""Type aliases used across the literalizer package."""

import datetime
from collections.abc import Mapping, Sequence

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
type ValueInput = (
    Scalar | Sequence[ValueInput] | Mapping[Scalar, ValueInput] | set[Scalar]
)


class OrderedMap(dict[Scalar, Value]):
    """An order-significant mapping (a YAML ``!!omap``).

    Literalizer treats a plain :class:`dict` as unordered and therefore
    record-eligible, while an ``OrderedMap`` is always rendered
    positionally and never collapsed into a record. This is the only
    distinction the type carries: it is a bare :class:`dict` subclass
    (every ``dict`` is insertion-ordered since Python 3.7) used purely
    as a nominal tag, so it remains a valid ``Value``/``ValueInput`` and
    keeps plain-``dict`` equality semantics.

    This type is owned by literalizer so that ordered-map detection does
    not depend on a third-party YAML library's class hierarchy. The YAML
    parser (the only ruamel boundary) converts ``!!omap`` nodes into
    ``OrderedMap``; everything downstream dispatches on this type alone.
    """
