from collections import OrderedDict
import dataclasses
@dataclasses.dataclass(frozen=True)
class Record0:
    x: int
my_data = OrderedDict([
    ("outer", (OrderedDict([("inner", Record0(x=1))]), OrderedDict([("inner", Record0(x=2))]))),
])
