from __future__ import annotations
from collections import OrderedDict
import dataclasses
@dataclasses.dataclass(frozen=True)
class Record0:
    x: int
my_data: tuple[OrderedDict[str, Record0], ...] = (
    OrderedDict([
        ("first", Record0(
            x=1,
        )),
    ]),
    OrderedDict([
        ("first", Record0(
            x=2,
        )),
    ]),
)
