{.warning[UnusedImport]:off.}
import tables
type Record1 = object
    a: int
type Record0 = object
    items: seq[Record1]
var my_data = Record0(
    items: @[
        Record1(
            a: 1
        )
    ]
)
