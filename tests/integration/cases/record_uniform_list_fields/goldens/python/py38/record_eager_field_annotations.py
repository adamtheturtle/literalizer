import dataclasses
from typing import Tuple
@dataclasses.dataclass(frozen=True)
class Record0:
    scores: Tuple[int, ...]
my_data = (
    Record0(scores=(1, 2)),
    Record0(scores=(3, 4)),
)
