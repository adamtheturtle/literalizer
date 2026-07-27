from __future__ import annotations
from collections import OrderedDict
from typing import Any, Union
my_data: dict[str, Union[OrderedDict[str, Any], int]] = {
    "a": OrderedDict([]),
    "b": 1,
}
my_data = {
    "a": OrderedDict([]),
    "b": 1,
}
