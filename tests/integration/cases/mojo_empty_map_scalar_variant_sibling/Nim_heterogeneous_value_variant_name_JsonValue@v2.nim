import tables
type
  JsonValueKind = enum
    vkInt, vkStr, vkTable
  JsonValue = object
    case kind: JsonValueKind
    of vkInt: intVal: int
    of vkStr: strVal: string
    of vkTable: tableVal: Table[string, JsonValue]
var my_data = @[
    JsonValue(kind: vkTable, tableVal: {"count": JsonValue(kind: vkInt, intVal: 1), "name": JsonValue(kind: vkStr, strVal: "value")}.toTable),
    JsonValue(kind: vkTable, tableVal: initTable[string, JsonValue]())
]
