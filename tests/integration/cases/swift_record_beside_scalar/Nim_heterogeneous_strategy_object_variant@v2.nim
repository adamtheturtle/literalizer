import tables
type
  ValueKind = enum
    vkInt, vkTable
  Value = object
    case kind: ValueKind
    of vkInt: intVal: int
    of vkTable: tableVal: Table[string, Value]
var my_data = @[
    Value(kind: vkTable, tableVal: {"a": Value(kind: vkInt, intVal: 1)}.toTable),
    Value(kind: vkInt, intVal: 5)
]
