from collections import OrderedDict
import dataclasses
from typing import OrderedDict as TypingOrderedDict, Tuple
@dataclasses.dataclass(frozen=True)
class Record1:
    x: int
@dataclasses.dataclass(frozen=True)
class Record0:
    values: TypingOrderedDict[str, Tuple[TypingOrderedDict[str, Record1], ...]]
    flag: bool
my_data = Record0(
    values=OrderedDict([
        ("entries", (
            OrderedDict([
                ("inner", Record1(
                    x=1,
                )),
            ]),
            OrderedDict([
                ("inner", Record1(
                    x=2,
                )),
            ]),
        )),
    ]),
    flag=True,
)
