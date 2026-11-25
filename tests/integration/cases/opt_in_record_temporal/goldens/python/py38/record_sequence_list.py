from __future__ import annotations
import datetime
import dataclasses
@dataclasses.dataclass(frozen=True)
class Record0:
    event_date: datetime.date
    event_time: datetime.time
    event_datetime: datetime.datetime
my_data = Record0(
    event_date=datetime.date(year=2024, month=1, day=15),
    event_time=datetime.time(hour=12, minute=30, second=0),
    event_datetime=datetime.datetime(year=2024, month=1, day=15, hour=12, minute=30, second=0, tzinfo=datetime.timezone.utc),
)
