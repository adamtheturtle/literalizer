import tables
type
  ValueKind = enum
    vkInt, vkStr, vkList
  Value = object
    case kind: ValueKind
    of vkInt: intVal: int
    of vkStr: strVal: string
    of vkList: listVal: seq[Value]
var my_data = {
    "scores": Value(kind: vkList, listVal: @[Value(kind: vkInt, intVal: 10), Value(kind: vkInt, intVal: 20), Value(kind: vkInt, intVal: 30)]),
    "args": Value(kind: vkList, listVal: @[Value(kind: vkInt, intVal: 1), Value(kind: vkStr, strVal: "email"), Value(kind: vkStr, strVal: "a@gmail.com"), Value(kind: vkInt, intVal: 100)])
}.toTable
