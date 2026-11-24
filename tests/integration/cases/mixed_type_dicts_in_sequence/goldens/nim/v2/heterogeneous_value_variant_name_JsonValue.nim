import tables
type
  JsonValueKind = enum
    vkStr, vkBool, vkTable
  JsonValue = object
    case kind: JsonValueKind
    of vkStr: strVal: string
    of vkBool: boolVal: bool
    of vkTable: tableVal: Table[string, JsonValue]
var my_data = @[
    JsonValue(kind: vkTable, tableVal: {"type": JsonValue(kind: vkStr, strVal: "create"), "pr_id": JsonValue(kind: vkStr, strVal: "pr_1"), "draft": JsonValue(kind: vkBool, boolVal: true)}.toTable),
    JsonValue(kind: vkTable, tableVal: {"type": JsonValue(kind: vkStr, strVal: "create"), "pr_id": JsonValue(kind: vkStr, strVal: "pr_2")}.toTable)
]
