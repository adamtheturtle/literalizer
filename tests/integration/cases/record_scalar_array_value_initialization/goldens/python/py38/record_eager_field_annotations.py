import dataclasses
from typing import Tuple
@dataclasses.dataclass(frozen=True)
class Record0:
    numbers: Tuple[int, ...]
    nested_numbers: Tuple[Tuple[int, ...], ...]
    words: Tuple[str, ...]
    flag: bool
my_data = Record0(
    numbers=(
        1,
        2,
    ),
    nested_numbers=(
        (
            3,
            4,
        ),
        (
            5,
            6,
        ),
    ),
    words=(
        "s",
    ),
    flag=True,
)
