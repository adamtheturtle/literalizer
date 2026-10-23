{.warning[UnusedImport]:off.}
import tables
type Record0 = object
    value: seq[int]
var shared = Record0(
    value: @[
        1,
        2
    ]
)
var my_data = @[
    shared,
    shared
]
