from typing import Any, Tuple
import dataclasses
from typing import Union
@dataclasses.dataclass(frozen=True)
class Record0:
    x: int
my_data: Tuple[Union[Tuple[Any, ...], Record0], ...] = (
    (),
    Record0(x=1),
)
