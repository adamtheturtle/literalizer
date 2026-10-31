from __future__ import annotations
import datetime
import dataclasses
@dataclasses.dataclass(frozen=True)
class Record0:
    a: int
def consume(*_args: object, **_kwargs: object) -> object: ...
item = Record0(
    a=1,
)
stamp = datetime.date(year=2001, month=2, day=3)
consume(stamp=stamp, value=item)
