package main
type objType_ struct{}
func (objType_) ZVal(args ...any) any { return nil }
var obj objType_

func main() {
obj.ZVal(1)
}
