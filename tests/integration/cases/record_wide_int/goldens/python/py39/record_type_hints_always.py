from __future__ import annotations
import dataclasses
@dataclasses.dataclass(frozen=True)
class Record0:
    quantity: int
    big: int
    ratio: float
    label: str
    ok: bool
my_data: Record0 = Record0(
    quantity=1000000,
    big=18446744073709551615,
    ratio=2.5,
    label="tag",
    ok=True,
)
