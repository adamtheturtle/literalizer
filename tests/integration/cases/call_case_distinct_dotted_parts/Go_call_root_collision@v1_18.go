package main
type FooType_ struct{}
func (FooType_) bar(args ...any) any { return nil }
type fooType_ struct{ Foo FooType_ }
var foo fooType_

func main() {
foo.Foo.bar([]int{1})
}
