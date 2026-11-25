from __future__ import annotations
import datetime
import dataclasses
@dataclasses.dataclass(frozen=True)
class Record0:
    vals: tuple[datetime.time | str, ...]
my_data = Record0(
    vals=(
        datetime.time(hour=9, minute=30, second=0),
        "hello",
    ),
)
