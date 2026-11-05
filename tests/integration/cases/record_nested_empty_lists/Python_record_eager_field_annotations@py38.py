from typing import Any, Tuple
import dataclasses
from typing import Any, Tuple, Union
@dataclasses.dataclass(frozen=True)
class Record0:
    a: Tuple[Tuple[int, ...], ...]
    b: Tuple[Union[Tuple[Any, ...], Tuple[int, ...]], ...]
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
