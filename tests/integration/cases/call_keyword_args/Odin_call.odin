#+feature dynamic-literals
package main
ThrottlerType_ :: struct { check: proc(..any) -> any }
throttler: ThrottlerType_
emit :: proc(args: ..any) -> any { return nil }

main :: proc() {
emit(throttler.check("user_1", 1000.0));
emit(throttler.check("user_2", 2000.5));
}
