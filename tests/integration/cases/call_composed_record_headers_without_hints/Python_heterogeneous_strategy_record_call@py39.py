from __future__ import annotations
import dataclasses
@dataclasses.dataclass(frozen=True)
class Record0:
    name: str
    values: tuple[int, ...]
def consume(*_args: object, **_kwargs: object) -> object: ...
item = Record0(
    name="first",
    values=(
        1,
        2,
    ),
)
consume(value=item)
