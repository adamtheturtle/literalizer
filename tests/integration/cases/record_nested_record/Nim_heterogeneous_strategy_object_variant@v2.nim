import tables
type
  ValueKind = enum
    vkInt, vkStr, vkTable
  Value = object
    case kind: ValueKind
    of vkInt: intVal: int
    of vkStr: strVal: string
    of vkTable: tableVal: Table[string, Value]
var my_data = {
    "id": Value(kind: vkInt, intVal: 1),
    "owner": Value(kind: vkTable, tableVal: {"name": Value(kind: vkStr, strVal: "Alice"), "age": Value(kind: vkInt, intVal: 30)}.toTable)
}.toTable
