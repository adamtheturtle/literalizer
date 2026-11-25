from __future__ import annotations
import dataclasses
@dataclasses.dataclass(frozen=True)
class Record2:
    value: int
@dataclasses.dataclass(frozen=True)
class Record1:
    items: tuple[int | Record2, ...]
@dataclasses.dataclass(frozen=True)
class Record4:
    value: str
@dataclasses.dataclass(frozen=True)
class Record3:
    items: tuple[int | Record4, ...]
@dataclasses.dataclass(frozen=True)
class Record0:
    first: Record1
    second: Record3
my_data: Record0 = Record0(
    first=Record1(
        items=(
            1,
            Record2(
                value=2,
            ),
        ),
    ),
    second=Record3(
        items=(
            1,
            Record4(
                value="s",
            ),
        ),
    ),
)
