from __future__ import annotations
from typing import Any
my_data: tuple[tuple[int | tuple[Any, ...], ...] | tuple[int | tuple[int, ...], ...], ...] = (
    (1, ()),
    (2, (3,)),
)
