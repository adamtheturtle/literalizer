from __future__ import annotations
import dataclasses
@dataclasses.dataclass(frozen=True)
class Record0:
    flags: list[bool]
    values: list[float]
    ints: list[int]
    text: list[str]
    nested_flags: list[list[bool]]
    nested_values: list[list[float]]
my_data = Record0(
    flags=[
        True,
        False,
    ],
    values=[
        1.5,
        -2.25,
    ],
    ints=[
        1,
        2,
    ],
    text=[
        "a",
    ],
    nested_flags=[
        [
            True,
        ],
        [
            False,
        ],
    ],
    nested_values=[
        [
            1.5,
        ],
        [
            2.25,
        ],
    ],
)
