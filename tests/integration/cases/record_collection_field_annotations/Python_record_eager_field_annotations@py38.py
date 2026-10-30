import dataclasses
from typing import Any, Dict, Set, Tuple
@dataclasses.dataclass(frozen=True)
class Record1:
    value: int
@dataclasses.dataclass(frozen=True)
class Record0:
    items: Tuple[int, ...]
    empty_items: Tuple[Any, ...]
    values: Set[int]
    mapping: Dict[int, int]
    empty_mapping: Dict[str, Any]
    records: Tuple[Record1, ...]
my_data = Record0(
    items=(
        1,
        2,
    ),
    empty_items=(),
    values={
        1,
        2,
    },
    mapping={
        1: 2,
        3: 4,
    },
    empty_mapping={},
    records=(
        Record1(
            value=1,
        ),
        Record1(
            value=2,
        ),
    ),
)
