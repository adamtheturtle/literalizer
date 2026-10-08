{.warning[UnusedImport]:off.}
import tables
type Record1 = object
    value: int
type Record0 = object
    child: Record1
var first = Record0(
    child: Record1(
        value: 1
    )
)
var my_data = first
