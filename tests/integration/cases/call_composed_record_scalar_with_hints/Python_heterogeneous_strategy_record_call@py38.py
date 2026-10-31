from __future__ import annotations
import dataclasses
@dataclasses.dataclass(frozen=True)
class Record0:
    a: int
def consume(*_args: object, **_kwargs: object) -> object: ...
item = Record0(
    a=1,
)
consume(value=item)
