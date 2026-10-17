from __future__ import annotations
import dataclasses
@dataclasses.dataclass(frozen=True)
class Record0:
    short: list[int]
    long: list[int]
my_data = Record0(
    short=[
        1,
    ],
    long=[
        1,
        2,
    ],
)
