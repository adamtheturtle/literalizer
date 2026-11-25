from __future__ import annotations
import dataclasses
@dataclasses.dataclass(frozen=True)
class Record0:
    flags: tuple[bool, ...]
    values: tuple[float, ...]
    ints: tuple[int, ...]
    text: tuple[str, ...]
    nested_flags: tuple[tuple[bool, ...], ...]
    nested_values: tuple[tuple[float, ...], ...]
my_data: Record0 = Record0(
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
