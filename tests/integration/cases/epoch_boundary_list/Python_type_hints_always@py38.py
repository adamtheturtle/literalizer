from __future__ import annotations
import datetime
my_data: tuple[datetime.datetime, ...] = (
    datetime.datetime(year=1901, month=12, day=13, hour=20, minute=45, second=51),
    datetime.datetime(year=1901, month=12, day=13, hour=20, minute=45, second=52),
    datetime.datetime(year=2038, month=1, day=19, hour=3, minute=14, second=7),
    datetime.datetime(year=2038, month=1, day=19, hour=3, minute=14, second=8),
)
