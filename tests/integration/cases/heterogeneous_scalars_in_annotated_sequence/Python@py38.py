from __future__ import annotations
import datetime
from typing import Any, Tuple, Union
my_data: Tuple[Union[bool, float, None, datetime.date, datetime.datetime, Tuple[Any, ...]], ...] = (
    True,
    1.5,
    None,
    datetime.date(year=2020, month=1, day=1),
    datetime.datetime(year=2020, month=1, day=1, hour=0, minute=0, second=0, tzinfo=datetime.timezone.utc),
    (),
)
