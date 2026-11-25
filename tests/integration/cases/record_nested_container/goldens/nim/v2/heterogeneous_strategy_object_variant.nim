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
    "title": Value(kind: vkStr, strVal: "report"),
    "tags": Value(kind: vkList, listVal: @[Value(kind: vkStr, strVal: "draft"), Value(kind: vkStr, strVal: "urgent"), Value(kind: vkStr, strVal: "review")]),
    "priority": Value(kind: vkInt, intVal: 2)
}.toTable
