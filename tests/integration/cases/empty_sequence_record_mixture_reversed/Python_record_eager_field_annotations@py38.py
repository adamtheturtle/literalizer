from typing import Any, Tuple, Union
import dataclasses
@dataclasses.dataclass(frozen=True)
class Record0:
    x: int
my_data: Tuple[Union[Record0, Tuple[Any, ...]], ...] = (
    Record0(x=1),
    (),
)
