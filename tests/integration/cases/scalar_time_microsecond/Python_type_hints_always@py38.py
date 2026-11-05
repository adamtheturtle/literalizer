from __future__ import annotations
import datetime
my_data: dict[str, datetime.time] = {
    "exact_millisecond": datetime.time(hour=9, minute=30, second=15, microsecond=123000),
    "sub_millisecond": datetime.time(hour=9, minute=30, second=15, microsecond=123456),
}
