from __future__ import annotations
from typing import Any
my_data: dict[str, tuple[dict[str, int], ...] | tuple[tuple[Any, ...] | tuple[int, ...], ...]] = {
    "a": ({}, {"x": 1}),
    "b": ((), (1,)),
}
