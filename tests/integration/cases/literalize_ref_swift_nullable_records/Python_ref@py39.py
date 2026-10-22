from __future__ import annotations
import dataclasses
@dataclasses.dataclass(frozen=True)
class Record1:
    x: int
    y: None
@dataclasses.dataclass(frozen=True)
class Record2:
    x: None
    y: None
@dataclasses.dataclass(frozen=True)
class Record3:
    x: int
    y: int
@dataclasses.dataclass(frozen=True)
class Record0:
    nullable: Record1
    null_fields: Record2
    plain: Record3
nullable = Record1(
    x=1,
    y=None,
)
null_fields = Record2(
    x=None,
    y=None,
)
plain = Record3(
    x=1,
    y=2,
)
my_data = Record0(
    nullable=nullable,
    null_fields=null_fields,
    plain=plain,
)
