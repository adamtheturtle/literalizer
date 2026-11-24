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
    Value(kind: vkTable, tableVal: {
        "input": Value(kind: vkTable, tableVal: {
            "kind": Value(kind: vkStr, strVal: "add"),
            "item_id": Value(kind: vkStr, strVal: "item_1"),
            "urgent": Value(kind: vkBool, boolVal: true)
        }.toTable),
        "expected": Value(kind: vkTable, tableVal: {
            "item_id": Value(kind: vkStr, strVal: "item_1"),
            "state": Value(kind: vkStr, strVal: "pending")
        }.toTable)
    }.toTable),
    Value(kind: vkTable, tableVal: {
        "input": Value(kind: vkTable, tableVal: {
            "kind": Value(kind: vkStr, strVal: "remove"),
            "item_id": Value(kind: vkStr, strVal: "item_9")
        }.toTable),
        "expected": Value(kind: vkTable, tableVal: {
            "error": Value(kind: vkStr, strVal: "not_found")
        }.toTable)
    }.toTable)
]
