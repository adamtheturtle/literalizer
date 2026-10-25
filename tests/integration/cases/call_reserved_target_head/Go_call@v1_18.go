package main
type classType_ struct{}
func (classType_) member(args ...any) any { return nil }
var class classType_

func main() {
class.member(42)
}
