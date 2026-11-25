#+feature dynamic-literals
package main
process :: proc(args: ..any) -> any { return nil }
emit :: proc(args: ..any) -> any { return nil }

main :: proc() {
emit(process("hello"), map[string]any{"a" = 1, "b" = 2});
emit(process(42), map[string]any{"c" = 3, "d" = 4});
}
