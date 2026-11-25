{.warning[UnusedImport]:off.}
type
  ValueKind = enum
    vkInt, vkStr, vkList
  Value = object
    case kind: ValueKind
    of vkInt: intVal: int
    of vkStr: strVal: string
    of vkList: listVal: seq[Value]
template process(args: varargs[untyped]) = discard
var my_ints = @[
    1,
    2,
    3
]
var my_strings = @[
    "a",
    "b"
]
var my_empty = newSeq[string]()
process(my_ints, 42)
process(my_strings, 7)
process(my_empty, 99)
