from __future__ import annotations
from typing import Any
import dataclasses
@dataclasses.dataclass(frozen=True)
class Record0:
    label: str
    meta: dict[str, Any]
my_data: Record0 = Record0(
    label="tag",
    meta={},
)
