from __future__ import annotations
import dataclasses
@dataclasses.dataclass(frozen=True)
class Record1:
    a: int
    b: str
    c: None
@dataclasses.dataclass(frozen=True)
class Record0:
    outer: Record1
my_data = Record0(
    outer=Record1(
        a=1,
        b="x",
        c=None,
    ),
)
