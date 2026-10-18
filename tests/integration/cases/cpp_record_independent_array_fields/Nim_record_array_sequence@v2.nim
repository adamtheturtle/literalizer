{.warning[UnusedImport]:off.}
import tables
type Record0 = object
    numbers: seq[int]
    words: seq[string]
var my_data = Record0(
    numbers: @[
        1
    ],
    words: @[
        "s"
    ]
)
