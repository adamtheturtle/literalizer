from __future__ import annotations
from typing import Any
def consume_widget(*_args: object, **_kwargs: object) -> object: ...
item: tuple[Any, ...] = ()
my_data = (
    item,
    item,
)
consume_widget(arg_value=my_data)
