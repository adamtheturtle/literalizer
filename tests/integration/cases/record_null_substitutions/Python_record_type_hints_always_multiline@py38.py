from __future__ import annotations
from collections import OrderedDict
import dataclasses
@dataclasses.dataclass(frozen=True)
class Record0:
    replacement: int
    present: int
my_data: OrderedDict[str, tuple[Record0, ...]] = OrderedDict([
    ("rows", (
        Record0(
            replacement=-1,
            present=1,
        ),
        Record0(
            replacement=2,
            present=3,
        ),
    )),
])
