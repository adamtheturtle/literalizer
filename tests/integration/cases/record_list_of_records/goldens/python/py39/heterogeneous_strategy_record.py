from __future__ import annotations
import dataclasses
@dataclasses.dataclass(frozen=True)
class Record1:
    id: int
    label: str
@dataclasses.dataclass(frozen=True)
class Record0:
    name: str
    items: tuple[Record1, ...]
my_data = Record0(
    name="box",
    items=(
        Record1(
            id=1,
            label="first",
        ),
        Record1(
            id=2,
            label="second",
        ),
    ),
)
