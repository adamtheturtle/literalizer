from __future__ import annotations
from typing import Any
def process(data: 'tuple[object, ...]') -> object: ...
unknown_value: tuple[Any, ...] = ()
process(data=unknown_value)
