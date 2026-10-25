from __future__ import annotations
from typing import Any
def process(*_args: object, **_kwargs: object) -> object: ...
untyped_value: tuple[Any, ...] = ()
process(data=(untyped_value, untyped_value))
