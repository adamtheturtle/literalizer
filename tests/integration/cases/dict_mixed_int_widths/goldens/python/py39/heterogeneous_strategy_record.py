from __future__ import annotations
import dataclasses
@dataclasses.dataclass(frozen=True)
class Record0:
    a: int
    b: int
    c: str
my_data = Record0(
    a=1,
    b=3000000000,
    c="x",
)
