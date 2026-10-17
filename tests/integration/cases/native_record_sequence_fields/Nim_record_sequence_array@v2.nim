{.warning[UnusedImport]:off.}
import tables
type Record0 = object
    short: seq[int]
    long: seq[int]
var my_data = Record0(
    short: @[
        1
    ],
    long: @[
        1,
        2
    ]
)
