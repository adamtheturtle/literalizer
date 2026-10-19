from __future__ import annotations
import dataclasses
@dataclasses.dataclass(frozen=True)
class Record1:
    value: int
@dataclasses.dataclass(frozen=True)
class Record0:
    child: Record1
first = Record0(
    child=Record1(
        value=1,
    ),
)
my_data = first
