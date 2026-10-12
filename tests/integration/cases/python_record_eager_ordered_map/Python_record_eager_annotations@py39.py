from collections import OrderedDict
import dataclasses
from typing import Union
@dataclasses.dataclass(frozen=True)
class Record0:
    x: int
@dataclasses.dataclass(frozen=True)
class Record1:
    y: int
my_data: OrderedDict[str, Union[Record0, Record1]] = OrderedDict([
    ("first", Record0(x=1)),
    ("second", Record1(y=2)),
])
