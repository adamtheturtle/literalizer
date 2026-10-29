package main
type processType_ struct{}
func (processType_) fetch(args ...any) any { return nil }
type appType_ struct{ process processType_ }
var app appType_

func main() {
app.process.fetch(map[string]any{"data": "hello"})
app.process.fetch(map[string]any{"data": 42})
app.process.fetch(map[string]any{"data": true})
}
