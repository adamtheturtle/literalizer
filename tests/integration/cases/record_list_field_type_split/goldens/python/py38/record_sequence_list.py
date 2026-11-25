from __future__ import annotations
from collections import OrderedDict
import dataclasses
@dataclasses.dataclass(frozen=True)
class Record1:
    kind: str
    urgent: bool
@dataclasses.dataclass(frozen=True)
class Record0:
    entries: list[Record1]
@dataclasses.dataclass(frozen=True)
class Record3:
    error: str
@dataclasses.dataclass(frozen=True)
class Record2:
    entries: list[Record3]
my_data = OrderedDict([
    ("left", Record0(entries=[Record1(kind="add", urgent=True)])),
    ("right", Record2(entries=[Record3(error="not_found")])),
])
