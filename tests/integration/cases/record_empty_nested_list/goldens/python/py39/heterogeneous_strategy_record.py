from __future__ import annotations
from typing import Any
import dataclasses
@dataclasses.dataclass(frozen=True)
class Record0:
    a: tuple[tuple[int, ...], ...]
    b: tuple[tuple[Any, ...] | tuple[int, ...], ...]
my_data = Record0(
    a=(
        (
            1,
            2,
        ),
        (
            3,
        ),
    ),
    b=(
        (),
        (
            1,
        ),
    ),
)
