{.warning[UnusedImport]:off.}
import tables
type Record1 = object
    name: string
    active: bool
type Record2 = object
    name: string
    score: float
type Record0 = object
    owner: Record1
    members: seq[Record2]
var my_data = Record0(
    owner: Record1(
        name: "Ada",
        active: false
    ),
    members: @[
        Record2(
            name: "Ada",
            score: 1.5
        ),
        Record2(
            name: "Bob",
            score: 2.5
        )
    ]
)
