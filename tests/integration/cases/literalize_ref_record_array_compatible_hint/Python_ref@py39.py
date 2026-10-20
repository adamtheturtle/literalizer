from __future__ import annotations
import dataclasses
@dataclasses.dataclass(frozen=True)
class Record0:
    items: tuple[int, ...]
record_data = (
    Record0(items=(1, 2)),
)
my_data = record_data
