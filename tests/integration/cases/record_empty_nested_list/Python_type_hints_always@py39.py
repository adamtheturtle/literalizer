from __future__ import annotations
from typing import Any
my_data: dict[str, tuple[tuple[int, ...], ...] | tuple[tuple[Any, ...] | tuple[int, ...], ...]] = {
    "a": ((1, 2), (3,)),
    "b": ((), (1,)),
}
