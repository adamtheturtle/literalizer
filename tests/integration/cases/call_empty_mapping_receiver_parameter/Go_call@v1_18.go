package main
type apiType_ struct{}
func (apiType_) process(args ...any) any { return nil }
var api apiType_

func main() {
api.process(map[string]any{})
}
