from __future__ import annotations
from typing import Any
def process(data: 'list[object]') -> object: ...
untyped_value: list[Any] = []
process(data=[untyped_value, untyped_value])
