from __future__ import annotations
def process(*_args: object, **_kwargs: object) -> object: ...
my_var = 42
my_other = 7
process(data=(my_var, 42, "static"))
process(data=(my_other, 7, "label"))
