from __future__ import annotations
from typing import Any
import dataclasses
@dataclasses.dataclass(frozen=True)
class Record0:
    pair: tuple[int, ...]
    mixed: tuple[int | str, ...]
    triple: tuple[int | str | bool, ...]
    nested: tuple[tuple[int | str, ...] | tuple[int | bool | float, ...], ...]
    empty: tuple[Any, ...]
    single: tuple[int, ...]
    long: tuple[int, ...]
my_data = Record0(
    pair=(
        1,
        2,
    ),
    mixed=(
        1,
        "text",
    ),
    triple=(
        1,
        "text",
        True,
    ),
    nested=(
        (
            1,
            "text",
        ),
        (
            2,
            False,
            3.5,
        ),
    ),
    empty=(),
    single=(
        1,
    ),
    long=(
        1,
        2,
        3,
        4,
    ),
)
