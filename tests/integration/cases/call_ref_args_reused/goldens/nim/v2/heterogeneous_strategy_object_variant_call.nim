{.warning[UnusedImport]:off.}
type
  ValueKind = enum
    vkInt, vkList
  Value = object
    case kind: ValueKind
    of vkInt: intVal: int
    of vkList: listVal: seq[Value]
template process(args: varargs[untyped]) = discard
var single_var = @[
    4,
    5,
    6
]
var repeated_var = 1
process(repeated_var, 1)
process(single_var, 0)
process(repeated_var, 8)
