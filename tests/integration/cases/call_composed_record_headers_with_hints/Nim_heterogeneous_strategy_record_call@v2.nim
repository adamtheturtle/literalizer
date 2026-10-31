{.warning[UnusedImport]:off.}
import tables
type Record0 = object
    name: string
    values: seq[int]
template consume(args: varargs[untyped]) = discard
var item = Record0(
    name: "first",
    values: @[
        1,
        2
    ]
)
consume(item)
