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
    quantity=0o3641100,
    big=0o1777777777777777777777,
    ratio=2.5,
    label="tag",
    ok=True,
)
