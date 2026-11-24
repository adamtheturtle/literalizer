from typing import Any
import dataclasses
from typing import Any, Union
@dataclasses.dataclass(frozen=True)
class Record0:
    a: tuple[tuple[int, ...], ...]
    b: tuple[Union[tuple[Any, ...], tuple[int, ...]], ...]
my_data = Record0(
    a=(
        (
            1,
            2,
        ),
        (
            3,
        ),
    ),
    b=(
        (),
        (
            1,
        ),
    ),
)
