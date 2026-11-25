import tables
type
  ValueKind = enum
    vkStr, vkInt, vkList
  Value = object
    case kind: ValueKind
    of vkStr: strVal: string
    of vkInt: intVal: int
    of vkList: listVal: seq[Value]
var my_data = {
    "name": Value(kind: vkStr, strVal: "Alice"),
    "scores": Value(kind: vkList, listVal: @[Value(kind: vkInt, intVal: 10), Value(kind: vkInt, intVal: 20), Value(kind: vkInt, intVal: 30)])
}.toTable
