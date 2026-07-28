from __future__ import annotations
from typing import Any
def process(*_args: object, **_kwargs: object) -> object: ...
my_list: tuple[Any, ...] = ()
process(data=(({"inner": my_list},),))
