from __future__ import annotations
def consume(*_args: object, **_kwargs: object) -> object: ...
item: tuple[int, ...] = (
    1,
    2,
)
consume(value=item)
