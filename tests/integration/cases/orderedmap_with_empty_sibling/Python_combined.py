from collections import OrderedDict
from typing import Any
my_data: tuple[tuple[Any, ...] | OrderedDict[str, int], ...] = (
    OrderedDict([("a", 1)]),
    (),
)
my_data = (
    OrderedDict([("a", 1)]),
    (),
)
