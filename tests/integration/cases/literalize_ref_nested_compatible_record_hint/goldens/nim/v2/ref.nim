{.warning[UnusedImport]:off.}
import tables
type Record1 = object
    items: seq[int]
type Record0 = object
    outer: Record1
var recordData = Record1(
    items: @[
        1,
        2
    ]
)
var my_data = Record0(
    outer: recordData
)
