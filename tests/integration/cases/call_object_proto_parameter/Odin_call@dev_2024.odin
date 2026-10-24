#+feature dynamic-literals
package main
capture :: proc(args: ..any) -> any { return nil }

main :: proc() {
capture(1);
}
