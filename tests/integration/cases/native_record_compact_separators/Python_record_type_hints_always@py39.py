from __future__ import annotations
import dataclasses
@dataclasses.dataclass(frozen=True)
class Record0:
    name: str
    active: bool
my_data: tuple[Record0, ...] = (
    Record0(name="Ada", active=True),
)
