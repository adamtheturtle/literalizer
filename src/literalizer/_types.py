"""Type aliases used across the literalizer package."""

import datetime

type Scalar = (
    str | int | float | bool | None | datetime.date | datetime.datetime | bytes
)
type Value = Scalar | list[Value] | dict[str, Value] | set[Scalar]
