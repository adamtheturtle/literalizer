#+feature dynamic-literals
package main
process :: proc(args: ..any) -> any { return nil }

main :: proc() {
process("hello", "a");
process(42, "b");
process(true, "c");
}
