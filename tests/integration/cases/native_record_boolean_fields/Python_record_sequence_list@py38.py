from __future__ import annotations
import dataclasses
@dataclasses.dataclass(frozen=True)
class Record0:
    active: bool
my_data = [
    Record0(active=True),
    Record0(active=False),
]
