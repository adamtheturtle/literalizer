from __future__ import annotations
from collections import OrderedDict
from typing import Any
my_data: OrderedDict[str, tuple[Any, ...] | int] = OrderedDict([
    ("a", ()),
    ("b", 1),
])
