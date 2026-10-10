from __future__ import annotations
import dataclasses
@dataclasses.dataclass(frozen=True)
class Record0:
    name: str
    age: int
    active: bool
    score: float
my_data = Record0(
    name="Alice",
    age=30,
    active=True,
    score=4.5,
)
