from __future__ import annotations
import dataclasses
@dataclasses.dataclass(frozen=True)
class Record0:
    name: str
    scores: tuple[int, ...]
my_data = Record0(
    name="Alice",
    scores=(
        10,
        20,
        30,
    ),
)
