import tables
type
  ValueKind = enum
    vkInt, vkList
  Value = object
    case kind: ValueKind
    of vkInt: intVal: int
    of vkList: listVal: seq[Value]
var my_data = {
    "a": Value(kind: vkList, listVal: @[Value(kind: vkList, listVal: @[Value(kind: vkInt, intVal: 1), Value(kind: vkInt, intVal: 2)]), Value(kind: vkList, listVal: @[Value(kind: vkInt, intVal: 3)])]),
    "b": Value(kind: vkList, listVal: @[Value(kind: vkList, listVal: newSeq[Value]()), Value(kind: vkList, listVal: @[Value(kind: vkInt, intVal: 1)])])
}.toTable
