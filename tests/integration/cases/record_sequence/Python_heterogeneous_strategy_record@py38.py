from __future__ import annotations
from typing import Any
import dataclasses
@dataclasses.dataclass(frozen=True)
class Record0:
    id: int
    label: str
    tags: tuple[Any, ...]
my_data = (
    Record0(id=1, label="first", tags=()),
    Record0(id=2, label="second", tags=()),
    Record0(id=3, label="third", tags=()),
)
