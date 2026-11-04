from typing import Any, Union
import dataclasses
@dataclasses.dataclass(frozen=True)
class Record0:
    x: int
my_data: tuple[Union[Record0, tuple[Any, ...]], ...] = (
    Record0(x=1),
    (),
)
