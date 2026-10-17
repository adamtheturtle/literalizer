#+feature dynamic-literals
package main
first_value :: proc(args: ..any) -> any { return nil }

main :: proc() {
first_value(1);
}
