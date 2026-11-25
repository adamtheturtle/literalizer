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
    "title": JsonValue(kind: vkStr, strVal: "report"),
    "tags": JsonValue(kind: vkList, listVal: @[JsonValue(kind: vkStr, strVal: "draft"), JsonValue(kind: vkStr, strVal: "urgent"), JsonValue(kind: vkStr, strVal: "review")]),
    "priority": JsonValue(kind: vkInt, intVal: 2)
}.toTable
