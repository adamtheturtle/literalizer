{.warning[UnusedImport]:off.}
import tables
type Record1 = object
    a: int
    b: string
    c: pointer
type Record0 = object
    outer: Record1
var my_data = Record0(
    outer: Record1(
        a: 1,
        b: "x",
        c: nil
    )
)
