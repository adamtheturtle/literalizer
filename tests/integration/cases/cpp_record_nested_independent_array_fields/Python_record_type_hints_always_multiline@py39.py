from __future__ import annotations
import dataclasses
@dataclasses.dataclass(frozen=True)
class Record0:
    numbers: tuple[tuple[int, ...], ...]
    words: tuple[tuple[str, ...], ...]
my_data: Record0 = Record0(
    numbers=(
        (
            1,
        ),
        (
            2,
        ),
    ),
    words=(
        (
            "s",
        ),
        (
            "t",
        ),
    ),
)
