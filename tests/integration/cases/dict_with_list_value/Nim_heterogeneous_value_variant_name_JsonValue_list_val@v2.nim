import tables
type
  JsonValueKind = enum
    vkStr, vkInt, vkList
  JsonValue = object
    case kind: JsonValueKind
    of vkStr: strVal: string
    of vkInt: intVal: int
    of vkList: listVal: seq[JsonValue]
var my_data = {
    "name": JsonValue(kind: vkStr, strVal: "Alice"),
    "scores": JsonValue(kind: vkList, listVal: @[JsonValue(kind: vkInt, intVal: 10), JsonValue(kind: vkInt, intVal: 20), JsonValue(kind: vkInt, intVal: 30)])
}.toTable
