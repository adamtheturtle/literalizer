from __future__ import annotations
import dataclasses
@dataclasses.dataclass(frozen=True)
class Record0:
    x: int
first = (
    Record0(x=1),
    Record0(x=2),
)
my_data = first
