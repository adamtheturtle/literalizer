{.warning[UnusedImport]:off.}
import tables
type
  ValueKind = enum
    vkStr, vkBool
  Value = object
    case kind: ValueKind
    of vkStr: strVal: string
    of vkBool: boolVal: bool
type Record0 = object
    name: string
    input: Table[string, Value]
    expected: Table[string, Value]
var my_data = @[
    Record0(
        name: "test_1",
        input: {
            "type": Value(kind: vkStr, strVal: "create"),
            "pr_id": Value(kind: vkStr, strVal: "pr_1"),
            "draft": Value(kind: vkBool, boolVal: true)
        }.toTable,
        expected: {
            "pr_id": Value(kind: vkStr, strVal: "pr_1"),
            "status": Value(kind: vkStr, strVal: "draft")
        }.toTable
    ),
    Record0(
        name: "test_2",
        input: {
            "type": Value(kind: vkStr, strVal: "publish"),
            "pr_id": Value(kind: vkStr, strVal: "pr_1")
        }.toTable,
        expected: {
            "error": Value(kind: vkStr, strVal: "invalid_operation")
        }.toTable
    )
]
