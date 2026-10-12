from __future__ import annotations
import dataclasses
@dataclasses.dataclass(frozen=True)
class Record0:
    a: int
    b: str
my_data = Record0(
    a=1,
    b="x",
)
