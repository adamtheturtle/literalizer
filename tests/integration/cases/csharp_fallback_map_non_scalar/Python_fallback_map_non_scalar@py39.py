from __future__ import annotations
import dataclasses
@dataclasses.dataclass(frozen=True)
class Record1:
    scalar: int
    items: tuple[int, ...]
@dataclasses.dataclass(frozen=True)
class Record0:
    name: str
    payload: Record1
@dataclasses.dataclass(frozen=True)
class Record2:
    other: int
my_data = (
    Record0(name="one", payload=Record1(scalar=1, items=(2, 3))),
    Record0(name="two", payload=Record2(other=2)),
)
