import dataclasses
from typing import Any, Dict, FrozenSet, List
@dataclasses.dataclass(frozen=True)
class Record1:
    value: int
@dataclasses.dataclass(frozen=True)
class Record0:
    items: List[int]
    empty_items: List[Any]
    values: FrozenSet[int]
    mapping: Dict[int, int]
    empty_mapping: Dict[str, Any]
    records: List[Record1]
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
