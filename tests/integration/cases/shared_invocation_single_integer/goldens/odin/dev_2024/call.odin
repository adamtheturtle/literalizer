#+feature dynamic-literals
package main
consume :: proc(args: ..any) -> any { return nil }

main :: proc() {
consume(1);
}
