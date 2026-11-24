from __future__ import annotations
from typing import Any
seed = 1
my_data: tuple[tuple[Any, ...] | tuple[tuple[Any, ...], ...] | int, ...] = (
    (),
    ((),),
    seed,
)
