from __future__ import annotations
from typing import Any
import dataclasses
@dataclasses.dataclass(frozen=True)
class Record0:
    f: dict[str, Any]
    g: int
my_data: Record0 = Record0(
    f={},
    g=1,
)
