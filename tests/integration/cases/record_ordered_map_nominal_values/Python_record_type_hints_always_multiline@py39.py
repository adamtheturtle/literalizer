from __future__ import annotations
from collections import OrderedDict
import dataclasses
@dataclasses.dataclass(frozen=True)
class Record1:
    x: int
@dataclasses.dataclass(frozen=True)
class Record0:
    values: OrderedDict[str, Record1]
    flag: bool
my_data: Record0 = Record0(
    values=OrderedDict([
        ("first", Record1(
            x=1,
        )),
        ("second", Record1(
            x=2,
        )),
    ]),
    flag=True,
)
