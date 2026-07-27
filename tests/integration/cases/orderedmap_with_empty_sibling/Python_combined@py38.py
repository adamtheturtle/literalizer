from __future__ import annotations
from collections import OrderedDict
from typing import Any, Union
my_data: tuple[Union[tuple[Any, ...], OrderedDict[str, int]], ...] = (
    OrderedDict([("a", 1)]),
    (),
)
my_data = (
    OrderedDict([("a", 1)]),
    (),
)
