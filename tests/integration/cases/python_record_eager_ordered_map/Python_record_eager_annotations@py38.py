from collections import OrderedDict
from typing import OrderedDict as TypingOrderedDict
import dataclasses
from typing import Union
@dataclasses.dataclass(frozen=True)
class Record0:
    x: int
@dataclasses.dataclass(frozen=True)
class Record1:
    y: int
my_data: TypingOrderedDict[str, Union[Record0, Record1]] = OrderedDict([
    ("first", Record0(x=1)),
    ("second", Record1(y=2)),
])
