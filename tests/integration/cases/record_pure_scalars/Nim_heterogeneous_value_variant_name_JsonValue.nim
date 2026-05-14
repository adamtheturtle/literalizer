import tables
type
  JsonValueKind = enum
    vkStr, vkInt, vkBool, vkFloat
  JsonValue = object
    case kind: JsonValueKind
    of vkStr: strVal: string
    of vkInt: intVal: int
    of vkBool: boolVal: bool
    of vkFloat: floatVal: float
var my_data = {
    "name": JsonValue(kind: vkStr, strVal: "Alice"),
    "age": JsonValue(kind: vkInt, intVal: 30),
    "active": JsonValue(kind: vkBool, boolVal: true),
    "score": JsonValue(kind: vkFloat, floatVal: 4.5)
}.toTable
