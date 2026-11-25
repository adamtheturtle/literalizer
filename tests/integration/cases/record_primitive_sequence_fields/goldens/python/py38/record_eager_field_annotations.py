import dataclasses
from typing import Tuple
@dataclasses.dataclass(frozen=True)
class Record0:
    flags: Tuple[bool, ...]
    values: Tuple[float, ...]
    ints: Tuple[int, ...]
    text: Tuple[str, ...]
    nested_flags: Tuple[Tuple[bool, ...], ...]
    nested_values: Tuple[Tuple[float, ...], ...]
my_data = Record0(
    flags=(
        True,
        False,
    ),
    values=(
        1.5,
        -2.25,
    ),
    ints=(
        1,
        2,
    ),
    text=(
        "a",
    ),
    nested_flags=(
        (
            True,
        ),
        (
            False,
        ),
    ),
    nested_values=(
        (
            1.5,
        ),
        (
            2.25,
        ),
    ),
)
