package main
type workerType_ struct{}
func (workerType_) process(args ...any) any { return nil }
type apiType_ struct{ worker workerType_ }
var api apiType_

func main() {
api.worker.process([]any{1, map[string]any{}}, 42)
api.worker.process([]any{2, map[string]string{"x": "s"}}, 43)
}
