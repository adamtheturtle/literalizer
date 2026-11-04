import dataclasses
from typing import Tuple, Union
@dataclasses.dataclass(frozen=True)
class Record0:
    call: str
    args: Tuple[Union[int, str], ...]
my_data = Record0(
    call="send",
    args=(
        1,
        "email",
    ),
)
