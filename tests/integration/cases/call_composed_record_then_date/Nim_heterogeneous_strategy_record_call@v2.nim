{.warning[UnusedImport]:off.}
import tables
type Record0 = object
    a: int
template consume(args: varargs[untyped]) = discard
var item = Record0(
    a: 1
)
var stamp = {"year": 2001, "month": 2, "day": 3}
consume(stamp, item)
