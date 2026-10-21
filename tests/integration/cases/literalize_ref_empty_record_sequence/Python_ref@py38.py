from __future__ import annotations
from typing import Any
import dataclasses
@dataclasses.dataclass(frozen=True)
class Record0:
    x: int
empty_items: tuple[Any, ...] = ()
populated_items = (
    Record0(x=1),
)
my_data: tuple[tuple[Any, ...] | tuple[Record0, ...], ...] = (
    empty_items,
    populated_items,
)
