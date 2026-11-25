from __future__ import annotations
import dataclasses
@dataclasses.dataclass(frozen=True)
class Record0:
    value: str
def consume(*_args: object, **_kwargs: object) -> object: ...
item = Record0(
    value="owned",
)
consume(value=item)
