from collections import OrderedDict
from typing import Any, cast

x: Any = OrderedDict(
    cast(
        "list[tuple[str, Any]]",
        [
            ("name", "Alice"),
            ("age", 30),
            ("active", True),
        ],
    )
)
