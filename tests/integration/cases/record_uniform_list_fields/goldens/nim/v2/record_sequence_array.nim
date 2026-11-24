{.warning[UnusedImport]:off.}
import tables
type Record0 = object
    scores: seq[int]
var my_data = @[
    Record0(scores: @[1, 2]),
    Record0(scores: @[3, 4])
]
