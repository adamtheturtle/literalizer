from __future__ import annotations
import dataclasses
@dataclasses.dataclass(frozen=True)
class Record0:
    field: int
value = Record0(
    field=2,
)
my_data = (
    Record0(field=1),
    value,
)
