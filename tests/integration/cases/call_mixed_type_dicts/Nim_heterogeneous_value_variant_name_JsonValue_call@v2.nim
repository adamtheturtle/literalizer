import tables
{.warning[UnusedImport]:off.}
type
  JsonValueKind = enum
    vkStr, vkBool
  JsonValue = object
    case kind: JsonValueKind
    of vkStr: strVal: string
    of vkBool: boolVal: bool
type MgrType = object
type AppType = object
    mgr: MgrType
template run(self: MgrType; args: varargs[untyped]) = discard
var app: AppType
app.mgr.run({"type": JsonValue(kind: vkStr, strVal: "create"), "pr_id": JsonValue(kind: vkStr, strVal: "pr_1"), "draft": JsonValue(kind: vkBool, boolVal: true)}.toTable)
app.mgr.run({"type": JsonValue(kind: vkStr, strVal: "create"), "pr_id": JsonValue(kind: vkStr, strVal: "pr_2")}.toTable)
