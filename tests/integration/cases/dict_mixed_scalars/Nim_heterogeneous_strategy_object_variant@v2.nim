import tables
type
  ValueKind = enum
    vkInt, vkStr
  Value = object
    case kind: ValueKind
    of vkInt: intVal: int
    of vkStr: strVal: string
var my_data = {
    "a": Value(kind: vkInt, intVal: 1),
    "b": Value(kind: vkStr, strVal: "x")
}.toTable
