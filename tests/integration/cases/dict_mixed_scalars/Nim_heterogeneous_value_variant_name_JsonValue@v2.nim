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
    "b": JsonValue(kind: vkStr, strVal: "x")
}.toTable
