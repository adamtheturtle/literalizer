from __future__ import annotations
import datetime
import dataclasses
from typing import Union
@dataclasses.dataclass(frozen=True)
class Record0:
    vals: tuple[Union[datetime.time, str], ...]
my_data = Record0(
    vals=(
        datetime.time(hour=9, minute=30, second=0),
        "hello",
    ),
)
