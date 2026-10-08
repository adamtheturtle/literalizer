{.warning[UnusedImport]:off.}
import tables
type Record0 = object
    value: int
template consume(args: varargs[untyped]) = discard
var item = Record0(
    value: 1
)
consume(item)
