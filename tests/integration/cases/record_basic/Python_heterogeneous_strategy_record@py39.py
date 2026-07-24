from __future__ import annotations
import dataclasses
@dataclasses.dataclass(frozen=True)
class Record0:
    id: int
    label: str
    enabled: bool
    related_ids: tuple[int, ...]
my_data = Record0(
    id=1,
    label="She said \"hello\", then waved",
    enabled=False,
    related_ids=(
        1,
        2,
        3,
    ),
)
