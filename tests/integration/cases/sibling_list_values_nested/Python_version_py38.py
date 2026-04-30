from __future__ import annotations
from typing import Any, Dict, Tuple, Union
my_data: Dict[str, Union[Tuple[Union[int, Tuple[Any, ...]], ...], Tuple[Union[int, Tuple[str, ...]], ...]]] = {
    "lint": (2, ()),
    "test": (5, ("compile",)),
}
