from __future__ import annotations
import dataclasses
@dataclasses.dataclass(frozen=True)
class Record0:
    number: int
my_data: Record0 = Record0(
    number=1,
)
