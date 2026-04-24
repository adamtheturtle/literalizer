from typing import Any
def process(*_args: object, **_kwargs: object) -> object: ...
items: tuple[Any, ...] = (
process(a=1, b=42),
process(a=2, b=100),
)
