package main

func main() {
type _throttlerType struct{}
func (_throttlerType) check(args ...any) any { return nil }
var throttler = _throttlerType{}
func print(args ...any) any { return nil }
print(throttler.check("user_1", 1000.0))
print(throttler.check("user_2", 2000.5))
_ = my_data
}
