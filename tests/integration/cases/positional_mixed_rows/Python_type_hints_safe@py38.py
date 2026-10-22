from __future__ import annotations
from typing import Any
my_data: tuple[tuple[tuple[int | str, ...] | tuple[int, ...] | tuple[Any, ...], ...] | tuple[tuple[Any, ...] | tuple[int, ...], ...], ...] = (
    ((1, "value"), (1, 2), ()),
    ((), (), (3, 4)),
)
