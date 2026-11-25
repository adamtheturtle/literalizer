from __future__ import annotations
from typing import Any
my_data: tuple[tuple[int | tuple[int, ...], ...] | tuple[int | tuple[Any, ...], ...], ...] = (
    (1, (3,)),
    (2, ()),
)
