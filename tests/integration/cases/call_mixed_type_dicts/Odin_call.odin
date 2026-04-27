#+feature dynamic-literals
package main
MgrType_ :: struct { op: proc(..any) -> any }
AppType_ :: struct { mgr: MgrType_ }
app: AppType_

main :: proc() {
app.mgr.op(map[string]any{"type" = "create", "pr_id" = "pr_1", "draft" = true});
app.mgr.op(map[string]any{"type" = "create", "pr_id" = "pr_2"});
}
