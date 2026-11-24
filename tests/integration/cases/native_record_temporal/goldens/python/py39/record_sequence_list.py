from __future__ import annotations
import datetime
import dataclasses
@dataclasses.dataclass(frozen=True)
class Record0:
    birthday: datetime.date
    meeting: datetime.time
    event_time: datetime.datetime
my_data = Record0(
    birthday=datetime.date(year=2024, month=1, day=15),
    meeting=datetime.time(hour=9, minute=30, second=0),
    event_time=datetime.datetime(year=2024, month=1, day=15, hour=12, minute=30, second=0, tzinfo=datetime.UTC),
)
