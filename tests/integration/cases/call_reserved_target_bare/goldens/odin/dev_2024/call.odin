#+feature dynamic-literals
package main
class :: proc(args: ..any) -> any { return nil }

main :: proc() {
class(42);
}
