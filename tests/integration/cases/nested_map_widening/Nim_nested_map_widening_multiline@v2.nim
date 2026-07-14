import tables
type
  ValueKind = enum
    vkStr, vkBool
  Value = object
    case kind: ValueKind
    of vkStr: strVal: string
    of vkBool: boolVal: bool
var my_data = @[
    {
        "input": {
            "kind": Value(kind: vkStr, strVal: "add"),
            "item_id": Value(kind: vkStr, strVal: "item_1"),
            "urgent": Value(kind: vkBool, boolVal: true)
        }.toTable,
        "expected": {
            "item_id": Value(kind: vkStr, strVal: "item_1"),
            "state": Value(kind: vkStr, strVal: "pending")
        }.toTable
    }.toTable,
    {
        "input": {
            "kind": Value(kind: vkStr, strVal: "remove"),
            "item_id": Value(kind: vkStr, strVal: "item_9")
        }.toTable,
        "expected": {
            "error": Value(kind: vkStr, strVal: "not_found")
        }.toTable
    }.toTable
]
