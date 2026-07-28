from __future__ import annotations
from typing import Any, Tuple
def process(*_args: object, **_kwargs: object) -> object: ...
my_list: Tuple[Any, ...] = ()
process(data=(({"inner": my_list},),))
