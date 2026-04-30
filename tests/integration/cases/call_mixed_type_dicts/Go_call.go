package main
type mgrType_ struct{}
func (mgrType_) run(args ...any) any { return nil }
type appType_ struct{ mgr mgrType_ }
var app appType_

func main() {
app.mgr.run(map[string]any{"type": "create", "pr_id": "pr_1", "draft": true});
app.mgr.run(map[string]any{"type": "create", "pr_id": "pr_2"});
}
