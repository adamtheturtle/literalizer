import tables
type
  ValueKind = enum
    vkInt, vkStr, vkTable
  Value = object
    case kind: ValueKind
    of vkInt: intVal: int
    of vkStr: strVal: string
    of vkTable: tableVal: Table[string, Value]
var my_data = @[
    Value(kind: vkTable, tableVal: {"count": Value(kind: vkInt, intVal: 1), "name": Value(kind: vkStr, strVal: "value")}.toTable),
    Value(kind: vkTable, tableVal: initTable[string, Value]())
]
