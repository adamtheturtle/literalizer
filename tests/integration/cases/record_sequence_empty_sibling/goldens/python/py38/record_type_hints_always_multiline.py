from __future__ import annotations
from typing import Any
import dataclasses
@dataclasses.dataclass(frozen=True)
class Record0:
    x: int
my_data: tuple[tuple[Any, ...] | tuple[Record0, ...], ...] = (
    (),
    (
        Record0(
            x=1,
        ),
    ),
)
