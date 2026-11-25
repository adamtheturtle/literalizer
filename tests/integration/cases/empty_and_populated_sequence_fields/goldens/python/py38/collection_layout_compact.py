from __future__ import annotations
from typing import Any
my_data: tuple[dict[str, tuple[Any, ...] | tuple[int, ...]], ...] = (
    {"value": ()},
    {"value": (1,)},
)
my_data = (
    {"value": ()},
    {"value": (1,)},
)
