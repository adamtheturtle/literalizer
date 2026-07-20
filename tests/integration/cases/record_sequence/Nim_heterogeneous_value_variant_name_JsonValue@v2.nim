import tables
type
  JsonValueKind = enum
    vkInt, vkStr, vkList
  JsonValue = object
    case kind: JsonValueKind
    of vkInt: intVal: int
    of vkStr: strVal: string
    of vkList: listVal: seq[JsonValue]
var my_data = @[
    {"id": JsonValue(kind: vkInt, intVal: 1), "label": JsonValue(kind: vkStr, strVal: "first"), "tags": JsonValue(kind: vkList, listVal: newSeq[JsonValue]())}.toTable,
    {"id": JsonValue(kind: vkInt, intVal: 2), "label": JsonValue(kind: vkStr, strVal: "second"), "tags": JsonValue(kind: vkList, listVal: newSeq[JsonValue]())}.toTable,
    {"id": JsonValue(kind: vkInt, intVal: 3), "label": JsonValue(kind: vkStr, strVal: "third"), "tags": JsonValue(kind: vkList, listVal: newSeq[JsonValue]())}.toTable
]
