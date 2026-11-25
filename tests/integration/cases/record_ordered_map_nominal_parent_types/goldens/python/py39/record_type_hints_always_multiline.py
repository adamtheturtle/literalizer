from __future__ import annotations
from collections import OrderedDict
import dataclasses
@dataclasses.dataclass(frozen=True)
class Record2:
    x: int
@dataclasses.dataclass(frozen=True)
class Record1:
    values: OrderedDict[str, Record2]
    flag: bool
@dataclasses.dataclass(frozen=True)
class Record4:
    y: str
@dataclasses.dataclass(frozen=True)
class Record3:
    values: OrderedDict[str, Record4]
    flag: bool
@dataclasses.dataclass(frozen=True)
class Record0:
    first: Record1
    second: Record3
my_data: Record0 = Record0(
    first=Record1(
        values=OrderedDict([
            ("item", Record2(
                x=1,
            )),
        ]),
        flag=True,
    ),
    second=Record3(
        values=OrderedDict([
            ("item", Record4(
                y="s",
            )),
        ]),
        flag=False,
    ),
)
