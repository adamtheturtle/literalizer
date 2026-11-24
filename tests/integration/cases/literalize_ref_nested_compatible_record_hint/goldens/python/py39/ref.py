from __future__ import annotations
import dataclasses
@dataclasses.dataclass(frozen=True)
class Record1:
    items: tuple[int, ...]
@dataclasses.dataclass(frozen=True)
class Record0:
    outer: Record1
record_data = Record1(
    items=(
        1,
        2,
    ),
)
my_data = Record0(
    outer=record_data,
)
