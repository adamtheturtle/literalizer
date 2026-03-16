"""Type aliases used across the literalizer package."""

from __future__ import annotations

import datetime

type Scalar = (
    str | int | float | bool | None | datetime.date | datetime.datetime | bytes
)
type Value = Scalar | list[Value] | dict[str, Value] | set[Scalar]
