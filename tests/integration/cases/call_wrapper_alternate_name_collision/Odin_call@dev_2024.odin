#+feature dynamic-literals
package main
check_wrapper :: proc(args: ..any) -> any { return nil }

main :: proc() {
check_wrapper(42);
}
