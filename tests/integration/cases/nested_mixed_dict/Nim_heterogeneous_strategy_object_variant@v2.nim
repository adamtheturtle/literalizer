import tables
type
  ValueKind = enum
    vkInt, vkStr, vkNull, vkTable
  Value = object
    case kind: ValueKind
    of vkInt: intVal: int
    of vkStr: strVal: string
    of vkNull: discard
    of vkTable: tableVal: Table[string, Value]
var my_data = {
    "outer": Value(kind: vkTable, tableVal: {"a": Value(kind: vkInt, intVal: 1), "b": Value(kind: vkStr, strVal: "x"), "c": Value(kind: vkNull)}.toTable)
}.toTable
