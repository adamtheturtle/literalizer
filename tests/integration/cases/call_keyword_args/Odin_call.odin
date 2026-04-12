#+feature dynamic-literals
package main

main :: proc() {
_throttler_type :: struct {}
check :: proc(_: _throttler_type, _: ..any) {}
throttler := _throttler_type{}
print :: proc(_: ..any) {}
print(throttler.check("user_1", 1000.0))
print(throttler.check("user_2", 2000.5))
_ = my_data
}
