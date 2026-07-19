import tables
type
  JsonValueKind = enum
    vkStr, vkInt, vkList
  JsonValue = object
    case kind: JsonValueKind
    of vkStr: strVal: string
    of vkInt: intVal: int
    of vkList: listVal: seq[JsonValue]
var my_data = @[
    {"call": JsonValue(kind: vkStr, strVal: "send"), "args": JsonValue(kind: vkList, listVal: @[JsonValue(kind: vkInt, intVal: 1), JsonValue(kind: vkStr, strVal: "email"), JsonValue(kind: vkStr, strVal: "a@gmail.com"), JsonValue(kind: vkInt, intVal: 100)])}.toTable,
    {"call": JsonValue(kind: vkStr, strVal: "recv"), "args": JsonValue(kind: vkList, listVal: @[JsonValue(kind: vkInt, intVal: 2), JsonValue(kind: vkStr, strVal: "sms"), JsonValue(kind: vkStr, strVal: "b@example.com"), JsonValue(kind: vkInt, intVal: 200)])}.toTable
]
