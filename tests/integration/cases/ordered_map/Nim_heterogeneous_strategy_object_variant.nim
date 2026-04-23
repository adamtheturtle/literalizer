import tables
type
  ValueKind = enum
    vkStr, vkInt, vkBool
  Value = object
    case kind: ValueKind
    of vkStr: strVal: string
    of vkInt: intVal: int
    of vkBool: boolVal: bool
var my_data = {
    "name": Value(kind: vkStr, strVal: "Alice"),
    "age": Value(kind: vkInt, intVal: 30),
    "active": Value(kind: vkBool, boolVal: true)
}.toOrderedTable
