from collections import OrderedDict
from typing import Any
my_data: OrderedDict[str, tuple[Any, ...] | int] = OrderedDict([
    ("a", ()),
    ("b", 1),
])
my_data = OrderedDict([
    ("a", ()),
    ("b", 1),
])
