from __future__ import annotations
import dataclasses
@dataclasses.dataclass(frozen=True)
class Record0:
    a: int
my_data: tuple[tuple[Record0, ...], ...] = (
    (Record0(a=1),),
    (Record0(a=2),),
)
