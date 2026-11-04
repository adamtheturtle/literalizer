import datetime
import dataclasses
@dataclasses.dataclass(frozen=True)
class Record0:
    birthday: datetime.date
    moment: datetime.datetime
    at: datetime.time
my_data = Record0(
    birthday=datetime.date(year=2024, month=1, day=15),
    moment=datetime.datetime(year=2024, month=1, day=15, hour=12, minute=30, second=0, tzinfo=datetime.UTC),
    at=datetime.time(hour=9, minute=30, second=0),
)
