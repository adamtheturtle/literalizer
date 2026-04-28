#+feature dynamic-literals
package main
_mgr_op_ :: proc(args: ..any) -> any { return nil }
MgrType_ :: struct { op: proc(..any) -> any }
AppType_ :: struct { mgr: MgrType_ }

main :: proc() {
app: AppType_ = AppType_{ mgr = MgrType_{ op = _mgr_op_ } }
app.mgr.op(map[string]any{"type" = "create", "pr_id" = "pr_1", "draft" = true});
app.mgr.op(map[string]any{"type" = "create", "pr_id" = "pr_2"});
}
