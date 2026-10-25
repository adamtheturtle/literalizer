from __future__ import annotations
import dataclasses
@dataclasses.dataclass(frozen=True)
class Record0:
    short: tuple[int, ...]
    long: tuple[int, ...]
my_data: Record0 = Record0(
    short=(
        1,
    ),
    long=(
        1,
        2,
    ),
)
