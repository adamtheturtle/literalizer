from __future__ import annotations
from collections import OrderedDict
from typing import Any
import dataclasses
@dataclasses.dataclass(frozen=True)
class Record0:
    values: OrderedDict[str, tuple[tuple[int, ...] | tuple[Any, ...], ...] | tuple[tuple[int, ...], ...] | str]
    flag: bool
    direct_arrays: tuple[tuple[int, ...] | tuple[Any, ...], ...]
my_data = Record0(
    values=OrderedDict([
        ("wide", (
            (
                2208988800,
            ),
            (),
        )),
        ("narrow", (
            (
                946684800,
            ),
        )),
        ("negative", (
            (
                -2208988800,
            ),
        )),
        ("shifted", (
            (
                2208988800,
            ),
        )),
        ("mixed_width", (
            (
                946684800,
            ),
            (
                2208988800,
            ),
        )),
        ("text", "preserve"),
    ]),
    flag=True,
    direct_arrays=(
        (
            2208988800,
        ),
        (),
    ),
)
