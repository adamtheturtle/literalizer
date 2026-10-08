from __future__ import annotations
from typing import Any
import dataclasses
@dataclasses.dataclass(frozen=True)
class Record0:
    a: tuple[int | tuple[Any, ...], ...]
my_data = Record0(
    a=(
        1,
        (),
    ),
)
