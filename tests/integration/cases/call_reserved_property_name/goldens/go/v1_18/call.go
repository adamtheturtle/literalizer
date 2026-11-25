package main
type fooType_ struct{}
func (fooType_) class(args ...any) any { return nil }
var foo fooType_

func main() {
foo.class(1)
}
