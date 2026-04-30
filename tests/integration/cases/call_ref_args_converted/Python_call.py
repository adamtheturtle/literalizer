from __future__ import annotations
def process(*_args: object, **_kwargs: object) -> object: ...
my_var = (
    1,
    2,
    3,
)
my_other = (
    4,
    5,
    6,
)
process(data=my_var, count=42)
process(data=my_other, count=7)
