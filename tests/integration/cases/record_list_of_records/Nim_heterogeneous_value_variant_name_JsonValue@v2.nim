import tables
type
  JsonValueKind = enum
    vkStr, vkInt, vkList, vkTable
  JsonValue = object
    case kind: JsonValueKind
    of vkStr: strVal: string
    of vkInt: intVal: int
    of vkList: listVal: seq[JsonValue]
    of vkTable: tableVal: Table[string, JsonValue]
var my_data = {
    "name": JsonValue(kind: vkStr, strVal: "box"),
    "items": JsonValue(kind: vkList, listVal: @[JsonValue(kind: vkTable, tableVal: {"id": JsonValue(kind: vkInt, intVal: 1), "label": JsonValue(kind: vkStr, strVal: "first")}.toTable), JsonValue(kind: vkTable, tableVal: {"id": JsonValue(kind: vkInt, intVal: 2), "label": JsonValue(kind: vkStr, strVal: "second")}.toTable)])
}.toTable
