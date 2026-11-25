from __future__ import annotations
import dataclasses
@dataclasses.dataclass(frozen=True)
class Record0:
    payload: str
my_data: Record0 = Record0(
    payload="48656c6c6f",
)
