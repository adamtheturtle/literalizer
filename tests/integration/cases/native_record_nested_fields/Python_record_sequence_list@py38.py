from __future__ import annotations
import dataclasses
@dataclasses.dataclass(frozen=True)
class Record1:
    name: str
    active: bool
@dataclasses.dataclass(frozen=True)
class Record2:
    name: str
    score: float
@dataclasses.dataclass(frozen=True)
class Record0:
    owner: Record1
    members: list[Record2]
my_data = Record0(
    owner=Record1(
        name="Ada",
        active=False,
    ),
    members=[
        Record2(
            name="Ada",
            score=1.5,
        ),
        Record2(
            name="Bob",
            score=2.5,
        ),
    ],
)
