from __future__ import annotations
from collections import OrderedDict
import dataclasses
@dataclasses.dataclass(frozen=True)
class Record0:
    id: int
my_data: OrderedDict[str, tuple[Record0, ...] | int] = OrderedDict([
    ("first", (
        Record0(
            id=1,
        ),
    )),
    ("second", 2),
])
