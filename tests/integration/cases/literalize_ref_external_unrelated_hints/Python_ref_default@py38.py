from __future__ import annotations
from typing import Any
def consume_widget(*_args: object, **_kwargs: object) -> object: ...
missing = (
    1,
    2,
)
my_data = missing
consume_widget(arg_value=my_data)
