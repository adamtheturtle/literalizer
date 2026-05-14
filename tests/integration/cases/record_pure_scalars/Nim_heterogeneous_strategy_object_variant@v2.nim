import tables
type
  ValueKind = enum
    vkStr, vkInt, vkBool, vkFloat
  Value = object
    case kind: ValueKind
    of vkStr: strVal: string
    of vkInt: intVal: int
    of vkBool: boolVal: bool
    of vkFloat: floatVal: float
var my_data = {
    "name": Value(kind: vkStr, strVal: "Alice"),
    "age": Value(kind: vkInt, intVal: 30),
    "active": Value(kind: vkBool, boolVal: true),
    "score": Value(kind: vkFloat, floatVal: 4.5)
}.toTable
