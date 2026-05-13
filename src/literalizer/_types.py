"""Type aliases used across the literalizer package."""

import datetime
from collections.abc import Mapping, Sequence

type Scalar = (
    str | int | float | bool | None | datetime.date | datetime.datetime | bytes
)
type Value = Scalar | list[Value] | dict[str, Value] | set[Scalar]
type ValueInput = (
    Scalar | Sequence[ValueInput] | Mapping[str, ValueInput] | set[Scalar]
)
