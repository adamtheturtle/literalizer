import dataclasses
from typing import Union
@dataclasses.dataclass(frozen=True)
class Record0:
    call: str
    args: tuple[Union[int, str, bool], ...]
my_data = Record0(
    call="send",
    args=(
        1,
        "email",
        True,
    ),
)
