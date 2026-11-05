from __future__ import annotations
def process(*_args: object, **_kwargs: object) -> object: ...
big_list: tuple[str, ...] = (
    "x",
)
process(a={"k": big_list}, b=2)
