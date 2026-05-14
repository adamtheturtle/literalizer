type
  JsonValueKind = enum
    vkStr, vkInt
  JsonValue = object
    case kind: JsonValueKind
    of vkStr: strVal: string
    of vkInt: intVal: int
var my_data = @[
    JsonValue(kind: vkStr, strVal: "hello"),
    JsonValue(kind: vkInt, intVal: 42)
]
