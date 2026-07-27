from __future__ import annotations
from collections import OrderedDict
from typing import Any, Tuple
my_data: OrderedDict[str, Tuple[Any, ...] | int] = OrderedDict([
    ("a", ()),
    ("b", 1),
])
