from __future__ import annotations
import datetime
my_data: dict[str, dict[str, int] | dict[str, datetime.datetime]] = {
    "b": {"k": 1},
    "a": {"k": datetime.datetime(year=2040, month=1, day=1, hour=0, minute=0, second=0, tzinfo=datetime.timezone.utc)},
}
