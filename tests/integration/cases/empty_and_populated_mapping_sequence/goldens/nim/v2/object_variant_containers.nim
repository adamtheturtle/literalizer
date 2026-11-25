import tables
type
  ValueKind = enum
    vkInt, vkTable
  Value = object
    case kind: ValueKind
    of vkInt: intVal: int
    of vkTable: tableVal: Table[string, Value]
var my_data = @[
    Value(kind: vkTable, tableVal: initTable[string, Value]()),
    Value(kind: vkTable, tableVal: {"value": Value(kind: vkInt, intVal: 1)}.toTable)
]
