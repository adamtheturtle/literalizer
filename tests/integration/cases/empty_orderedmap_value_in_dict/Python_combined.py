from collections import OrderedDict
from typing import Any
my_data: dict[str, OrderedDict[str, Any] | int] = {
    "a": OrderedDict([]),
    "b": 1,
}
my_data = {
    "a": OrderedDict([]),
    "b": 1,
}
