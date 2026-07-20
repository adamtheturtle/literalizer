import tables
type
  ValueKind = enum
    vkStr, vkBool, vkTable
  Value = object
    case kind: ValueKind
    of vkStr: strVal: string
    of vkBool: boolVal: bool
    of vkTable: tableVal: Table[string, Value]
var my_data = @[
    Value(kind: vkTable, tableVal: {"type": Value(kind: vkStr, strVal: "create"), "pr_id": Value(kind: vkStr, strVal: "pr_1"), "draft": Value(kind: vkBool, boolVal: true)}.toTable),
    Value(kind: vkTable, tableVal: {"type": Value(kind: vkStr, strVal: "create"), "pr_id": Value(kind: vkStr, strVal: "pr_2")}.toTable)
]
