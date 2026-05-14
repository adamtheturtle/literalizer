import tables
type
  JsonValueKind = enum
    vkInt, vkStr
  JsonValue = object
    case kind: JsonValueKind
    of vkInt: intVal: int
    of vkStr: strVal: string
var my_data = {
    "a": JsonValue(kind: vkInt, intVal: 1),
    "b": JsonValue(kind: vkInt, intVal: 3000000000),
    "c": JsonValue(kind: vkStr, strVal: "x")
}.toTable
