from __future__ import annotations
from collections import OrderedDict
import dataclasses
@dataclasses.dataclass(frozen=True)
class Record0:
    id: int
my_data = OrderedDict([
    ("first", (Record0(id=1),)),
    ("second", 2),
])
