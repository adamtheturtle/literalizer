import tables
type
  ValueKind = enum
    vkStr, vkBool
  Value = object
    case kind: ValueKind
    of vkStr: strVal: string
    of vkBool: boolVal: bool
var my_data = @[
    {"type": Value(kind: vkStr, strVal: "create"), "pr_id": Value(kind: vkStr, strVal: "pr_1"), "draft": Value(kind: vkBool, boolVal: true)}.toTable,
    {"type": Value(kind: vkStr, strVal: "create"), "pr_id": Value(kind: vkStr, strVal: "pr_2")}.toTable
]
