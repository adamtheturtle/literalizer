package main
type workerType_ struct{}
func (workerType_) process(args ...any) any { return nil }
type apiType_ struct{ worker workerType_ }
var api apiType_

func main() {
api.worker.process(map[string]any{}, map[string]any{})
}
