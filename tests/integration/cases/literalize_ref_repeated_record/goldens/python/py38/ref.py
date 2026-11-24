from __future__ import annotations
import dataclasses
@dataclasses.dataclass(frozen=True)
class Record0:
    value: tuple[int, ...]
shared = Record0(
    value=(
        1,
        2,
    ),
)
my_data = (
    shared,
    shared,
)
