from __future__ import annotations
import datetime
from typing import Any
my_data: dict[str, tuple[tuple[datetime.time, ...] | tuple[Any, ...], ...]] = {
    "mixed": ((datetime.time(hour=9, minute=30, second=0),), ()),
}
