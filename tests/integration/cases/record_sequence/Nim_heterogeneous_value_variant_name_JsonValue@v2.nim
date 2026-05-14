import tables
type
  JsonValueKind = enum
    vkInt, vkStr
  JsonValue = object
    case kind: JsonValueKind
    of vkInt: intVal: int
    of vkStr: strVal: string
var my_data = @[
    {"id": JsonValue(kind: vkInt, intVal: 1), "label": JsonValue(kind: vkStr, strVal: "first")}.toTable,
    {"id": JsonValue(kind: vkInt, intVal: 2), "label": JsonValue(kind: vkStr, strVal: "second")}.toTable,
    {"id": JsonValue(kind: vkInt, intVal: 3), "label": JsonValue(kind: vkStr, strVal: "third")}.toTable
]
