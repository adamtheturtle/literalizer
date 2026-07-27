from __future__ import annotations
from collections import OrderedDict
from typing import Any, Union
my_data: OrderedDict[str, Union[tuple[Any, ...], int]] = OrderedDict([
    ("a", ()),
    ("b", 1),
])
