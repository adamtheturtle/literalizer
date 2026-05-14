from __future__ import annotations
from collections import OrderedDict
from typing import Any, Dict, Union
my_data: Dict[str, Union[OrderedDict[str, Any], int]] = {
    "a": OrderedDict([]),
    "b": 1,
}
