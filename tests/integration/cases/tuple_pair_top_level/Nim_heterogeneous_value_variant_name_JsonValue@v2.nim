type
  JsonValueKind = enum
    vkInt, vkStr
  JsonValue = object
    case kind: JsonValueKind
    of vkInt: intVal: int
    of vkStr: strVal: string
var my_data = @[
    JsonValue(kind: vkInt, intVal: 1),
    JsonValue(kind: vkStr, strVal: "email")
]
