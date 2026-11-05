from __future__ import annotations
def process(*_args: object, **_kwargs: object) -> object: ...
my_var: tuple[int, ...] = (
    1,
    2,
    3,
)
process(data=my_var)
