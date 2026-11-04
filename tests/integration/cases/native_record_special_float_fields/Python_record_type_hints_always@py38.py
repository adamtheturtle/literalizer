from __future__ import annotations
import dataclasses
@dataclasses.dataclass(frozen=True)
class Record0:
    positive: float
    negative: float
    nan_value: float
    finite: float
my_data: Record0 = Record0(
    positive=float("inf"),
    negative=float("-inf"),
    nan_value=float("nan"),
    finite=1.5,
)
