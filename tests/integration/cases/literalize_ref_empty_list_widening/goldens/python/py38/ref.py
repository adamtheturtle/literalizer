from __future__ import annotations
from typing import Any
empty_values: tuple[Any, ...] = ()
integer_values = (
    1,
)
my_data: tuple[tuple[Any, ...] | tuple[int, ...], ...] = (
    empty_values,
    integer_values,
)
