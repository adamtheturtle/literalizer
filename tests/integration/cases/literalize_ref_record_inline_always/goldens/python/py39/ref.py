from __future__ import annotations
import dataclasses
@dataclasses.dataclass(frozen=True)
class Record0:
    x: int
    y: None
my_data: Record0 = Record0(
    x=1,
    y=None,
)
