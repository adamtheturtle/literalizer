package main
type mType_ struct{}
func (mType_) Op(args ...any) any { return nil }
var m mType_

func main() {
m.Op(map[string]any{"type": "create", "pr_id": "pr_1", "draft": true});
m.Op(map[string]any{"type": "create", "pr_id": "pr_2"});
}
