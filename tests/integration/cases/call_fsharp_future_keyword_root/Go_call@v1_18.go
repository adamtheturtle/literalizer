package main
type apiType_ struct{}
func (apiType_) fetch(args ...any) any { return nil }
type processType_ struct{ api apiType_ }
var process processType_

func main() {
process.api.fetch(map[string]any{"data": "hello"})
process.api.fetch(map[string]any{"data": 42})
process.api.fetch(map[string]any{"data": true})
}
