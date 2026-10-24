from __future__ import annotations
from typing import Any
my_data: tuple[tuple[Any, ...] | tuple[int | str, ...] | tuple[int, ...], ...] = (
    (),
    (1, "value"),
    (2, 3),
)
