from typing import Any
import dataclasses
from typing import Union
@dataclasses.dataclass(frozen=True)
class Record0:
    x: int
my_data: tuple[Union[Record0, tuple[Any, ...]], ...] = (
    Record0(x=1),
    (),
)
