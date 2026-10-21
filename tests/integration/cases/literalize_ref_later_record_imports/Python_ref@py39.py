from __future__ import annotations
import datetime
import dataclasses
@dataclasses.dataclass(frozen=True)
class Record1:
    x: int
@dataclasses.dataclass(frozen=True)
class Record2:
    day: datetime.date
    stamp: datetime.datetime
@dataclasses.dataclass(frozen=True)
class Record0:
    plain: Record1
    timed: Record2
plain = Record1(
    x=1,
)
timed = Record2(
    day=datetime.date(year=2001, month=1, day=2),
    stamp=datetime.datetime(year=2001, month=1, day=2, hour=3, minute=4, second=5, tzinfo=datetime.UTC),
)
my_data = Record0(
    plain=plain,
    timed=timed,
)
