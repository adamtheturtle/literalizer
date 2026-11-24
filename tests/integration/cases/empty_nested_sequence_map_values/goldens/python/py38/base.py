from __future__ import annotations
from typing import Any
my_data: dict[str, tuple[int | tuple[Any, ...], ...] | tuple[int | tuple[str, ...], ...]] = {
    "alpha": (2, ()),
    "beta": (5, ("x",)),
}
