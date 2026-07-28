from __future__ import annotations
from typing import Any
def process(*_args: object, **_kwargs: object) -> object: ...
known_value = 1
unknown_value: tuple[Any, ...] = ()
process(data=unknown_value)
