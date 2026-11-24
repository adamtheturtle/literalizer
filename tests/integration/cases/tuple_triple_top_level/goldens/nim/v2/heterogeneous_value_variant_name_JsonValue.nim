type
  JsonValueKind = enum
    vkInt, vkStr, vkBool
  JsonValue = object
    case kind: JsonValueKind
    of vkInt: intVal: int
    of vkStr: strVal: string
    of vkBool: boolVal: bool
var my_data = @[
    JsonValue(kind: vkInt, intVal: 1),
    JsonValue(kind: vkStr, strVal: "email"),
    JsonValue(kind: vkBool, boolVal: true)
]
