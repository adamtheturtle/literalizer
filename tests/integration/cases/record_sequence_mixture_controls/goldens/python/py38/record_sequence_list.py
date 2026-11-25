from __future__ import annotations
from typing import Any
import dataclasses
@dataclasses.dataclass(frozen=True)
class Record0:
    x: int
my_data: list[list[list[int] | Record0] | list[Record0] | list[list[Any] | list[Record0]] | list[list[Any]]] = [
    [[1], Record0(x=1)],
    [Record0(x=1), Record0(x=2)],
    [[], [Record0(x=1)]],
    [[], []],
]
