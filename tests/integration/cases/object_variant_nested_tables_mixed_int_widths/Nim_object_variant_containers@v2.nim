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
    Value(kind: vkList, listVal: @[Value(kind: vkTable, tableVal: {"value": Value(kind: vkInt, intVal: 1)}.toTable)]),
    Value(kind: vkList, listVal: @[Value(kind: vkTable, tableVal: {"value": Value(kind: vkInt, intVal: 1099511627776)}.toTable)])
]
