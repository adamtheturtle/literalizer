{.warning[UnusedImport]:off.}
import tables
type Record0 = object
    a: int
template consume(args: varargs[untyped]) = discard
var item = Record0(
    a: 1
)
consume(item)
