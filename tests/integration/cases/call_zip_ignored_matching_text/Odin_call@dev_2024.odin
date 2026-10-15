#+feature dynamic-literals
package main
process :: proc(args: ..any) -> any { return nil }

main :: proc() {
process("time.Date(2024, time.January, 15, 12, 0, 0, 0, time.UTC)");
}
