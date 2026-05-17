{.warning[UnusedImport]:off.}
import tables
type Record0 = object
    name: string
    scores: seq[int]
var my_data = Record0(
    name: "Alice",
    scores: @[
        10,
        20,
        30
    ]
)
