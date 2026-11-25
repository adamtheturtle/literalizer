import dataclasses
from typing import Any
@dataclasses.dataclass(frozen=True)
class Record1:
    value: int
@dataclasses.dataclass(frozen=True)
class Record0:
    items: list[int]
    empty_items: list[Any]
    values: frozenset[int]
    mapping: dict[int, int]
    empty_mapping: dict[str, Any]
    records: list[Record1]
my_data = Record0(
    items=[
        1,
        2,
    ],
    empty_items=[],
    values=frozenset({
        1,
        2,
    }),
    mapping={
        1: 2,
        3: 4,
    },
    empty_mapping={},
    records=[
        Record1(
            value=1,
        ),
        Record1(
            value=2,
        ),
    ],
)
