import dataclasses
@dataclasses.dataclass(frozen=True)
class Record0:
    name: str
    active: bool
my_data = (
    Record0(name="Ada", active=True),
)
