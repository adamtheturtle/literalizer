package main
type helperType_ struct{}
func (helperType_) list(args ...any) any { return nil }
var helper helperType_

func main() {
helper.list(1)
}
