from __future__ import annotations
from typing import Any, Set, Tuple
my_data: Tuple[Set[Any] | Set[int] | Tuple[Any, ...], ...] = (
    set(),
    {1, 2},
    (),
)
