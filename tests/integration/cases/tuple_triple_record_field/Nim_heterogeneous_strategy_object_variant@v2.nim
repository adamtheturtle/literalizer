import tables
type
  ValueKind = enum
    vkStr, vkInt, vkBool, vkList
  Value = object
    case kind: ValueKind
    of vkStr: strVal: string
    of vkInt: intVal: int
    of vkBool: boolVal: bool
    of vkList: listVal: seq[Value]
var my_data = {
    "call": Value(kind: vkStr, strVal: "send"),
    "args": Value(kind: vkList, listVal: @[Value(kind: vkInt, intVal: 1), Value(kind: vkStr, strVal: "email"), Value(kind: vkBool, boolVal: true)])
}.toTable
