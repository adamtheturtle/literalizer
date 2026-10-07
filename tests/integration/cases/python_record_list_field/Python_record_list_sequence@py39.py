from __future__ import annotations
import dataclasses
@dataclasses.dataclass(frozen=True)
class Record1:
    a: int
@dataclasses.dataclass(frozen=True)
class Record0:
    items: list[Record1]
my_data = Record0(
    items=[
        Record1(
            a=1,
        ),
    ],
)
