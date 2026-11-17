from __future__ import annotations
import dataclasses
@dataclasses.dataclass(frozen=True)
class Record0:
    name: str
    age: int
    active: bool
    score: float
my_data = Record0(
    name="Alice",
    age=30,
    active=True,
    score=4.5,
)
# Independent native value checks.
from dataclasses import fields, is_dataclass
assert is_dataclass(obj=my_data)
assert [field.name for field in fields(class_or_instance=my_data)] == ["name", "age", "active", "score"]
assert my_data.name == "Alice"
assert type(my_data.age) is int and my_data.age == 30
assert my_data.active is True
assert type(my_data.score) is float and my_data.score == 4.5
