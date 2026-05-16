from __future__ import annotations
import dataclasses
@dataclasses.dataclass(frozen=True)
class Record0:
    id: int
    description: str
    is_done: bool
    blocks: tuple[int, ...]
my_data = Record0(
    id=1,
    description="She said \"hello\", then waved",
    is_done=False,
    blocks=(
        1,
        2,
        3,
    ),
)
