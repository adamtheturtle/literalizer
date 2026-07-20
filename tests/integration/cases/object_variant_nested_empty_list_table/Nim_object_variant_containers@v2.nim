import tables
type
  ValueKind = enum
    vkInt, vkList, vkTable
  Value = object
    case kind: ValueKind
    of vkInt: intVal: int
    of vkList: listVal: seq[Value]
    of vkTable: tableVal: Table[string, Value]
var my_data = @[
    Value(kind: vkTable, tableVal: {"value": Value(kind: vkList, listVal: newSeq[Value]())}.toTable),
    Value(kind: vkTable, tableVal: {"value": Value(kind: vkList, listVal: @[Value(kind: vkInt, intVal: 1)])}.toTable)
]
