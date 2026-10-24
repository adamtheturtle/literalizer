from __future__ import annotations
import datetime
import dataclasses
@dataclasses.dataclass(frozen=True)
class Record1:
    integer: int
    boolean: bool
    decimal: float
    null: None
@dataclasses.dataclass(frozen=True)
class Record3:
    integer: int
@dataclasses.dataclass(frozen=True)
class Record2:
    child: Record3
@dataclasses.dataclass(frozen=True)
class Record4:
    text: str
@dataclasses.dataclass(frozen=True)
class Record5:
    day: datetime.date
    stamp: datetime.datetime
@dataclasses.dataclass(frozen=True)
class Record0:
    trivial: Record1
    nested: Record2
    owning: Record4
    calendar: Record5
trivial = Record1(
    integer=1,
    boolean=True,
    decimal=1.5,
    null=None,
)
nested = Record2(
    child=Record3(
        integer=2,
    ),
)
owning = Record4(
    text="owned",
)
calendar = Record5(
    day=datetime.date(year=2001, month=1, day=2),
    stamp=datetime.datetime(year=2001, month=1, day=2, hour=3, minute=4, second=5, tzinfo=datetime.UTC),
)
my_data = Record0(
    trivial=trivial,
    nested=nested,
    owning=owning,
    calendar=calendar,
)
