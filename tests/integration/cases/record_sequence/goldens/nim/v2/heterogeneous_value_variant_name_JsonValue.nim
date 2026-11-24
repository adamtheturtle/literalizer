import tables
type
  JsonValueKind = enum
    vkInt, vkStr, vkList, vkTable
  JsonValue = object
    case kind: JsonValueKind
    of vkInt: intVal: int
    of vkStr: strVal: string
    of vkList: listVal: seq[JsonValue]
    of vkTable: tableVal: Table[string, JsonValue]
var my_data = @[
    JsonValue(kind: vkTable, tableVal: {"id": JsonValue(kind: vkInt, intVal: 1), "label": JsonValue(kind: vkStr, strVal: "first"), "tags": JsonValue(kind: vkList, listVal: newSeq[JsonValue]())}.toTable),
    JsonValue(kind: vkTable, tableVal: {"id": JsonValue(kind: vkInt, intVal: 2), "label": JsonValue(kind: vkStr, strVal: "second"), "tags": JsonValue(kind: vkList, listVal: newSeq[JsonValue]())}.toTable),
    JsonValue(kind: vkTable, tableVal: {"id": JsonValue(kind: vkInt, intVal: 3), "label": JsonValue(kind: vkStr, strVal: "third"), "tags": JsonValue(kind: vkList, listVal: newSeq[JsonValue]())}.toTable)
]
