#+feature dynamic-literals
package main
_throttler_check_ :: proc(args: ..any) -> any { return nil }
ThrottlerType_ :: struct { check: proc(..any) -> any }

main :: proc() {
throttler: ThrottlerType_ = ThrottlerType_{ check = _throttler_check_ }
throttler.check();
throttler.check();
}
