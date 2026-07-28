#+feature dynamic-literals
package main
process :: proc(args: ..any) -> any { return nil }

main :: proc() {
process("09:30:00");
process("2024-01-15T00:00:00+00:00");
process(1);
}
