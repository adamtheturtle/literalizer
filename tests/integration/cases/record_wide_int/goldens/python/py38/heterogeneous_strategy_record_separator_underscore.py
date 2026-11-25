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
    quantity=1_000_000,
    big=18_446_744_073_709_551_615,
    ratio=2.5,
    label="tag",
    ok=True,
)
