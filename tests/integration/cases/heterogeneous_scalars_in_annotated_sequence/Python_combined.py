import datetime
from typing import Any
my_data: tuple[bool | float | None | datetime.date | datetime.datetime | tuple[Any, ...], ...] = (
    True,
    1.5,
    None,
    datetime.date(year=2020, month=1, day=1),
    datetime.datetime(year=2020, month=1, day=1, hour=0, minute=0, second=0),
    (),
)
my_data = (
    True,
    1.5,
    None,
    datetime.date(year=2020, month=1, day=1),
    datetime.datetime(year=2020, month=1, day=1, hour=0, minute=0, second=0),
    (),
)
