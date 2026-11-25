package main
type objType_ struct{}
func (objType_) ZKV(args ...any) any { return nil }
var obj objType_

func main() {
obj.ZKV(1)
}
