from typing import Any, Union
import dataclasses
@dataclasses.dataclass(frozen=True)
class Record0:
    x: int
my_data: tuple[Union[tuple[Union[tuple[int, ...], Record0], ...], tuple[Record0, ...], tuple[Union[tuple[Any, ...], tuple[Record0, ...]], ...], tuple[tuple[Any, ...], ...]], ...] = (
    ((1,), Record0(x=1)),
    (Record0(x=1), Record0(x=2)),
    ((), (Record0(x=1),)),
    ((), ()),
)
