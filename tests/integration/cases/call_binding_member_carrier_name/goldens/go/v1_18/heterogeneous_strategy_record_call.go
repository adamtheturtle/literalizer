package main
type objType_ struct{}
func (objType_) ZVal(args ...any) any { return nil }
var obj objType_

func main() {
my_data := obj.ZVal(42) // note
_ = my_data
}
