from __future__ import annotations
import dataclasses
@dataclasses.dataclass(frozen=True)
class Record1:
    name: str
    age: int
@dataclasses.dataclass(frozen=True)
class Record0:
    id: int
    owner: Record1
my_data = Record0(
    id=1,
    owner=Record1(
        name="Alice",
        age=30,
    ),
)
