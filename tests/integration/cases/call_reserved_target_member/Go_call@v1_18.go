package main
type objType_ struct{}
func (objType_) class(args ...any) any { return nil }
var obj objType_

func main() {
obj.class(42)
}
