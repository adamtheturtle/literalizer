import tables
type
  JsonValueKind = enum
    vkStr, vkBool
  JsonValue = object
    case kind: JsonValueKind
    of vkStr: strVal: string
    of vkBool: boolVal: bool
var my_data = @[
    {"type": JsonValue(kind: vkStr, strVal: "create"), "pr_id": JsonValue(kind: vkStr, strVal: "pr_1"), "draft": JsonValue(kind: vkBool, boolVal: true)}.toTable,
    {"type": JsonValue(kind: vkStr, strVal: "create"), "pr_id": JsonValue(kind: vkStr, strVal: "pr_2")}.toTable
]
