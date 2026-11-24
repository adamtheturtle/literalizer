from __future__ import annotations
from collections import OrderedDict
from typing import Any
import dataclasses
@dataclasses.dataclass(frozen=True)
class Record0:
    numbers: OrderedDict[str, int]
    words: OrderedDict[str, str]
    nested: OrderedDict[str, tuple[int, ...]]
    empty: OrderedDict[str, Any]
    flag: bool
    nested_maps: OrderedDict[str, OrderedDict[str, int]]
    empty_nested_maps: OrderedDict[str, OrderedDict[str, Any]]
my_data = Record0(
    numbers=OrderedDict([
        ("first", 1),
    ]),
    words=OrderedDict([
        ("first", "s"),
    ]),
    nested=OrderedDict([
        ("first", (
            1,
            2,
        )),
    ]),
    empty=OrderedDict([]),
    flag=True,
    nested_maps=OrderedDict([
        ("first", OrderedDict([
            ("nested", 1),
        ])),
    ]),
    empty_nested_maps=OrderedDict([
        ("first", OrderedDict([])),
    ]),
)
