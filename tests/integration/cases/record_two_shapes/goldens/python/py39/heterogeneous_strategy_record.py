from __future__ import annotations
import dataclasses
@dataclasses.dataclass(frozen=True)
class Record1:
    count: int
    rate: int
@dataclasses.dataclass(frozen=True)
class Record2:
    retries: int
    timeout: int
@dataclasses.dataclass(frozen=True)
class Record0:
    metrics: Record1
    flags: Record2
my_data = Record0(
    metrics=Record1(
        count=100,
        rate=50,
    ),
    flags=Record2(
        retries=3,
        timeout=30,
    ),
)
