{.warning[UnusedImport]:off.}
import tables
type Record0 = object
    a: int
    b: string
template consume_widget(args: varargs[untyped]) = discard
consume_widget(Record0(
    a: 1,
    b: "x"
))
