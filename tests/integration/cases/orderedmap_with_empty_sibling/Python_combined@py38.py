from __future__ import annotations
from collections import OrderedDict
from typing import Any, Tuple, Union
my_data: Tuple[Union[Tuple[Any, ...], OrderedDict[str, int]], ...] = (
    OrderedDict([("a", 1)]),
    (),
)
my_data = (
    OrderedDict([("a", 1)]),
    (),
)
