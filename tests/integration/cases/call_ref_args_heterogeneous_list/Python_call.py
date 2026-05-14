from __future__ import annotations
from typing import Any
def process(*_args: object, **_kwargs: object) -> object: ...
my_ints = (
    1,
    2,
    3,
)
my_strings = (
    "a",
    "b",
)
my_empty: tuple[Any, ...] = ()
process(data=my_ints, count=42)
process(data=my_strings, count=7)
process(data=my_empty, count=99)
