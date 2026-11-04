from typing import Any, Tuple, Union
import dataclasses
@dataclasses.dataclass(frozen=True)
class Record0:
    x: int
my_data: Tuple[Union[Tuple[Union[Tuple[int, ...], Record0], ...], Tuple[Record0, ...], Tuple[Union[Tuple[Any, ...], Tuple[Record0, ...]], ...], Tuple[Tuple[Any, ...], ...]], ...] = (
    ((1,), Record0(x=1)),
    (Record0(x=1), Record0(x=2)),
    ((), (Record0(x=1),)),
    ((), ()),
)
