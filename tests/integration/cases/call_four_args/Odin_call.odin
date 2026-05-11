#+feature dynamic-literals
package main
process :: proc(args: ..any) -> any { return nil }

main :: proc() {
process(1, 2, 3, 4);
process(10, 20, 30, 40);
}
