from __future__ import annotations
import dataclasses
@dataclasses.dataclass(frozen=True)
class Record1:
    age: int
@dataclasses.dataclass(frozen=True)
class Record0:
    name: str
    active: bool
    count: int
    score: float
    missing: None
    scores: tuple[int, ...]
    child: Record1
my_data: tuple[Record0, ...] = (
    Record0(name="Ada", active=True, count=1, score=1.5, missing=None, scores=(1, 2), child=Record1(age=3)),
    Record0(name="Bob", active=False, count=2, score=2.5, missing=None, scores=(4,), child=Record1(age=5)),
)
