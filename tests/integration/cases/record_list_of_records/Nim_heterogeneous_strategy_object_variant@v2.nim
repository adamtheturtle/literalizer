import tables
type
  ValueKind = enum
    vkStr, vkInt, vkList, vkTable
  Value = object
    case kind: ValueKind
    of vkStr: strVal: string
    of vkInt: intVal: int
    of vkList: listVal: seq[Value]
    of vkTable: tableVal: Table[string, Value]
var my_data = {
    "name": Value(kind: vkStr, strVal: "box"),
    "items": Value(kind: vkList, listVal: @[Value(kind: vkTable, tableVal: {"id": Value(kind: vkInt, intVal: 1), "label": Value(kind: vkStr, strVal: "first")}.toTable), Value(kind: vkTable, tableVal: {"id": Value(kind: vkInt, intVal: 2), "label": Value(kind: vkStr, strVal: "second")}.toTable)])
}.toTable
