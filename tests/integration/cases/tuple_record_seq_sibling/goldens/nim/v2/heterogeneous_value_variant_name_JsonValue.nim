import tables
type
  JsonValueKind = enum
    vkInt, vkStr, vkList
  JsonValue = object
    case kind: JsonValueKind
    of vkInt: intVal: int
    of vkStr: strVal: string
    of vkList: listVal: seq[JsonValue]
var my_data = {
    "scores": JsonValue(kind: vkList, listVal: @[JsonValue(kind: vkInt, intVal: 10), JsonValue(kind: vkInt, intVal: 20), JsonValue(kind: vkInt, intVal: 30)]),
    "args": JsonValue(kind: vkList, listVal: @[JsonValue(kind: vkInt, intVal: 1), JsonValue(kind: vkStr, strVal: "email"), JsonValue(kind: vkStr, strVal: "a@gmail.com"), JsonValue(kind: vkInt, intVal: 100)])
}.toTable
