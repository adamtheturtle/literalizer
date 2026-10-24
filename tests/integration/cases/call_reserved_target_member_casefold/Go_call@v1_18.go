package main
type objType_ struct{}
func (objType_) BEGIN(args ...any) any { return nil }
var obj objType_

func main() {
obj.BEGIN(42)
}
