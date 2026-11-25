import tables
type
  JsonValueKind = enum
    vkInt, vkStr, vkTable
  JsonValue = object
    case kind: JsonValueKind
    of vkInt: intVal: int
    of vkStr: strVal: string
    of vkTable: tableVal: Table[string, JsonValue]
var my_data = {
    "id": JsonValue(kind: vkInt, intVal: 1),
    "owner": JsonValue(kind: vkTable, tableVal: {"name": JsonValue(kind: vkStr, strVal: "Alice"), "age": JsonValue(kind: vkInt, intVal: 30)}.toTable)
}.toTable
