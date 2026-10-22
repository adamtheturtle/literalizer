from __future__ import annotations
from typing import Any
my_data: tuple[tuple[Any, ...] | tuple[int, ...] | tuple[int | str | bool | None, ...], ...] = (
    (),
    (1,),
    (1, 2),
    (1, "x", True, None),
    (1, 2, 3, 4, 5, 6, 7, 8),
)
