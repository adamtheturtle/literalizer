{.warning[UnusedImport]:off.}
import tables
type Record1 = object
    name: string
    age: int
type Record0 = object
    id: int
    owner: Record1
var my_data = Record0(
    id: 1,
    owner: Record1(
        name: "Alice",
        age: 30
    )
)
