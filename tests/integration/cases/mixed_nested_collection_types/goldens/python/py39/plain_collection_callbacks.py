from __future__ import annotations
from typing import Any
my_data: dict[str, tuple[tuple[int, ...] | tuple[str, ...] | tuple[Any, ...], ...] | tuple[dict[str, int | str], ...] | dict[str, tuple[int, ...] | tuple[Any, ...]]] = {
    "lists": ((1,), ("x",), ()),
    "maps": ({"x": 1}, {"x": "s"}),
    "empties": {"a": (1,), "b": ()},
}
