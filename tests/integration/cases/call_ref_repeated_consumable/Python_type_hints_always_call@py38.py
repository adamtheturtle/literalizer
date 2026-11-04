from __future__ import annotations
def process(*_args: object, **_kwargs: object) -> object: ...
item: tuple[int, ...] = (
    1,
    2,
)
process(data=item)
process(data=item)
