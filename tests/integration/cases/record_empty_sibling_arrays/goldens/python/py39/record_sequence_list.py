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
    integers: list[list[Any] | list[Record1]]
    nulls: list[list[Any] | list[Record2]]
    nested: list[list[list[Any] | list[Record1]] | list[list[Record1] | list[Any]]]
    reversed: list[list[Record1] | list[Any]]
my_data = Record0(
    integers=[
        [],
        [
            Record1(
                item=1,
            ),
        ],
    ],
    nulls=[
        [],
        [
            Record2(
                item=None,
            ),
        ],
    ],
    nested=[
        [
            [],
            [
                Record1(
                    item=2,
                ),
            ],
        ],
        [
            [
                Record1(
                    item=3,
                ),
            ],
            [],
        ],
    ],
    reversed=[
        [
            Record1(
                item=4,
            ),
        ],
        [],
    ],
)
