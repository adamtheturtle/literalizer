from __future__ import annotations
from typing import Any
import dataclasses
@dataclasses.dataclass(frozen=True)
class Record1:
    item: int
@dataclasses.dataclass(frozen=True)
class Record2:
    item: None
@dataclasses.dataclass(frozen=True)
class Record0:
    integers: tuple[tuple[Any, ...] | tuple[Record1, ...], ...]
    nulls: tuple[tuple[Any, ...] | tuple[Record2, ...], ...]
    nested: tuple[tuple[tuple[Any, ...] | tuple[Record1, ...], ...] | tuple[tuple[Record1, ...] | tuple[Any, ...], ...], ...]
    reversed: tuple[tuple[Record1, ...] | tuple[Any, ...], ...]
my_data = Record0(
    integers=(
        (),
        (
            Record1(
                item=1,
            ),
        ),
    ),
    nulls=(
        (),
        (
            Record2(
                item=None,
            ),
        ),
    ),
    nested=(
        (
            (),
            (
                Record1(
                    item=2,
                ),
            ),
        ),
        (
            (
                Record1(
                    item=3,
                ),
            ),
            (),
        ),
    ),
    reversed=(
        (
            Record1(
                item=4,
            ),
        ),
        (),
    ),
)
