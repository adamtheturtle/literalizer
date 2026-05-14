import tables
type
  JsonValueKind = enum
    vkInt, vkStr, vkNull
  JsonValue = object
    case kind: JsonValueKind
    of vkInt: intVal: int
    of vkStr: strVal: string
    of vkNull: discard
var my_data = {
    "outer": {"a": JsonValue(kind: vkInt, intVal: 1), "b": JsonValue(kind: vkStr, strVal: "x"), "c": JsonValue(kind: vkNull)}.toTable
}.toTable
