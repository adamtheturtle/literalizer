from __future__ import annotations
from typing import Any, Tuple
def process(*_args: object, **_kwargs: object) -> object: ...
known_value = 1
unknown_value: Tuple[Any, ...] = ()
process(data=unknown_value)
