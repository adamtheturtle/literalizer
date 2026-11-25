from __future__ import annotations
import dataclasses
@dataclasses.dataclass(frozen=True)
class Record0:
    numbers: tuple[int, ...]
    nested_numbers: tuple[tuple[int, ...], ...]
    words: tuple[str, ...]
    flag: bool
my_data: Record0 = Record0(
    numbers=(
        1,
        2,
    ),
    nested_numbers=(
        (
            3,
            4,
        ),
        (
            5,
            6,
        ),
    ),
    words=(
        "s",
    ),
    flag=True,
)
