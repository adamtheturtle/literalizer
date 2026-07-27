from __future__ import annotations
from typing import Any, Union
my_data: dict[str, Union[tuple[Union[int, tuple[Any, ...]], ...], tuple[Union[int, tuple[str, ...]], ...]]] = {
    "lint": (2, ()),
    "test": (5, ("compile",)),
}
my_data = {
    "lint": (2, ()),
    "test": (5, ("compile",)),
}
