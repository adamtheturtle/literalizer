from __future__ import annotations
import datetime
my_data: tuple[dict[str, dict[str, tuple[datetime.datetime, ...]]], ...] = (
    {"nested": {"times": (datetime.datetime(year=1900, month=1, day=1, hour=0, minute=0, second=0, tzinfo=datetime.UTC),)}},
    {},
)
