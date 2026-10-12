from __future__ import annotations
import dataclasses
@dataclasses.dataclass(frozen=True)
class Record0:
    due_date: int
    parent_id: int
    assignee: str
my_data = (
    Record0(due_date=-1, parent_id=-1, assignee=""),
    Record0(due_date=10, parent_id=20, assignee="alice"),
)
