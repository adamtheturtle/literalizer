from __future__ import annotations
import dataclasses
@dataclasses.dataclass(frozen=True)
class Record0:
    nan: float
    positive: float
    negative: float
std = Record0(
    nan=float("nan"),
    positive=float("inf"),
    negative=float("-inf"),
)
