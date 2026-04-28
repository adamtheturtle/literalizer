#+feature dynamic-literals
package main
_throttler_check_ :: proc(args: ..any) -> any { return nil }
ThrottlerType_ :: struct { check: proc(..any) -> any }
emit :: proc(args: ..any) -> any { return nil }

main :: proc() {
throttler: ThrottlerType_ = ThrottlerType_{ check = _throttler_check_ }
emit(throttler.check("user_1", 1000.0));
emit(throttler.check("user_2", 2000.5));
}
