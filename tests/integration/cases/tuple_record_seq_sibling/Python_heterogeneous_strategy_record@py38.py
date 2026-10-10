from __future__ import annotations
import dataclasses
@dataclasses.dataclass(frozen=True)
class Record0:
    scores: tuple[int, ...]
    args: tuple[int | str, ...]
my_data = Record0(
    scores=(
        10,
        20,
        30,
    ),
    args=(
        1,
        "email",
        "a@gmail.com",
        100,
    ),
)
