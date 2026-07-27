from __future__ import annotations
from typing import Any, Tuple
my_data: Tuple[Tuple[int, ...] | Tuple[Any, ...] | Tuple[str, ...], ...] = (
    (1, 2),
    (),
    ("a", "b"),
)
