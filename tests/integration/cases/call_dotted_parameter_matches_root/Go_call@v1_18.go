package main
type outerType_ struct{}
func (outerType_) inner(args ...any) any { return nil }
var outer outerType_

func main() {
outer.inner(1, 2)
}
