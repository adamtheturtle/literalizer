package main
type throttlerType_ struct{}
func (throttlerType_) check(args ...any) any { return nil }
var throttler throttlerType_
func emit(args ...any) any { return nil }

func main() {
emit(throttler.check("user_1", 1000.0))
emit(throttler.check("user_2", 2000.5))
}
