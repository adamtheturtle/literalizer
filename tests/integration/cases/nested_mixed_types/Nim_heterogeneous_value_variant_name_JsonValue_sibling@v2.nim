type
  JsonValueKind = enum
    vkInt, vkStr, vkList
  JsonValue = object
    case kind: JsonValueKind
    of vkInt: intVal: int
    of vkStr: strVal: string
    of vkList: listVal: seq[JsonValue]
var my_data = @[
    JsonValue(kind: vkList, listVal: @[JsonValue(kind: vkInt, intVal: 1), JsonValue(kind: vkInt, intVal: 2)]),
    JsonValue(kind: vkList, listVal: @[JsonValue(kind: vkStr, strVal: "a"), JsonValue(kind: vkStr, strVal: "b")])
]
