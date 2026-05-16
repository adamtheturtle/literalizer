from __future__ import annotations
import dataclasses
@dataclasses.dataclass(frozen=True)
class Record0:
    title: str
    tags: tuple[str, ...]
    priority: int
my_data = Record0(
    title="report",
    tags=(
        "draft",
        "urgent",
        "review",
    ),
    priority=2,
)
