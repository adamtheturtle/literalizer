from __future__ import annotations
def process(*_args: object, **_kwargs: object) -> object: ...
single_var: tuple[int, ...] = (
    4,
    5,
    6,
)
repeated_var: int = 1
process(data=repeated_var, count=1)
process(data=single_var, count=0)
process(data=repeated_var, count=8)
