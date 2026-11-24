from __future__ import annotations
import dataclasses
@dataclasses.dataclass(frozen=True)
class Record0:
    within_i32: int
    beyond_i32: int
my_data = Record0(
    within_i32=1705320000,
    beyond_i32=4085195400,
)
