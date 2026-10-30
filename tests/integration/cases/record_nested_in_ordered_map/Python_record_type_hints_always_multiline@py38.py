from __future__ import annotations
from collections import OrderedDict
import dataclasses
@dataclasses.dataclass(frozen=True)
class Record0:
    name: None
    id: int
my_data: OrderedDict[str, tuple[Record0, ...]] = OrderedDict([
    ("outer", (
        Record0(
            name=None,
            id=1,
        ),
    )),
])
