package main
type throttlerType_ struct{}
func (throttlerType_) check(args ...any) any { return nil }
var throttler throttlerType_
func print(args ...any) any { return nil }

func main() {
print(throttler.check("user_1", 1000.0));
print(throttler.check("user_2", 2000.5));
}
