from __future__ import annotations
import dataclasses
@dataclasses.dataclass(frozen=True)
class Record1:
    k: tuple[bool, ...]
@dataclasses.dataclass(frozen=True)
class Record0:
    h: tuple[int | str | tuple[int | str, ...] | dict[str, tuple[bool, ...]], ...]
my_data = Record0(
    h=(
        1,
        "a",
        (
            2,
            "b",
        ),
        Record1(
            k=(
                True,
            ),
        ),
    ),
)
