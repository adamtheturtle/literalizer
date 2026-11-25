from __future__ import annotations
import dataclasses
@dataclasses.dataclass(frozen=True)
class Record0:
    a: int
    b: str
def consume_widget(*_args: object, **_kwargs: object) -> object: ...
consume_widget(arg_value=Record0(
    a=1,
    b="x",
))
