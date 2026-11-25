from __future__ import annotations
from collections import OrderedDict
my_data: OrderedDict[str, dict[str, int] | int] = OrderedDict([
    ("__proto__", {"x": 1}),
    ("ordinary", 2),
])
