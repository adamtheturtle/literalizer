from __future__ import annotations
from typing import Any
import dataclasses
@dataclasses.dataclass(frozen=True)
class Record0:
    bound: dict[str, Any]
empty_map: dict[str, Any] = {}
my_data = Record0(
    bound=empty_map,
)
