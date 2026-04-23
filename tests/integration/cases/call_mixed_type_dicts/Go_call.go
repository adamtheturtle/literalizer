package main
type mgrType_ struct{}
func (mgrType_) Op(args ...any) any { return nil }
var mgr mgrType_

func main() {
mgr.Op(map[string]any{"type": "create", "pr_id": "pr_1", "draft": true});
mgr.Op(map[string]any{"type": "create", "pr_id": "pr_2"});
}
