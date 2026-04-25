import datetime
from typing import Any
my_data: tuple[tuple[datetime.date, ...] | tuple[Any, ...], ...] = (
    (datetime.date(year=2026, month=1, day=1), datetime.date(year=2026, month=1, day=2)),
    (),
    (datetime.date(year=2026, month=2, day=3), datetime.date(year=2026, month=2, day=4)),
)
my_data = (
    (datetime.date(year=2026, month=1, day=1), datetime.date(year=2026, month=1, day=2)),
    (),
    (datetime.date(year=2026, month=2, day=3), datetime.date(year=2026, month=2, day=4)),
)
