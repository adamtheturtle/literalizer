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
    quantity=0xf4240,
    big=0xffffffffffffffff,
    ratio=2.5,
    label="tag",
    ok=True,
)
