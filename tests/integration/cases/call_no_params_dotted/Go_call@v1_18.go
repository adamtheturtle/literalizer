package main
type throttlerType_ struct{}
func (throttlerType_) check(args ...any) any { return nil }
var throttler throttlerType_

func main() {
throttler.check()
throttler.check()
}
