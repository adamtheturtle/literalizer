from __future__ import annotations
from collections import OrderedDict
import dataclasses
@dataclasses.dataclass(frozen=True)
class Record0:
    values: OrderedDict[str, int]
    flag: bool
    nested_values: OrderedDict[str, OrderedDict[str, int]]
    list_values: OrderedDict[str, tuple[int, ...]]
my_data = Record0(
    values=OrderedDict([
        ("first", 2208988800),
    ]),
    flag=True,
    nested_values=OrderedDict([
        ("first", OrderedDict([
            ("nested", 2208988800),
        ])),
    ]),
    list_values=OrderedDict([
        ("first", (
            2208988800,
        )),
    ]),
)
