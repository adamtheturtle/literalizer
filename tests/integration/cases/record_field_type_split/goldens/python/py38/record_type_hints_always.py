from __future__ import annotations
import dataclasses
@dataclasses.dataclass(frozen=True)
class Record1:
    status: int
@dataclasses.dataclass(frozen=True)
class Record2:
    status: str
@dataclasses.dataclass(frozen=True)
class Record4:
    kind: str
    urgent: bool
@dataclasses.dataclass(frozen=True)
class Record3:
    inner: Record4
@dataclasses.dataclass(frozen=True)
class Record6:
    error: str
@dataclasses.dataclass(frozen=True)
class Record5:
    inner: Record6
@dataclasses.dataclass(frozen=True)
class Record7:
    holder: Record1
@dataclasses.dataclass(frozen=True)
class Record8:
    holder: Record2
@dataclasses.dataclass(frozen=True)
class Record9:
    nums: tuple[int, ...]
@dataclasses.dataclass(frozen=True)
class Record0:
    plain: Record1
    other: Record2
    nested_a: Record3
    nested_b: Record5
    wrap_a: Record7
    wrap_b: Record8
    wide: Record9
my_data: Record0 = Record0(
    plain=Record1(
        status=1,
    ),
    other=Record2(
        status="ready",
    ),
    nested_a=Record3(
        inner=Record4(
            kind="add",
            urgent=True,
        ),
    ),
    nested_b=Record5(
        inner=Record6(
            error="not_found",
        ),
    ),
    wrap_a=Record7(
        holder=Record1(
            status=2,
        ),
    ),
    wrap_b=Record8(
        holder=Record2(
            status="word",
        ),
    ),
    wide=Record9(
        nums=(
            1,
            1099511627776,
        ),
    ),
)
