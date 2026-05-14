#+feature dynamic-literals
package main
_mgr_run_ :: proc(args: ..any) -> any { return nil }
MgrType_ :: struct { run: proc(..any) -> any }
AppType_ :: struct { mgr: MgrType_ }

main :: proc() {
app: AppType_ = AppType_{ mgr = MgrType_{ run = _mgr_run_ } }
app.mgr.run(map[string]any{"type" = "create", "pr_id" = "pr_1", "draft" = true});
app.mgr.run(map[string]any{"type" = "create", "pr_id" = "pr_2"});
}
