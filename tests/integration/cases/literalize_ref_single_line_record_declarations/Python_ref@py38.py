from __future__ import annotations
import dataclasses
@dataclasses.dataclass(frozen=True)
class Record1:
    x: str
@dataclasses.dataclass(frozen=True)
class Record2:
    x: int
@dataclasses.dataclass(frozen=True)
class Record0:
    direct: Record1
    bound: Record2
first = Record2(
    x=1,
)
my_data = Record0(
    direct=Record1(
        x="s",
    ),
    bound=first,
)
