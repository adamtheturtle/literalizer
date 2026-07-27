from __future__ import annotations
from collections import OrderedDict
from typing import Any, Tuple
my_data: Tuple[Tuple[Any, ...] | OrderedDict[str, int], ...] = (
    OrderedDict([("a", 1)]),
    (),
)
my_data = (
    OrderedDict([("a", 1)]),
    (),
)
