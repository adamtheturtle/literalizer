import tables
type
  JsonValueKind = enum
    vkInt, vkStr, vkNull, vkTable
  JsonValue = object
    case kind: JsonValueKind
    of vkInt: intVal: int
    of vkStr: strVal: string
    of vkNull: discard
    of vkTable: tableVal: Table[string, JsonValue]
var my_data = {
    "outer": JsonValue(kind: vkTable, tableVal: {"a": JsonValue(kind: vkInt, intVal: 1), "b": JsonValue(kind: vkStr, strVal: "x"), "c": JsonValue(kind: vkNull)}.toTable)
}.toTable
