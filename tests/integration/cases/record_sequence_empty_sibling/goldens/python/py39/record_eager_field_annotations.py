from typing import Any, Union
import dataclasses
from typing import Union
@dataclasses.dataclass(frozen=True)
class Record0:
    x: int
my_data: tuple[Union[tuple[Any, ...], tuple[Record0, ...]], ...] = (
    (),
    (Record0(x=1),),
)
