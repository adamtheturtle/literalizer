{.warning[UnusedImport]:off.}
import tables
type
  ValueKind = enum
    vkStr
  Value = object
    case kind: ValueKind
    of vkStr: strVal: string
type Record1 = object
    kind: string
    prId: string
type Record0 = object
    name: string
    input: Record1
    expected: Table[string, Value]
var my_data = @[
    Record0(
        name: "test_1",
        input: Record1(
            kind: "create",
            prId: "pr_1"
        ),
        expected: {
            "pr_id": Value(kind: vkStr, strVal: "pr_1"),
            "status": Value(kind: vkStr, strVal: "draft")
        }.toTable
    ),
    Record0(
        name: "test_2",
        input: Record1(
            kind: "publish",
            prId: "pr_1"
        ),
        expected: {
            "error": Value(kind: vkStr, strVal: "invalid_operation")
        }.toTable
    )
]
