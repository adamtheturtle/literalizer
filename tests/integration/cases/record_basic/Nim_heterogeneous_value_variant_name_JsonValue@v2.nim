import tables
type
  JsonValueKind = enum
    vkInt, vkStr, vkBool, vkList
  JsonValue = object
    case kind: JsonValueKind
    of vkInt: intVal: int
    of vkStr: strVal: string
    of vkBool: boolVal: bool
    of vkList: listVal: seq[JsonValue]
var my_data = {
    "id": JsonValue(kind: vkInt, intVal: 1),
    "description": JsonValue(kind: vkStr, strVal: "She said \"hello\", then waved"),
    "is_done": JsonValue(kind: vkBool, boolVal: false),
    "blocks": JsonValue(kind: vkList, listVal: @[JsonValue(kind: vkInt, intVal: 1), JsonValue(kind: vkInt, intVal: 2), JsonValue(kind: vkInt, intVal: 3)])
}.toTable
