from __future__ import annotations
from collections import OrderedDict
def process(*_args: object, **_kwargs: object) -> object: ...
big_list: tuple[str, ...] = (
    "x",
)
process(a=OrderedDict([("m", big_list)]))
