{.warning[UnusedImport]:off.}
import tables
type Record0 = object
    value: string
template consume(args: varargs[untyped]) = discard
var item = Record0(
    value: "owned"
)
consume(item)
