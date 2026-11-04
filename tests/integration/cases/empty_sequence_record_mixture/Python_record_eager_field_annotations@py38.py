from typing import Any, Tuple, Union
import dataclasses
@dataclasses.dataclass(frozen=True)
class Record0:
    x: int
my_data: Tuple[Union[Tuple[Any, ...], Record0], ...] = (
    (),
    Record0(x=1),
)
