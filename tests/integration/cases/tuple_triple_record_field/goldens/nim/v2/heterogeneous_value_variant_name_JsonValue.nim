import tables
type
  JsonValueKind = enum
    vkStr, vkInt, vkBool, vkList
  JsonValue = object
    case kind: JsonValueKind
    of vkStr: strVal: string
    of vkInt: intVal: int
    of vkBool: boolVal: bool
    of vkList: listVal: seq[JsonValue]
var my_data = {
    "call": JsonValue(kind: vkStr, strVal: "send"),
    "args": JsonValue(kind: vkList, listVal: @[JsonValue(kind: vkInt, intVal: 1), JsonValue(kind: vkStr, strVal: "email"), JsonValue(kind: vkBool, boolVal: true)])
}.toTable
