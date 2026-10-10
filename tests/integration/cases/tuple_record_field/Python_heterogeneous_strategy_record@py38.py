from __future__ import annotations
import dataclasses
@dataclasses.dataclass(frozen=True)
class Record0:
    call: str
    args: tuple[int | str, ...]
my_data = Record0(
    call="send",
    args=(
        1,
        "email",
        "a@gmail.com",
        100,
    ),
)
