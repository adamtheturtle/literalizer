package main
type FooType_ struct{}
func (FooType_) bar(args ...any) any { return nil }
type fooType_ struct{ Foo FooType_ }
type aType_ struct{ foo fooType_ }
var a aType_

func main() {
a.foo.Foo.bar([]int{1})
}
