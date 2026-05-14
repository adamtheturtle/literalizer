import tables
type
  JsonValueKind = enum
    vkStr, vkInt, vkBool
  JsonValue = object
    case kind: JsonValueKind
    of vkStr: strVal: string
    of vkInt: intVal: int
    of vkBool: boolVal: bool
var my_data = {
    "name": JsonValue(kind: vkStr, strVal: "Alice"),
    "age": JsonValue(kind: vkInt, intVal: 30),
    "active": JsonValue(kind: vkBool, boolVal: true)
}.toOrderedTable
