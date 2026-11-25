from __future__ import annotations
from typing import Any
my_data: dict[str, tuple[int | tuple[Any, ...], ...] | tuple[int | tuple[str, ...], ...]] = {
    "lint": (2, ()),
    "test": (5, ("compile",)),
}
