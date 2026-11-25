from __future__ import annotations
import dataclasses
@dataclasses.dataclass(frozen=True)
class Record0:
    a: int
my_data = (
    Record0(a=1),
    2,
)
