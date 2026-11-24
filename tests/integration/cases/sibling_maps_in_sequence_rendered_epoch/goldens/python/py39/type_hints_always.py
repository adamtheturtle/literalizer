from __future__ import annotations
import datetime
my_data: tuple[dict[str, datetime.datetime | int], ...] = (
    {"k": datetime.datetime(year=2040, month=1, day=1, hour=0, minute=0, second=0, tzinfo=datetime.UTC)},
    {"k": 1},
)
