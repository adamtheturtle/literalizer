from __future__ import annotations
from collections import OrderedDict
import dataclasses
@dataclasses.dataclass(frozen=True)
class Record1:
    numbers: tuple[int, ...]
    strings: tuple[str, ...]
@dataclasses.dataclass(frozen=True)
class Record0:
    omap_value: OrderedDict[str, int]
    sibling_lists: Record1
    ref_marker_present: tuple[str, ...]
my_data = Record0(
    omap_value=OrderedDict([
        ("first", 1),
    ]),
    sibling_lists=Record1(
        numbers=(
            1,
            2,
        ),
        strings=(
            "x",
            "y",
        ),
    ),
    ref_marker_present=(
        "$keep",
        "z",
    ),
)
