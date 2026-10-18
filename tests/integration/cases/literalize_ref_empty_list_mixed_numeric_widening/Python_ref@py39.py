from __future__ import annotations
from typing import Any
empty_values: tuple[Any, ...] = ()
integer_values = (
    1,
)
float_values = (
    1.5,
)
my_data: tuple[tuple[Any, ...] | tuple[int, ...] | tuple[float, ...], ...] = (
    empty_values,
    integer_values,
    float_values,
)
