from __future__ import annotations
import dataclasses
@dataclasses.dataclass(frozen=True)
class Record0:
    narrow_pair: list[int]
    wide_pair: list[int]
    wide_triple: list[int]
    beyond_pair: list[int]
    beyond_triple: list[int]
    mixed_triple: list[int | str | bool]
my_data = Record0(
    narrow_pair=[
        1,
        2,
    ],
    wide_pair=[
        1,
        1099511627776,
    ],
    wide_triple=[
        1,
        2,
        1099511627776,
    ],
    beyond_pair=[
        1,
        18446744073709551616,
    ],
    beyond_triple=[
        1,
        2,
        18446744073709551616,
    ],
    mixed_triple=[
        1,
        "text",
        True,
    ],
)
