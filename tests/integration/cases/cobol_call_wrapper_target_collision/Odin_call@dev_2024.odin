#+feature dynamic-literals
package main
check :: proc(args: ..any) -> any { return nil }

main :: proc() {
check(42);
}
