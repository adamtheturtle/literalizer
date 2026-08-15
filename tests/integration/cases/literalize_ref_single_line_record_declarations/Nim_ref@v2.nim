{.warning[UnusedImport]:off.}
import tables
type Record1 = object
    x: string
type Record2 = object
    x: int
type Record0 = object
    direct: Record1
    bound: Record2
var first = Record2(
    x: 1
)
var my_data = Record0(
    direct: Record1(
        x: "s"
    ),
    bound: first
)
