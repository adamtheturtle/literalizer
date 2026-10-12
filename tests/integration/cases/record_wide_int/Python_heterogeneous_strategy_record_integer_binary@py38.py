from __future__ import annotations
import dataclasses
@dataclasses.dataclass(frozen=True)
class Record0:
    quantity: int
    big: int
    ratio: float
    label: str
    ok: bool
my_data = Record0(
    quantity=0b11110100001001000000,
    big=0b1111111111111111111111111111111111111111111111111111111111111111,
    ratio=2.5,
    label="tag",
    ok=True,
)
